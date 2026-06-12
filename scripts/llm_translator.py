import os
import argparse
import subprocess
import json
import re
import time
import hashlib
import concurrent.futures

try:
    import openai
except ImportError:
    print("Please install required libraries: pip install openai")
    exit(1)

DEFAULT_COMPILE_TIMEOUT = 90
DEFAULT_MAX_RETRIES = 5
LAKE_PREFLIGHT_TIMEOUT = 30
LAKE_INITIAL_BUILD_TIMEOUT = 600

# Shared system prompt using custom ManualFormalization definitions
LEAN_SYSTEM_PROMPT = (
    "Translate English math to Lean 4 using the 'ManualFormalization' namespace. "
    "Always import Definitions. Mathlib4 is available for use.\n"
    "Common modules: Mathlib.Tactic, Mathlib.Analysis.Calculus.Deriv.Basic, Mathlib.Topology.Basic, Mathlib.Data.Set.Basic.\n"
    "Note: Do NOT use 'Mathlib.Topology.Continuity' (use Mathlib.Topology.Basic instead).\n"
    "Custom definitions from Definitions.lean:\n"
    "- is_subset A B, set_union A B, set_intersection A B, are_disjoint A B\n"
    "- set_complement A, set_difference A B, symmetric_difference A B\n"
    "- is_injective f, is_surjective f, is_bijective f\n"
    "- implies p q, iff_def p q\n"
    "Structure your output like this:\n"
    "```lean\n"
    "import Definitions\n"
    "import Mathlib.Tactic\n"
    "namespace ManualFormalization\n"
    "-- (Your Lean code here)\n"
    "end ManualFormalization\n"
    "```\n"
    "Output ONLY Lean code."
)


def get_lean_dir() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Lean")


def get_next_output_filename(lean_dir: str) -> str:
    n = 1
    while True:
        filename = f"Output{n}.lean"
        if not os.path.exists(os.path.join(lean_dir, filename)):
            return filename
        n += 1


def resolve_output_path(output_file: str, use_lake: bool) -> str:
    lean_dir = get_lean_dir()
    if use_lake:
        # Instead of fixed Theorems.lean, use Output(n).lean
        filename = get_next_output_filename(lean_dir)
        return os.path.join(lean_dir, filename)
    return os.path.abspath(output_file)


def detect_lake_available(lean_dir: str) -> bool:
    try:
        result = subprocess.run(
            ["lake", "env", "lean", "--version"],
            cwd=lean_dir, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=LAKE_PREFLIGHT_TIMEOUT,
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass
    return False


def is_mathlib_setup_error(error_msg: str) -> bool:
    return "unknown module prefix 'Mathlib'" in error_msg


def truncate_error(error_msg: str, max_len: int = 1500) -> str:
    msg = error_msg.strip()
    # Remove long absolute paths to make it more readable in the terminal
    lean_dir = get_lean_dir().replace("\\", "/")
    msg = msg.replace(lean_dir, ".")
    msg = msg.replace(os.path.dirname(lean_dir).replace("\\", "/"), "..")
    
    if len(msg) <= max_len:
        return msg
    return "... (truncated)\n" + msg[-max_len:]


def fetch_mathlib_cache(lean_dir: str, timeout: int = 600) -> bool:
    try:
        result = subprocess.run(
            ["lake", "exe", "cache", "get"], cwd=lean_dir,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        return result.returncode == 0
    except Exception:
        return False


def ensure_lake_target_ready(lean_dir: str, timeout: int = LAKE_INITIAL_BUILD_TIMEOUT) -> bool:
    fetch_mathlib_cache(lean_dir)
    try:
        # Build Definitions.lean since others depend on it
        result = subprocess.run(
            ["lake", "build", "Definitions"], cwd=lean_dir,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        return result.returncode == 0
    except Exception:
        return False


def compile_lean(file_path: str, use_lake: bool = True, timeout: int = DEFAULT_COMPILE_TIMEOUT) -> tuple[bool, str]:
    lean_dir = get_lean_dir()
    # If use_lake is True, we use 'lean' command but with 'lake env' to ensure dependencies are loaded
    # because 'lake build LAKE_TARGET' only builds the static library defined in lakefile.
    if use_lake:
        cmd = ["lake", "env", "lean", file_path]
    else:
        cmd = ["lean", os.path.abspath(file_path)]
    
    try:
        result = subprocess.run(
            cmd, cwd=lean_dir if use_lake else None,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        # Capture BOTH stdout and stderr as Lake can print errors to either
        err = (result.stdout or "") + (result.stderr or "")
        err = err.strip()
        return result.returncode == 0, err
    except subprocess.TimeoutExpired:
        return False, f"Compilation timed out after {timeout}s."
    except Exception as e:
        return False, f"Subprocess Error: {str(e)}"


def extract_lean_code(text: str) -> str:
    blocks = re.findall(r"```(?:lean|Lean|LEAN)?\n(.*?)```", text, re.DOTALL)
    if blocks:
        return blocks[-1].strip()
    return text.replace("```lean", "").replace("```", "").strip()


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def apply_deterministic_fixes(lean_code: str, error_msg: str) -> str:
    fixed = lean_code
    if "Invalid field" in error_msg and "adj" in error_msg.lower():
        fixed = re.sub(r"\.adj\b", ".Adj", fixed)
    for old, new in {
        "import Mathlib.Graph.Basic": "import Mathlib.Combinatorics.SimpleGraph.Basic",
        "import Mathlib.GraphTheory.Basic": "import Mathlib.Combinatorics.SimpleGraph.Basic",
    }.items():
        fixed = fixed.replace(old, new)
    return fixed


def get_llama_translation(english_text: str) -> str:
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
             return "-- Error: GROQ_API_KEY missing"
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": LEAN_SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate: '{english_text}'"},
            ], temperature=0.0)
        return extract_lean_code(r.choices[0].message.content) if r.choices else "-- Error: No response"
    except Exception as e:
        return f"-- Llama Exception: {e}"


def get_gemini_translation(english_text: str) -> str:
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return "-- Error: GEMINI_API_KEY missing"
        client = openai.OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        r = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": LEAN_SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate: '{english_text}'"},
            ], temperature=0.0)
        return extract_lean_code(r.choices[0].message.content) if r.choices else "-- Error: No response"
    except Exception as e:
        return f"-- Gemini Exception: {e}"


