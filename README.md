# Context Windows Lab

**Experimental Framework for LLM Context Management**

A comprehensive system for investigating context window behavior in Large Language Models, including the "Lost in the Middle" phenomenon, context size impact, RAG effectiveness, and context engineering strategies.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Experiments](#experiments)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

---

## Overview

This project provides a modular, extensible framework for conducting controlled experiments on LLM context window behavior. It addresses two critical phenomena:

1. **Lost in the Middle**: Information embedded in the middle of long contexts is less accessible to LLMs
2. **Context Accumulation**: As conversations grow, maintaining relevant information becomes challenging

### Key Objectives

- Empirically demonstrate context window limitations
- Compare retrieval strategies (full context vs RAG)
- Evaluate context engineering techniques
- Provide reproducible, statistically significant results

---

## Features

- **4 Comprehensive Experiments**
  - Experiment 1: Needle in Haystack (Lost in the Middle)
  - Experiment 2: Context Window Size Impact
  - Experiment 3: RAG vs Full Context Comparison
  - Experiment 4: Context Engineering Strategies

- **Modular Architecture**
  - 7 reusable building blocks
  - Clean separation of concerns
  - Dependency injection for flexibility

- **Local Execution**
  - No cloud dependencies
  - Zero API costs
  - Full privacy (data stays local)

- **Statistical Rigor**
  - Multiple iterations for significance
  - Confidence intervals
  - Comprehensive metrics

- **Publication-Quality Visualizations**
  - Bar charts, line graphs
  - Error bars and confidence intervals
  - 300 DPI output

---

## Installation

### Prerequisites

- **Python 3.9+**
- **Ollama** (local LLM server)

### Step 1: Install Ollama

```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/

# Pull the llama2 model
ollama pull llama2

# Start Ollama server
ollama serve
```

### Step 2: Clone Repository

```bash
git clone https://github.com/LiorLivyatan/HW5_RAG_Context_Window.git
cd HW5_RAG_Context_Window
```

### Step 3: Install Package

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dependencies
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"

# Or install everything (dev + jupyter)
pip install -e ".[all]"
```

### Step 4: Verify Installation

```bash
# Check if Ollama is available
context-windows-lab --check-ollama

# Should output: ✓ Ollama is available and responding
```

---

## Quick Start

### Run Experiment 1 (Needle in Haystack)

```bash
# Run Experiment 1 with default settings (3 iterations)
context-windows-lab --experiment 1

# With custom iterations and output directory
context-windows-lab --experiment 1 --iterations 5 --output-dir ./my_results

# Verbose output for debugging
context-windows-lab --experiment 1 --verbose
```

### Run All Experiments

```bash
context-windows-lab --run-all
```

### View Results

Results are saved to `results/experiment_N/`:
- `results.json` - Raw data and statistics
- `accuracy_by_position.png` - Visualization

---

## Experiments

### Experiment 1: Needle in Haystack

**Objective**: Demonstrate "Lost in the Middle" phenomenon

**Method**:
- Generate 5 documents (200 words each)
- Embed critical fact at start/middle/end
- Query LLM for each document
- Measure accuracy by position

**Expected Result**: Accuracy drops when fact is in middle

**Usage**:
```bash
context-windows-lab --experiment 1
```

### Experiment 2: Context Window Size Impact

**Status**: Planned (not yet implemented)

**Objective**: Measure performance degradation with increasing context size

**Method**:
- Test with 2, 5, 10, 20, 50 documents
- Measure accuracy, latency, tokens used

### Experiment 3: RAG Impact

**Status**: Planned (not yet implemented)

**Objective**: Compare RAG with full context loading

**Method**:
- Create 20 Hebrew documents
- Compare full context vs top-3 retrieval
- Measure accuracy, speed, token efficiency

### Experiment 4: Context Engineering Strategies

**Status**: Planned (not yet implemented)

**Objective**: Evaluate context management strategies

**Method**:
- Simulate 10-step agent interaction
- Compare SELECT, COMPRESS, WRITE strategies
- Measure performance over time

---

## Project Structure

```
context-windows-lab/
├── src/context_windows_lab/       # Main package
│   ├── data_generation/           # Synthetic data generation
│   ├── context_management/        # Context building strategies
│   ├── llm/                       # Ollama interface
│   ├── rag/                       # RAG components
│   ├── evaluation/                # Accuracy measurement
│   ├── visualization/             # Plotting
│   ├── experiments/               # 4 experiments
│   └── cli.py                     # Command-line interface
├── tests/                         # Test suite
├── docs/                          # Documentation
│   └── architecture/              # Architecture docs
│       ├── c4_diagrams.md
│       ├── uml_diagrams.md
│       └── adrs/                  # Decision records
├── config/                        # Configuration files
│   ├── llm_config.yaml
│   └── experiments.yaml
├── results/                       # Experiment outputs
├── pyproject.toml                 # Package definition
└── README.md                      # This file
```

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TEMPERATURE=0.0

# Parallelization
USE_MULTIPROCESSING=true
MAX_PROCESSES=4

# Logging
LOG_LEVEL=INFO
```

### Experiment Configuration

Edit `config/experiments.yaml` to customize experiment parameters:

```yaml
experiment_1:
  num_documents: 5
  words_per_document: 200
  fact: "The CEO of the company is David Cohen."
  question: "Who is the CEO of the company?"
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=context_windows_lab --cov-report=html

# Run specific test file
pytest tests/test_data_generation/test_document_generator.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
pylint src/
```

### Adding a New Experiment

1. Create file: `src/context_windows_lab/experiments/expN_name.py`
2. Inherit from `BaseExperiment`
3. Implement required methods:
   - `_generate_data()`
   - `_execute_queries()`
   - `_evaluate_responses()`
   - `analyze()`
   - `visualize()`
4. Add to CLI in `cli.py`
5. Write tests in `tests/test_experiments/`

---

## Documentation

- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Complete project roadmap
- **[Requirements (PRD)](REQUIREMENTS.md)** - Product requirements
- **[Architecture (C4)](docs/architecture/c4_diagrams.md)** - System architecture
- **[UML Diagrams](docs/architecture/uml_diagrams.md)** - Detailed design
- **[ADRs](docs/architecture/adrs/)** - Architecture decisions

---

## Building Blocks

The system is built on 7 modular building blocks:

1. **Document Generator** - Create synthetic test documents
2. **Context Manager** - Format context strings
3. **LLM Interface** - Query Ollama with monitoring
4. **RAG Components** - Chunking, embedding, retrieval
5. **Evaluator** - Measure response accuracy
6. **Visualizer** - Generate publication-quality graphs
7. **Experiment Runner** - Orchestrate experiments

Each block has:
- Clear input/output interfaces
- Comprehensive validation
- Single responsibility
- Independent testability

---

## Technology Stack

- **Language**: Python 3.9+
- **LLM**: Ollama (llama2)
- **Vector DB**: ChromaDB
- **Embeddings**: Nomic Embed Text
- **Visualization**: Matplotlib, Seaborn
- **Testing**: pytest, pytest-cov
- **Packaging**: Modern pyproject.toml

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Authors

- **Lior Livyatan** - MSc Computer Science Student
- Built with [Claude Code](https://claude.com/claude-code)

---

## Acknowledgments

- Based on research on context window limitations in LLMs
- Inspired by the "Lost in the Middle" paper
- Part of MSc CS LLM Course (Homework 5)

---

## Support

For issues, questions, or contributions:
- **GitHub Issues**: https://github.com/LiorLivyatan/HW5_RAG_Context_Window/issues
- **Documentation**: See `docs/` directory

---

**Made with 🤖 by Claude Code**
