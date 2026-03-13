import os
import json
import argparse
from openai import OpenAI

def translate_math_to_lean(english_text: str, api_key: str = None) -> str:
    """
    Translates an informal English mathematical definition into Lean 4 code
    using the OpenAI API.
    """
    # Use provided API key or fallback to environment variable
    client_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not client_key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=client_key)

    system_prompt = """You are an expert mathematician and a specialist in the interactive theorem prover Lean 4.
Your goal is to translate English mathematical definitions exactly into valid, compilable Lean 4 code.
Always use explicit type annotations for quantifiers (e.g., `∀ (x : α)` instead of `∀ x`) and explicitly typed set bindings.
You may import Mathlib library modules if necessary (e.g., `import Mathlib.Data.Set.Basic`).
Only output the raw Lean code in your response without ANY markdown formatting (no ```lean blocks)."""

    user_prompt = f"""Translate the following text from Kenneth Rosen's Discrete Mathematics into Lean 4 code:
"{english_text}"
"""

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4-turbo" / "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neuro-Symbolic Math Translator")
    parser.add_argument("--text", type=str, required=True, help="English math text to translate")
    parser.add_argument("--output", type=str, default="Output.lean", help="Output .lean file name")
    
    args = parser.parse_args()
    
    print(f"Translating: '{args.text}'...")
    
    try:
        lean_code = translate_math_to_lean(args.text)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(lean_code)
        print(f"Success! Lean 4 code saved to '{args.output}'")
        print("\n--- Generated Code ---\n" + lean_code + "\n----------------------\n")
    except Exception as e:
        print(f"Error during translation: {e}")
