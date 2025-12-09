# Implementation Plan: Context Windows Lab

## Project Overview

**Assignment**: Lab - Context Windows in Practice (Homework 5)
**Goal**: Build a comprehensive system to run 4 experiments demonstrating context window limitations and management strategies in LLMs
**Target Grade**: 100/100
**Timeline**: 5+ days available
**Status**: Documentation Phase

## Problem Statement

This project addresses the challenge of understanding and managing context windows in Large Language Models. Students will:
1. Demonstrate "Lost in the Middle" phenomenon where information in the middle of context is less accessible
2. Show how context window size affects model accuracy
3. Compare full context vs RAG (Retrieval Augmented Generation) approaches
4. Implement and evaluate context engineering strategies (Select, Compress, Write)

## Experiments Summary

| Experiment | Topic | Tools | Duration | Output |
|------------|-------|-------|----------|--------|
| 1 | Needle in Haystack (Lost in Middle) | Ollama + Python | 15 min | Accuracy by position graph |
| 2 | Context Window Size Impact | Ollama + LangChain | 20 min | Latency vs size graph |
| 3 | RAG Impact | Ollama + ChromaDB | 25 min | Performance comparison |
| 4 | Context Engineering Strategies | LangChain + Memory | 30 min | Strategy performance table |

## User Setup Confirmed

- **Ollama**: Already installed ✓
- **Model**: llama2 (optimal for context experiments)
- **Timeline**: 5+ days (allows for comprehensive implementation and analysis)

## Architecture Design

### High-Level Architecture (C4 - Context Level)

```
┌─────────────┐
│   User      │
│  (Student)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  Context Windows Lab System                         │
│  - Run experiments                                  │
│  - Generate synthetic data                          │
│  - Query LLMs                                       │
│  - Analyze results                                  │
│  - Produce visualizations                           │
└──────────────┬──────────────────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐  ┌──────────────┐
│   Ollama    │  │  ChromaDB    │
│   (Local    │  │  (Vector     │
│    LLM)     │  │   Store)     │
└─────────────┘  └──────────────┘
```

### Building Blocks Design

#### Core Building Blocks

1. **Document Generator** (data_generation/)
   - Input: num_docs, words_per_doc, fact_position
   - Output: List of synthetic documents with embedded facts
   - Setup: Configurable templates, fact library

2. **Context Manager** (context_management/)
   - Input: Documents, strategy (full/rag/compress)
   - Output: Formatted context string
   - Setup: Max tokens, chunking strategy

3. **LLM Interface** (llm/)
   - Input: Context, query
   - Output: Response, metadata (latency, tokens)
   - Setup: Model name, temperature, max_tokens

4. **RAG Components** (rag/)
   - Chunker: Split documents into chunks
   - Embedder: Convert to vectors (Nomic embeddings)
   - Vector Store: ChromaDB interface
   - Retriever: Similarity search

5. **Evaluator** (evaluation/)
   - Input: Response, expected_answer
   - Output: Accuracy score, metrics
   - Setup: Evaluation criteria

6. **Visualizer** (visualization/)
   - Input: Experiment results
   - Output: Graphs, tables
   - Setup: Plot style, output format

7. **Experiment Runner** (experiments/)
   - Input: Experiment config
   - Output: Results, analysis
   - Setup: Number of iterations, parallelization

### Directory Structure

