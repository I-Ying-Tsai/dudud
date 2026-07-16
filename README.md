## Academic Decompiler

An advanced academic paper compilation and optimization framework based on Non-linear Closed-loop Verification and Multi-objective Product Export.

By constraining probabilistic LLM outputs into a deterministic runtime sandbox, this project eliminates semantic cascades of errors, automatically reconstructing a Minimum Viable Implementation (MVI) and technical specifications from complex research papers.

## Why Academic Decompiler?

When translating complex mathematical papers into production-ready code, engineers often face three major challenges:

* The Implementation Gap: Papers provide abstract formulas but lack executable, clean source code.

* LLM Hallucinations: Standard LLMs write code that appears correct but contains subtle matrix dimension mismatches or syntax errors.

* Execution Blindness: Generative outputs are rarely verified against a ground-truth mathematical runtime before delivery.

**Our Solution:** Academic Decompiler parses paper concepts into structured intermediate representations (IR), synthesizes concrete mathematical implementations, runs them in an isolated evaluation sandbox, and automatically self-heals any runtime failures.

---

## Dependencies

* **`google-genai`**
* **`pydantic`**
* **`pydantic-settings`**
* **`tenacity`**
* **`numpy`**