def get_llama8b_translation(english_text: str) -> str:
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
             return "-- Error: GROQ_API_KEY missing"
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": LEAN_SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate: '{english_text}'"},
            ], temperature=0.0)
        return extract_lean_code(r.choices[0].message.content) if r.choices else "-- Error: No response"
    except Exception as e:
        return f"-- Llama8b Exception: {e}"


def get_gemini_critique(lean_code: str, compiler_error: str, error_history: str) -> str:
    print("\n[Critic] Analyzing the compiler error...")
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return "Strategy: GEMINI_API_KEY missing"
        client = openai.OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        prompt = (
            f"Code:\n{lean_code}\n\nError:\n{compiler_error}\n\nHistory:\n{error_history}\n\n"
            "Give a 3-step Lean 4 repair strategy.\n"
            "Note: If the error is 'object file does not exist' or 'unknown module', it means an import is wrong. "
            "Recommend a common alternative (e.g., use Mathlib.Topology.Basic instead of Mathlib.Topology.Continuity).\n"
            "Do NOT suggest editing lakefile."
        )
        r = client.chat.completions.create(model="gemini-2.5-flash", messages=[{"role": "user", "content": prompt}], temperature=0.0)
        return r.choices[0].message.content if r.choices else "Check imports and syntax."
    except Exception as e:
        return f"Strategy: {e}"


def get_llama_repair(lean_code: str, critique: str, compiler_error: str) -> str:
    print("\n[Actor] Llama 3.3 is repairing the code...")
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
             return lean_code
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        prompt = f"Code:\n{lean_code}\n\nError:\n{compiler_error}\n\nStrategy:\n{critique}\n\nOutput ONLY fixed Lean 4 code."
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Lean 4 repair actor. Output only code."}, {"role": "user", "content": prompt}],
            temperature=0.0)
        return extract_lean_code(r.choices[0].message.content) if r.choices else lean_code
    except Exception as e:
        print(f"Repair Error: {e}")
        return lean_code


def validate_prompt_logic(english_text: str) -> tuple[bool, str]:
    """
    Validates if the input text is a math prompt.
    Uses basic heuristics first, then a very small, fast model for validation.
    """
    clean_text = english_text.lower().strip()

    # 1. Fast Heuristic Check: Keywords often found in math prompts
    math_keywords = ["let ", "define ", "theorem", "prove ", "graph", "set ", "function", "limit", "subset", "disjoint", "is a ", "if "]
    is_mathematical_start = any(clean_text.startswith(kw) for kw in math_keywords)
    
    # Common non-math greetings/prose
    greetings = ["hello", "hi", "test", "how are you", "what is your name", "hey"]
    if clean_text in greetings:
        return False, "Input is a greeting."

    # If it clearly looks like a theorem or definition, skip the LLM check to save time
    if len(clean_text.split()) > 5 and is_mathematical_start:
        return True, "Passed heuristic math check."

    print("\n[Validator] Analyzing mathematical validity of the prompt...")
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return False, "GEMINI_API_KEY is missing."
             
        # Reverting to gemini-2.5-flash as per user API key requirements
        client = openai.OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        prompt = (
            f"Is this input a math statement? '{english_text}'\n"
            "Return JSON: {\"is_valid\": bool, \"explanation\": \"short reason\"}"
        )
        r = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.0)
        # Use gpt-4o-mini or similar if using OpenAI, but since we are using Gemini endpoint:
        # gemini-2.5-flash is the standard naming.
        r = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0)
        
        text = re.sub(r"```json\n?|```", "", r.choices[0].message.content).strip()
        res = json.loads(text)
        return bool(res.get("is_valid")), res.get("explanation", "No explanation provided.")
    except Exception as e:
        print(f"Validator Warning: {e}")
        # If it's a known non-math input and the API fails, we should still fail.
        # But if the prompt is complex and just the API failed, we might want to allow it?
        # Actually, user wants it to STOP the command.
        return False, f"Validation failed to execute: {e}"


