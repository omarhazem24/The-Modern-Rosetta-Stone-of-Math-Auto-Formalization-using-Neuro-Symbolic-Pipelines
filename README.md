# The Modern Rosetta Stone of Math: Auto-Formalization using Neuro-Symbolic Pipelines

This repository contains the full automated pipeline and LaTeX thesis artifacts for the Bachelor's study on applying Neuro-Symbolic AI to translate informal mathematics into formally verified Lean 4 code.

## 📖 Project Overview
Natural language math is inherently ambiguous and prone to implicit assumptions, while formal verification systems (like Lean 4) require rigorous, unambiguous, and structurally flawless logical syntax. 

This project builds a **"Truth Scanner" pipeline**. It utilizes Large Language Models (LLMs) to creatively decompose complex mathematical definitions from Rosen's textbook, and relies on the strict compiler of Lean 4 as the ultimate standard of validation. By pairing the "Neuro" capabilities of the LLM with the "Symbolic" constraints of Lean, mathematical hallucinations are eliminated.

## 🗂 Folder Structure

- `/Lean`: Contains the `lake` system and the "Ground Truth" manual formalization files (`Definitions.lean`, `Theorems.lean`).
- `/scripts`: Contains the Python automation logic. Currently contains `llm_translator.py` wrapper for the OpenAI API.
- `/img`: LaTeX image assets and architecture diagrams.
- `*.tex`: The LaTeX source files for compiling the thesis document.
- `main.tex`: Extracted modular LaTeX orchestrator file linking all the thesis chapters.

## 🚀 How to Use the Translation Script

The Python script (`scripts/llm_translator.py`) sends English math textbook definitions to the OpenAI API and retrieves explicitly typed Lean 4 code.

### 1. Requirements
Ensure you have python and the OpenAI library installed:
```bash
pip install openai
```

### 2. Setting Your API Key
You must have a valid OpenAI API key exposed in your environment.
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Mac/Linux
export OPENAI_API_KEY="sk-your-key-here"
```

### 3. Running the Pipeline
Pass any mathematical statement via the `--text` argument:
```bash
python scripts/llm_translator.py --text "The union of two sets A and B contains all elements that are in A or in B." --output "Test.lean"
```
The script will cleanly query the LLM model and yield `.lean` syntax directly to `Test.lean`.

## 📜 How to Compile the Thesis
To build the thesis PDF locally:
1. Ensure you have MikTeX or TeXLive installed.
2. Run standard `pdflatex` compilation from the root directory:
   ```bash
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```
3. A formatted `main.pdf` standard A4 document will be generated.
