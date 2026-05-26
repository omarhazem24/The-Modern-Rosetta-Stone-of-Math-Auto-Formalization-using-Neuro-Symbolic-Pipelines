# The Modern Rosetta Stone of Mathematics
## Neuro-Symbolic Auto-Formalization using Multi-Agent Pipelines

### Overview
This project implement a neuro-symbolic bridge for the automatic translation of natural language mathematical statements into formal, machine-verifiable Lean 4 code. The system architecture utilizes a multi-agent cluster consisting of Llama 3.3, Gemini 2.5, and Llama 3.1 8B to achieve consensus-driven formalization and iterative error correction.

### Key Components
- **Logical Validation**: A pre-processing agent evaluates the mathematical consistency of input prompts. It identifies and rejects non-mathematical inputs or logical hallucinations before formalization begins.
- **Multi-Agent Consensus**: Three distinct LLMs generate candidate Lean 4 code in parallel. The system prioritizes consensus results to increase translation accuracy.
- **Iterative Repair Loop**: A critic-actor loop identifies Lean compiler errors. Gemini serves as the critic, generating repair strategies that are executed by a Llama 3.3 actor until the code passes verification.
- **Mathlib4 Integration**: The pipeline is specifically tuned for modern Lean 4 Mathlib conventions, with specialized handling for graph theory and topology.

### Repository Structure
- `scripts/llm_translator.py`: The core execution engine containing the validation logic, multi-agent coordination, and repair loops.
- `scripts/evaluate_pipeline.py`: Utilities for measuring success rates and iteration counts across different mathematical domains.
- `scripts/dataset.py`: Collection of mathematical benchmarks used for testing the pipeline's robustness.

### Requirements
- Python 3.10 or higher
- Lean 4 and Lake
- API keys for OpenAI (configured for Google Gemini and Groq)

### Usage
Run the translator script to begin the interactive formalization process:
```bash
python scripts/llm_translator.py
```

To generate a performance report based on benchmark data:
```bash
python scripts/llm_translator.py --report
```

### Authors
Omar Hazem
Department of Computer Science
The German University in Cairo (GUC)
