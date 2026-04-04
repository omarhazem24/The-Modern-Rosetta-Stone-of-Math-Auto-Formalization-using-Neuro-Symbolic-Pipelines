import os
import argparse
import subprocess
import json
import re
from google import genai

def compile_lean(file_path: str) -> tuple[bool, str]:
    # NOTE: Assumes 'lean' is installed and accessible in the system PATH
    result = subprocess.run(["lean", file_path], capture_output=True, text=True)
    is_success = result.returncode == 0
    error_msg = result.stderr if result.stderr else result.stdout
    return is_success, error_msg

def repair_loop_translation(english_text: str, output_file: str, max_retries: int = 5, api_key: str = None) -> dict:
    """
    Translates English math to Lean 4 code using a Neuro-Symbolic Iterative Repair Loop.
    """
    client_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not client_key:
        raise ValueError("API key not found. Please set GEMINI_API_KEY environment variable.")
    
    # Configure the newer Google GenAI SDK
    client = genai.Client(api_key=client_key)
    
    system_prompt = (
        "Role: You are a Neuro-Symbolic Repair Agent specializing in Lean 4 formalization. Your goal is to translate natural language mathematics into machine-verifiable code by acting as a bridge between the LLM and the Lean Compiler (Symbolic Auditor).\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. ALWAYS include all necessary imports, such as `import Mathlib` at the top of the file.\n"
        "2. Only return raw, executable Lean 4 code. Do NOT output markdown code blocks (```lean), conversational text, or explanations.\n"
        "3. Ensure your types, theorems, definitions, and syntax strictly adhere to Lean 4 standards.\n"
        "Truth Source: Do not assume the LLM is correct; only a successful compilation counts as 'Truth'."
    )
    
    # Initialize the chat session
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0
        )
    )
    
    metrics = {
        "initial_text": english_text,
        "initial_translation": "",
        "success": False,
        "iterations": 0,
        "errors": [],
        "last_error": "",
        "last_repair_prompt": "",
        "verified_code": ""
    }
    
    # The first prompt
    current_prompt = f"Translate the following text into Lean 4 code:\n'{english_text}'"

    for iteration in range(1, max_retries + 1):
        metrics["iterations"] = iteration
        print(f"\n=========================================")
        print(f"--- Translation Iteration {iteration}/{max_retries} ---")
        
        # Send message to Gemini
        response = chat.send_message(current_prompt)
        lean_code = response.text.strip()
        
        # Ingenious Solution 1: Clean up potential markdown if the model hallucinated it
        code_blocks = re.findall(r"```(?:lean|Lean|LEAN)?\n(.*?)```", response.text, re.DOTALL)
        if code_blocks:
            lean_code = code_blocks[-1].strip()
        else:
            lean_code = lean_code.replace("```lean", "").replace("```", "").strip()

        if iteration == 1:
            metrics["initial_translation"] = lean_code

        # Add the assistant's generated code to the conversation history (Handled automatically by Gemini chat)
        
        print("Generated Code:\n" + lean_code)
        
        # Save to file to compile
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(lean_code)
            
        print("\nRunning Lean Compiler Verification (Symbolic Auditor)...")
        is_success, error_msg = compile_lean(output_file)
        
        if is_success:
            print("Verification Constraint PASSED: Code compiled successfully. Truth established.")
            metrics["success"] = True
            metrics["verified_code"] = lean_code
            break
        else:
            print("Verification Constraint FAILED. The LLM generated mathematically invalid code.")
            
            # Ingenious Solution 2: Context Window Truncation (avoid overloading the model with massive trace)
            truncated_error = error_msg[:1000]
            print(f"--- Lean Compiler Error (Feedback for \\Phi mapping) ---\n")
            print(truncated_error + ("...\n[Truncated]" if len(error_msg) > 1000 else ""))
            print("---------------------------------------------------------")
            
            metrics["errors"].append(error_msg)
            metrics["last_error"] = truncated_error
            
            # State-Space Pivot: If max retries hit, fallback
            if iteration == max_retries:
                print(f"Fallback Paradigm activated: Reached maximum iterations. Please categorize this logical fallacy into the Manual Auto-Formalization Benchmark.")
                break
                
            # Formal mapping Phi: Error -> Prompt
            current_prompt = (
                f"The Lean 4 compiler returned the following error for your previous code:\n{truncated_error}\n\n"
                f"Please follow this structured transformation:\n"
                f"1. Extract Context: Identify the specific line, term, and expected type.\n"
                f"2. Categorize Fallacy: Determine if it is a Type Mismatch, Unsolved Goal, or Syntax Error.\n"
                f"3. Cross-Reference Schema: Refer back to the Atomic Definitions in the Lean 4 Formal Library.\n"
                f"4. Generate Correction: Rewrite only the failing segment, keeping the rest of the proof-trace intact.\n\n"
                f"Output ONLY the complete, repaired raw Lean 4 code. "
                f"Remember to include necessary imports (e.g., 'import Mathlib'). Ensure variables and types are properly declared "
                f"before use. NEVER include markdown blocks, just the code itself."
            )
            metrics["last_repair_prompt"] = current_prompt
            
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neuro-Symbolic Math Translator with Repair Loop")
    parser.add_argument("--text", type=str, required=True, help="English math text to translate")
    parser.add_argument("--output", type=str, default="Output.lean", help="Output .lean file name")
    parser.add_argument("--max-retries", type=int, default=5, help="Maximum number of repair iterations")
    
    args = parser.parse_args()

    print(f"Translating: '{args.text}'...")
    
    try:
        metrics = repair_loop_translation(args.text, args.output, args.max_retries)
        
        # Track persistent metric stats
        stats_file = "benchmark_stats.json"
        stats = {"total_attempts": 0, "total_successes": 0}
        if os.path.exists(stats_file):
            with open(stats_file, "r") as f:
                stats = json.load(f)
                
        stats["total_attempts"] += 1
        if metrics["success"]:
            stats["total_successes"] += 1
            
        with open(stats_file, "w") as f:
            json.dump(stats, f)
            
        overall_rate = (stats["total_successes"] / stats["total_attempts"]) * 100

        print("\n\n=== Formal Proof-Trace ===")
        print(f"Natural Language Input: {metrics['initial_text']}")
        print(f"\nInitial Lean Translation:\n{metrics['initial_translation']}")
        
        if len(metrics['errors']) > 0:
            print(f"\nCompiler Error Message:\n{metrics['last_error']}")
            print(f"\nRepair Prompt:\n{metrics['last_repair_prompt']}")
            
        if metrics["success"]:
            print(f"\nVerified Lean Code:\n{metrics['verified_code']}")
        else:
            print(f"\nVerified Lean Code: [FAILED TO VERIFY AFTER {metrics['iterations']} ITERATIONS]")
        print("==========================\n")

        print("--- Metric Report (Repair Success Rate) ---")
        print(f"Current Statement Iterations: {metrics['iterations']}")
        print(f"Successful Compilation: {metrics['success']}")
        print(f"Error Count: {len(metrics['errors'])}")
        print("-------------------------------------------")
        print(f"Historical Benchmark Runs: {stats['total_attempts']}")
        print(f"Historical Successes: {stats['total_successes']}")
        print(f"Overall Autonomy Success Rate: {overall_rate:.2f}%")
        print("===========================================")
        
        if metrics["success"]:
            print(f"\nFinal Verified Lean 4 code saved to '{args.output}'")
        else:
            print(f"\nProcess failed after {metrics['iterations']} iterations. Last output saved to '{args.output}'. Manual intervention required.")
            
            # Log the errors for the benchmark
            with open("lean_errors.txt", "a", encoding="utf-8") as f:
                f.write(f"\n--- Failed Definition: {args.text} ---\n")
                if metrics["errors"]:
                    f.write(metrics["errors"][-1])
                f.write("\n==========================================\n")
            
    except Exception as e:
        print(f"Error during translation: {e}")