```
context-windows-lab/
├── src/
│   ├── context_windows_lab/
│   │   ├── __init__.py
│   │   ├── data_generation/
│   │   │   ├── __init__.py
│   │   │   ├── document_generator.py
│   │   │   └── synthetic_data.py
│   │   ├── context_management/
│   │   │   ├── __init__.py
│   │   │   ├── context_builder.py
│   │   │   └── strategies.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── ollama_interface.py
│   │   │   └── response_parser.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── chunker.py
│   │   │   ├── embedder.py
│   │   │   ├── vector_store.py
│   │   │   └── retriever.py
│   │   ├── evaluation/
│   │   │   ├── __init__.py
│   │   │   ├── accuracy_evaluator.py
│   │   │   └── metrics.py
│   │   ├── visualization/
│   │   │   ├── __init__.py
│   │   │   ├── plotter.py
│   │   │   └── table_generator.py
│   │   ├── experiments/
│   │   │   ├── __init__.py
│   │   │   ├── base_experiment.py
│   │   │   ├── exp1_needle_haystack.py
│   │   │   ├── exp2_context_size.py
│   │   │   ├── exp3_rag_impact.py
│   │   │   └── exp4_engineering_strategies.py
│   │   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_data_generation/
│   ├── test_context_management/
│   ├── test_llm/
│   ├── test_rag/
│   ├── test_evaluation/
│   └── test_experiments/
├── docs/
│   ├── architecture/
│   │   ├── c4_diagrams.md
│   │   ├── uml_diagrams.md
│   │   └── adrs/
│   │       ├── 001-use-ollama.md
│   │       ├── 002-building-blocks-pattern.md
│   │       ├── 003-chromadb-for-vectors.md
│   │       └── 004-multiprocessing-strategy.md
│   ├── api/
│   │   └── api_documentation.md
│   └── user_guide.md
├── data/
│   ├── raw/
│   └── synthetic/
├── results/
│   ├── experiment_1/
│   ├── experiment_2/
│   ├── experiment_3/
│   └── experiment_4/
├── config/
│   ├── experiments.yaml
│   └── llm_config.yaml
├── assets/
│   └── screenshots/
├── notebooks/
│   └── analysis.ipynb
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
├── IMPLEMENTATION_PLAN.md
├── CLAUDE.md
├── PROJECT_PLAN.md
├── GRADING_CHECKLIST.md
└── REQUIREMENTS.md
```

## Implementation Strategy

### Phase 0: Documentation (CURRENT - Day 1)
**Before any coding begins:**
1. ✅ Create IMPLEMENTATION_PLAN.md
2. Complete REQUIREMENTS.md (PRD) with specific project details
3. Create architecture documentation (C4 diagrams, UML)
4. Create Architecture Decision Records (ADRs)
5. Update PROJECT_PLAN.md with implementation specifics
6. Update CLAUDE.md with session 2 details

### Phase 1: Project Setup (Day 1)
1. Create directory structure
2. Initialize pyproject.toml with dependencies
3. Create .env.example
4. Update .gitignore
5. Set up basic __init__.py files

**Dependencies**:
- ollama
- langchain
- langchain-community
- chromadb
- numpy
- matplotlib
- seaborn
- pytest
- pytest-cov
- python-dotenv
- pyyaml
- tiktoken

### Phase 2: Core Building Blocks (Day 1-2)

**Priority Order**:
1. Document Generator - for creating synthetic test data
2. LLM Interface - for querying Ollama
3. Context Manager - for building context strings
4. Evaluator - for measuring accuracy
5. RAG Components - for Experiment 3
6. Visualizer - for creating graphs

**Multiprocessing Strategy**:
- Use `multiprocessing.Pool` for running multiple experiment iterations in parallel
- CPU-bound: Running evaluations, computing metrics
- Use `ThreadPoolExecutor` for parallel LLM API calls
- I/O-bound: Waiting for Ollama responses

### Phase 3: Experiments Implementation (Day 2-3)

Each experiment module will:
1. Inherit from BaseExperiment class
2. Define specific parameters
3. Implement run() method
4. Return structured results
5. Generate visualizations

**Experiment 1: Needle in Haystack**
- Generate 5 synthetic documents (200 words each)
- Embed critical fact at start/middle/end positions
- Query LLM and measure accuracy by position
- Output: Bar chart showing accuracy degradation in middle

**Experiment 2: Context Size Impact**
- Test with 2, 5, 10, 20, 50 documents
- Measure: tokens_used, latency, accuracy
- Run 3 iterations per size for statistical validity
- Output: Line graphs showing latency and accuracy vs context size

**Experiment 3: RAG Impact**
- Create 20 Hebrew documents on different topics
- Compare:
  - Full context: All documents in context
  - RAG: Retrieve top-3 relevant documents