def write_lean_file(path: str, code: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)


def try_compile_and_fix(code: str, compile_path: str, use_lake: bool, compile_timeout: int) -> tuple[bool, str, str]:
    for attempt in range(3):
        write_lean_file(compile_path, code)
        print(f"  Compiling (attempt {attempt + 1}/3)...")
        t0 = time.time()
        ok, err = compile_lean(compile_path, use_lake, compile_timeout)
        print(f"  Compile finished in {time.time() - t0:.1f}s")
        if ok:
            return True, code, ""
        err = truncate_error(err)
        fixed = apply_deterministic_fixes(code, err)
        if fixed == code:
            return False, code, err
        code = fixed
    return False, code, err


def multi_agent_consensus_and_repair(english_text: str, output_file: str, max_retries: int = DEFAULT_MAX_RETRIES, compile_timeout: int = DEFAULT_COMPILE_TIMEOUT):
    # Pass the GROQ_API_KEY to the validator (using Groq's endpoint and Llama 3.3)
    is_valid, reason = validate_prompt_logic(english_text)
    if not is_valid:
        print(f"\nPrompt REJECTED: {reason}")
        print("Aborting translation.")
        return False, 0

    lean_dir = get_lean_dir()
    use_lake = detect_lake_available(lean_dir)
    if use_lake:
        ensure_lake_target_ready(lean_dir, max(compile_timeout, LAKE_INITIAL_BUILD_TIMEOUT))
    
    compile_path = resolve_output_path(output_file, use_lake)

    print("\nStarting Multi-Agent Processing...")
    with concurrent.futures.ThreadPoolExecutor() as ex:
        llama_code = ex.submit(get_llama_translation, english_text).result()
        ex.submit(get_gemini_translation, english_text).result()
        ex.submit(get_llama8b_translation, english_text).result()

    current_code = llama_code
    error_history = ""
    prev = (None, None)
    stagnation = 0

    for iteration in range(1, max_retries + 1):
        print(f"\n========== Iteration {iteration}/{max_retries} ==========")
        ok, current_code, err = try_compile_and_fix(current_code, compile_path, use_lake, compile_timeout)
        if ok:
            write_lean_file(os.path.abspath(output_file), current_code)
            print("\n" + "="*40)
            print("FINAL LEAN CODE:")
            print("-" * 40)
            print(current_code)
            print("-" * 40)
            print("Verification PASSED!")
            print("="*40)
            return True, iteration

        # Highlight error in terminal
        print("\n\033[91m" + "!"*10 + " VERIFICATION FAILED " + "!"*10 + "\033[0m")
        print(f"\033[93m{err}\033[0m")
        print("\033[91m" + "!"*41 + "\033[0m\n")
        if use_lake and is_mathlib_setup_error(err):
            print("\nMathlib not built. Run:\n  cd Lean\n  lake exe cache get\n  lake build TranslatorOutput\n")
            write_lean_file(os.path.abspath(output_file), current_code)
            return False, iteration

        h = (stable_hash(current_code), stable_hash(err))
        stagnation = stagnation + 1 if h == prev else 0
        prev = h
        if stagnation >= 2:
            print("Stopping: no progress.")
            return False, iteration
        if iteration == max_retries:
            return False, iteration

        error_history = (error_history + f"\nIter {iteration}: {err}\n")[-2500:]
        critique = get_gemini_critique(current_code, err, error_history)
        repaired = get_llama_repair(current_code, critique, err)
        if repaired.strip() == current_code.strip():
            return False, iteration
        current_code = repaired

    return False, max_retries


def generate_report():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    print("Generating report...")
    os.makedirs("img", exist_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    parser.add_argument("--output", default="Output.lean")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES)
    parser.add_argument("--compile-timeout", type=int, default=DEFAULT_COMPILE_TIMEOUT)
    args = parser.parse_args()
    if args.report:
        generate_report()
    elif args.text.strip():
        ok, n = multi_agent_consensus_and_repair(args.text.strip(), args.output, args.max_retries, args.compile_timeout)
        print(f"\n{'Success' if ok else 'Failed'} after {n} iteration(s).")
    else:
        try:
            text = input("\nEnter math to translate:\n> ").strip()
            if text:
                ok, n = multi_agent_consensus_and_repair(text, args.output, args.max_retries, args.compile_timeout)
                print(f"\n{'Success' if ok else 'Failed'} after {n} iteration(s).")
        except KeyboardInterrupt:
            print("\nExiting.")
