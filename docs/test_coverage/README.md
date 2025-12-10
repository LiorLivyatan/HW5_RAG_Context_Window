# Test Coverage Report

**Last Run:** Wed Dec 10 22:08:16 IST 2025
**Total Coverage:** 78.46%
**Tests Passed:** 231/231

## Coverage by Module

### 🧪 Experiments
Located in `src/context_windows_lab/experiments/`.
This suite tests the core scientific experiments (Needle in Haystack, Context Size, RAG Impact, Strategies). All experiments are tested end-to-end with mock LLMs to ensure reproducibility and correctness of the logic.

### 📄 Data Generation
Located in `src/context_windows_lab/data_generation/`.
Tests the creation of synthetic documents, ensuring facts are embedded correctly at specific positions (start, middle, end). Validates edge cases like empty inputs, random seeds, and large document counts.

### 📊 Evaluation & Metrics
Located in `src/context_windows_lab/evaluation/`.
Validates the accuracy of scoring mechanisms (Exact Match, Contains) and statistical functions (Mean, Std Dev, Confidence Intervals). High coverage here is critical for the scientific validity of experimental results.

### 🔍 RAG & Vector Store
Located in `src/context_windows_lab/rag/`.
Tests the integration with ChromaDB and vector retrieval logic. Includes handling of metadata, embedding generation, top-k retrieval efficiency, and fallback mechanisms.

### 🤖 LLM Interface
Located in `src/context_windows_lab/llm/`.
Tests the Ollama API wrapper. Coverage is lower because it relies on external services, but core request/response parsing, error handling, and retry logic are fully tested via mocks.

### 📈 Visualization
Located in `src/context_windows_lab/visualization/`.
Tests the plotting logic using Matplotlib. Focuses on ensuring file outputs are created and arguments are passed correctly, as visual rendering is verified manually.

## Accessing the Full Report
The complete interactive HTML report is available locally:
```bash
open htmlcov/index.html
```