- Measure: accuracy, latency, tokens_used
- Output: Comparison table and bar chart

**Experiment 4: Context Engineering**
- Simulate 10-step agent interaction
- Implement 3 strategies:
  - SELECT: RAG-based retrieval
  - COMPRESS: Automatic summarization
  - WRITE: External memory (scratchpad)
- Measure performance degradation over steps
- Output: Strategy comparison table

### Phase 4: Testing (Day 3)
- Write unit tests for each building block
- Achieve 70%+ coverage
- Test edge cases:
  - Empty documents
  - Very long contexts
  - Invalid queries
  - Network errors

### Phase 5: Analysis & Documentation (Day 4)

**Jupyter Notebook**:
1. Load results from all experiments
2. Statistical analysis (mean, std, confidence intervals)
3. Visualizations with proper labels
4. Observations and insights
5. Parameter sensitivity analysis

**Documentation**:
1. Complete README with:
   - Installation instructions
   - Usage examples with screenshots
   - Configuration guide
   - Troubleshooting
2. Architecture documentation:
   - C4 diagrams (Context, Container, Component)
   - UML sequence diagrams for complex flows
   - ADRs for key decisions
3. API documentation
4. User guide

### Phase 6: Self-Assessment (Day 4-5)
1. Update GRADING_CHECKLIST.md
2. Complete self-assessment justification (200-500 words)
3. Fill in cost analysis (token usage)
4. Academic integrity declaration
5. Update CLAUDE.md with all prompts used

## Technical Decisions (ADRs)

### ADR-001: Use Ollama for Local LLM
**Decision**: Use Ollama running locally instead of cloud APIs
**Rationale**:
- No API costs
- No rate limits
- Privacy (no data sent to cloud)
- Reproducibility
**Alternatives**: OpenAI API, Anthropic API (rejected due to cost)

### ADR-002: Building Blocks Pattern
**Decision**: Organize code into modular building blocks with clear interfaces
**Rationale**:
- Required by grading criteria (12 points)
- Improves testability
- Enables reusability
- Clear separation of concerns

### ADR-003: ChromaDB for Vector Store
**Decision**: Use ChromaDB for embeddings storage
**Rationale**:
- Lightweight, no separate server needed
- Good Python integration
- Supports Nomic embeddings
- Easy to setup for experiments

### ADR-004: Multiprocessing for Iterations
**Decision**: Use multiprocessing.Pool for running experiment iterations
**Rationale**:
- CPU-bound: Evaluation computations
- Improves experiment runtime
- Demonstrates multiprocessing requirement (12 points)
- Thread safety managed with separate processes

## Configuration Management

### experiments.yaml
```yaml
experiment_1:
  num_documents: 5
  words_per_document: 200
  positions: [start, middle, end]
  iterations: 3

experiment_2:
  document_counts: [2, 5, 10, 20, 50]
  iterations: 3

experiment_3:
  num_documents: 20
  topics: [technology, law, medicine]
  top_k: 3
  chunk_size: 500

experiment_4:
  num_actions: 10
  strategies: [select, compress, write]
  max_tokens: 2000
```

### llm_config.yaml
```yaml
ollama:
  base_url: http://localhost:11434  # Default Ollama endpoint
  model: llama2  # Confirmed available on user's machine
  temperature: 0.0  # Deterministic outputs for reproducibility
  max_tokens: 500
  timeout: 60

embeddings:
  model: nomic-embed-text
  dimension: 768
```

## Success Metrics

### Quantitative
- Test coverage: ≥70%
- All 4 experiments completed successfully
- Statistical significance (3+ iterations per condition)
- All visualizations generated
- Documentation completeness: 100%

### Qualitative
- Clear, insightful analysis in Jupyter notebook
- Professional visualizations with proper labels
- Comprehensive README
- Well-architected, modular code
- Thorough self-assessment

## Risk Mitigation

### Risk 1: Ollama connectivity
**Mitigation**: Check Ollama availability at startup, provide clear error messages

### Risk 2: Long experiment runtime
**Mitigation**: Use multiprocessing, provide progress bars, allow resuming

