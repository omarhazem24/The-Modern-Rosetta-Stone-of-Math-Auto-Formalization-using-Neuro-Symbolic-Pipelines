import os

def fix_prompts():
    with open('scripts/llm_translator.py', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace(
        "Translate the English math to strictly-typed Lean 4 code. Include imports (e.g. import Mathlib). Output only raw code.",
        "Translate the English math to strictly-typed Lean 4 code. Include imports (e.g. import Mathlib). Crucially, account for complex algebraic topology theorems, proofs, and advanced graph theory algorithms/optimizations. Output only raw code."
    )
    text = text.replace(
        "Act as an expert Lean 4 mathematician.",
        "Act as an expert Lean 4 mathematician, specialized in Algebraic Topology and Advanced Graph Theory."
    )

    with open('scripts/llm_translator.py', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    fix_prompts()
    print("Prompts updated successfully.")