### Risk 3: Non-deterministic LLM outputs
**Mitigation**: Set temperature=0.0, run multiple iterations, report mean/std

### Risk 4: Memory issues with large contexts
**Mitigation**: Stream responses, chunk processing, garbage collection

## Critical Files to Create

### Priority 1 (Documentation - CURRENT PHASE)
1. ✅ `IMPLEMENTATION_PLAN.md` - This file
2. `REQUIREMENTS.md` - Complete PRD
3. `docs/architecture/c4_diagrams.md` - Architecture diagrams
4. `docs/architecture/uml_diagrams.md` - UML diagrams
5. `docs/architecture/adrs/001-use-ollama.md` - ADR 1
6. `docs/architecture/adrs/002-building-blocks-pattern.md` - ADR 2
7. `docs/architecture/adrs/003-chromadb-for-vectors.md` - ADR 3
8. `docs/architecture/adrs/004-multiprocessing-strategy.md` - ADR 4

### Priority 2 (Core functionality)
9. `pyproject.toml` - Package definition
10. `src/context_windows_lab/__init__.py` - Package initialization
11. `src/context_windows_lab/llm/ollama_interface.py` - LLM queries
12. `src/context_windows_lab/data_generation/document_generator.py` - Synthetic data
13. `src/context_windows_lab/experiments/base_experiment.py` - Base class

### Priority 3 (Experiments)
14. `src/context_windows_lab/experiments/exp1_needle_haystack.py`
15. `src/context_windows_lab/experiments/exp2_context_size.py`
16. `src/context_windows_lab/experiments/exp3_rag_impact.py`
17. `src/context_windows_lab/experiments/exp4_engineering_strategies.py`

### Priority 4 (Analysis & Documentation)
18. `notebooks/analysis.ipynb` - Statistical analysis
19. `README.md` - Complete user guide
20. `docs/api/api_documentation.md` - API reference

## Grading Alignment

This plan addresses all 100 points:

**Part I: Academic (60 points)**
- Project Documentation (20): PRD updated, architecture docs, ADRs
- README & Code Documentation (15): Comprehensive README, docstrings
- Project Structure & Code Quality (15): Modular structure, <150 lines per file
- Configuration & Security (10): .env files, YAML configs
- Testing & QA (15): 70%+ coverage, edge cases
- Research & Analysis (15): Jupyter notebook, graphs, parameter analysis
- UI/UX & Extensibility (10): CLI interface, clear workflow, extensible design

**Part II: Technical (40 points)**
- Package Organization (16): pyproject.toml, __init__.py, proper structure
- Multiprocessing & Multithreading (12): Pool for iterations, threads for I/O
- Building Blocks Design (12): 7 clear building blocks with defined interfaces

## Additional Enhancements (Given 5+ Day Timeline)

With the extended timeline, we can add:

1. **Enhanced Analysis**
   - Parameter sensitivity analysis for each experiment
   - Statistical significance testing (t-tests, ANOVA)
   - Confidence intervals on all metrics
   - Additional visualization types (heatmaps, violin plots)

2. **Extended Documentation**
   - Video walkthrough or GIF demos
   - Detailed troubleshooting guide
   - Performance optimization tips
   - Architecture decision explanations

3. **Code Quality**
   - Aim for 80%+ test coverage
   - Add integration tests
   - Add type hints throughout
   - Implement logging framework

4. **Extra Experiment Variations**
   - Test with different LLM models (if available)
   - Additional context sizes beyond 50 documents
   - Alternative RAG strategies (e.g., MMR, diversity search)
   - Hybrid context engineering strategies

5. **Reproducibility**
   - Docker container for consistent environment
   - Seed management for reproducible results
   - Detailed requirements.txt with pinned versions
   - Results caching mechanism

---

**Estimated Total Time**: 4-5 days (with 5+ days available, we can exceed expectations)
**Lines of Code**: ~2000-2500
**Test Coverage Target**: 75%+
**Current Phase**: Documentation (Phase 0)
**Next Phase**: Project Setup (Phase 1)
