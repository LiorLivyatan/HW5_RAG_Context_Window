# Product Requirements Document (PRD)

## Document Status
- **Version:** 1.0 (Final)
- **Last Updated:** 2025-12-09
- **Status:** Approved - Ready for Implementation

---

## Executive Summary

### Project Name
**Context Windows Lab** - Experimental Framework for LLM Context Management

### Purpose
Build a comprehensive experimental system to investigate, demonstrate, and analyze context window limitations and management strategies in Large Language Models (LLMs). This system will conduct 4 controlled experiments to provide empirical evidence of the "Lost in the Middle" phenomenon, context size impact, RAG effectiveness, and context engineering strategies.

### Target Users
- Computer Science students learning about LLMs
- Researchers investigating context window behavior
- ML Engineers optimizing LLM applications
- Developers implementing RAG systems

### Success Criteria
- All 4 experiments successfully completed with statistical significance (3+ iterations)
- Clear visualizations demonstrating each phenomenon
- Comprehensive analysis with actionable insights
- Test coverage ≥70%
- Complete documentation (architecture, API, user guide)
- Project grade: 100/100

---

## 1. Problem Statement

### User Problem
LLM developers and researchers face critical challenges in understanding and managing context windows:
- **Lost in the Middle**: Information embedded in the middle of long contexts is less accessible to LLMs
- **Context Accumulation**: As conversations grow, maintaining relevant information becomes difficult
- **Performance Degradation**: Larger contexts lead to increased latency and decreased accuracy
- **Lack of Empirical Evidence**: Limited experimental frameworks to demonstrate these phenomena

### Current State
Currently, developers learn about context window limitations through:
- Anecdotal evidence and blog posts
- Trial and error in production systems
- Academic papers with limited reproducible code
- No standardized experimental framework for comparison

This leads to:
- Inefficient context management strategies
- Suboptimal RAG implementations
- Unexpected behavior in production
- Difficulty teaching these concepts

### Proposed Solution
Build a comprehensive experimental framework that:
1. Systematically demonstrates context window phenomena through controlled experiments
2. Provides quantitative evidence with statistical significance
3. Compares different context management strategies (Full, RAG, Compress, etc.)
4. Generates clear visualizations for understanding
5. Offers reusable, modular components for extending experiments
6. Serves as an educational tool for learning LLM context management

---

## 2. Market Analysis

### Target Audience
**Primary Users:**
- MSc Computer Science students taking LLM courses
- Academic researchers studying context window behavior
- ML Engineers building production LLM applications

**Secondary Users:**
- Technical educators teaching LLM concepts
- Product managers understanding LLM limitations
- Software architects designing LLM-powered systems

**User Characteristics:**
- Comfortable with Python programming
- Basic understanding of LLMs and NLP concepts
- Interest in experimental/empirical approaches
- Need for quantitative evidence to support design decisions

### Stakeholders
1. **Students**: Need clear demonstrations of theoretical concepts
2. **Instructors**: Require reproducible experiments for teaching
3. **Researchers**: Want extensible framework for further investigation
4. **Industry Practitioners**: Need practical insights for system design

### Competitive Landscape
**Existing Solutions:**
1. **LangChain Documentation**: Provides code examples but limited systematic experiments
2. **Academic Papers** (e.g., "Lost in the Middle" paper): Present findings but with limited reproducible code
3. **Blog Posts**: Anecdotal evidence without statistical rigor
4. **LLM Benchmarks** (MMLU, HumanEval): Focus on capabilities, not context management

**Our Differentiators:**
- Comprehensive 4-experiment suite covering multiple phenomena
- Statistical rigor with multiple iterations
- Modular, extensible architecture
- Local execution (no API costs)
- Complete documentation and educational focus
- Reproducible with consistent results

---

## 3. Goals & Objectives

### Strategic Goals
1. **Educational Excellence**: Create a definitive educational resource for understanding LLM context window behavior
2. **Scientific Rigor**: Produce statistically significant experimental results that can be cited and reproduced
3. **Practical Utility**: Provide actionable insights for developers building LLM-powered applications
4. **Technical Excellence**: Demonstrate software engineering best practices (testing, documentation, modularity)
5. **Academic Achievement**: Score 100/100 on all grading criteria

### Key Performance Indicators (KPIs)
| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Experiment Completion | 4/4 experiments (100%) | Successful execution with results |
| Statistical Significance | 3+ iterations per condition | Multiple runs with mean/std reported |
| Test Coverage | ≥70% (target 75%+) | pytest-cov reports |
| Documentation Completeness | 100% | All required docs present |
| Code Quality | <150 lines per file | File length analysis |
| Visualization Quality | 4+ publication-quality graphs | Visual inspection |
| API Response Time | <5 seconds per query | Latency measurements |
| Package Installation | Success on fresh system | Installation testing |
| Reproducibility | Consistent results across runs | Seed management + deterministic settings |
| Academic Grade | 100/100 points | Self-assessment checklist |

---

## 4. Functional Requirements

### Core Features

1. **Experiment 1: Needle in Haystack (Lost in the Middle)**
   - **Description**: Generate synthetic documents with embedded critical facts at different positions (start/middle/end) and measure LLM accuracy by position
   - **User Story**: As a researcher, I want to empirically demonstrate that LLMs have reduced accuracy for information in the middle of contexts, so I can validate the "Lost in the Middle" hypothesis
   - **Acceptance Criteria**:
     - Generate 5 synthetic documents (200 words each)
     - Embed one critical fact per document at specified position
     - Query LLM with 3+ iterations for statistical significance
     - Produce bar chart showing accuracy by position
     - Report mean accuracy and standard deviation
     - Demonstrate accuracy drop in middle position

2. **Experiment 2: Context Window Size Impact**
   - **Description**: Test LLM performance across varying context sizes (2, 5, 10, 20, 50 documents) measuring accuracy, latency, and token usage
   - **User Story**: As an ML engineer, I want to understand how context size affects model performance, so I can optimize my application's context management
   - **Acceptance Criteria**:
     - Test with 5 different document counts: 2, 5, 10, 20, 50
     - Measure latency (seconds), accuracy (%), tokens_used for each size
     - Run 3+ iterations per size
     - Generate line graphs: accuracy vs size, latency vs size
     - Report correlation between size and performance degradation

3. **Experiment 3: RAG vs Full Context Comparison**
   - **Description**: Compare retrieval-augmented generation (RAG) with full context loading, measuring accuracy, speed, and token efficiency
   - **User Story**: As a developer, I want quantitative evidence of RAG benefits vs full context, so I can justify RAG implementation
   - **Acceptance Criteria**:
     - Create 20 Hebrew documents across 3 topics (technology, law, medicine)
     - Implement chunking, embedding (Nomic), and vector storage (ChromaDB)
     - Compare full context (all 20 docs) vs RAG (top-3 retrieval)
     - Measure accuracy, latency, tokens_used for both approaches
     - Generate comparison table and bar chart
     - Demonstrate RAG advantage in speed and accuracy

4. **Experiment 4: Context Engineering Strategies**
   - **Description**: Simulate multi-step agent interactions and compare 3 context management strategies: SELECT (RAG), COMPRESS (summarization), WRITE (external memory)
   - **User Story**: As an architect, I want to evaluate different context engineering approaches, so I can choose the optimal strategy for my use case
   - **Acceptance Criteria**:
     - Simulate 10 sequential agent actions with growing context
     - Implement 3 strategies: SELECT, COMPRESS, WRITE
     - Measure accuracy degradation across 10 steps for each strategy
     - Generate strategy performance comparison table
     - Identify best-performing strategy under different conditions

5. **Document Generation System**
   - **Description**: Modular system for generating synthetic test documents with configurable parameters
   - **User Story**: As an experimenter, I want to generate realistic synthetic data, so I can run controlled experiments
   - **Acceptance Criteria**:
     - Generate documents with specified word count
     - Embed facts at configurable positions
     - Support multiple topics and languages
     - Provide templates for consistent generation
     - Validate generated documents meet specifications

6. **LLM Query Interface**
   - **Description**: Unified interface for querying Ollama with monitoring and error handling
   - **User Story**: As a developer, I want a reliable LLM interface, so I don't have to worry about connection issues
   - **Acceptance Criteria**:
     - Connect to Ollama API (localhost:11434)
     - Support configurable parameters (temperature, max_tokens)
     - Measure and return latency, token count
     - Handle errors gracefully with retries
     - Validate Ollama availability at startup

7. **Evaluation System**
   - **Description**: Automated evaluation of LLM responses against expected answers
   - **User Story**: As a researcher, I want objective accuracy measurements, so my results are scientifically valid
   - **Acceptance Criteria**:
     - Compare LLM response to expected answer
     - Calculate accuracy score (0-1 or percentage)
     - Support multiple evaluation methods (exact match, semantic similarity)
     - Generate aggregate statistics (mean, std, confidence intervals)
     - Handle edge cases (empty responses, timeouts)

8. **Visualization System**
   - **Description**: Generate publication-quality graphs and tables from experiment results
   - **User Story**: As a student, I want clear visualizations, so I can understand the phenomena easily
   - **Acceptance Criteria**:
     - Generate bar charts, line graphs, comparison tables
     - Include proper labels, legends, titles
     - Export high-resolution images (300 DPI)
     - Support multiple output formats (PNG, PDF)
     - Follow consistent style guidelines

### User Stories
*As a [type of user], I want [goal] so that [benefit]*

1. As a **student**, I want to run all 4 experiments with a single command, so that I can quickly generate results for my assignment
2. As a **researcher**, I want to adjust experiment parameters via config files, so that I can test different hypotheses without modifying code
3. As a **developer**, I want comprehensive API documentation, so that I can extend the framework with custom experiments
4. As an **educator**, I want clear visualizations and analysis notebooks, so that I can teach context window concepts effectively
5. As a **practitioner**, I want to understand which context strategy works best, so that I can apply it in my production system

### Use Cases
*Detailed scenarios of system usage*

#### Use Case 1: Running Complete Experiment Suite
- **Actor:** MSc Student submitting homework
- **Preconditions:**
  - Python 3.9+ installed
  - Ollama running locally with llama2 model
  - Project dependencies installed (pip install -e .)
- **Main Flow:**
  1. User runs `python -m context_windows_lab.cli --run-all`
  2. System validates Ollama connection
  3. System runs Experiment 1 (Needle in Haystack) with 3 iterations
  4. System generates and saves bar chart to results/experiment_1/
  5. System runs Experiment 2 (Context Size) with 3 iterations per size
  6. System generates and saves line graphs to results/experiment_2/
  7. System runs Experiment 3 (RAG) with full and RAG modes
  8. System generates and saves comparison table to results/experiment_3/
  9. System runs Experiment 4 (Strategies) across 10 steps
  10. System generates and saves strategy table to results/experiment_4/
  11. System prints summary statistics
- **Alternative Flows:**
  - If Ollama is not running: Display error message with connection instructions
  - If experiment fails: Save partial results and continue with remaining experiments
  - User can run individual experiments: `--experiment 1`
- **Postconditions:**
  - All experiment results saved in results/ directory
  - Visualizations generated and saved
  - Summary statistics logged to console and file

---

## 5. Non-Functional Requirements

### Performance
- **Response time**: LLM queries should complete within 5 seconds (excluding model inference time)
- **Throughput**: System should handle 100+ experiment iterations without memory leaks
- **Scalability**: Support multiprocessing for parallel experiment execution (utilize all available CPU cores)
- **Efficiency**: Minimize redundant LLM calls through caching where appropriate

### Reliability
- **Availability**: System should gracefully handle Ollama downtime with clear error messages
- **Error rate tolerance**: <5% failure rate across experiment iterations
- **Recovery procedures**:
  - Automatic retry on transient failures (3 attempts with exponential backoff)
  - Save intermediate results to allow resume on crash
  - Validate all inputs before expensive operations
- **Reproducibility**: Consistent results across runs (seed management + temperature=0.0)

### Security
- **Authentication**: None required (local execution only)
- **Authorization**: None required (single-user system)
- **Data protection**:
  - No sensitive data collected or stored
  - All synthetic data generated locally
  - No external API calls (except to local Ollama)
- **Sensitive information handling**:
  - No hardcoded secrets in code
  - Use .env for any future external API keys
  - .gitignore configured to exclude .env files

### Usability
- **User interface**:
  - Clear CLI with help messages and progress bars
  - Intuitive command structure: `--run-all`, `--experiment N`, `--config PATH`
  - Color-coded output (errors in red, success in green)
- **Accessibility**:
  - Text-based output readable by screen readers
  - Visualizations include alt-text descriptions
  - Documentation in English (code) and support for Hebrew (experiment data)
- **Documentation requirements**:
  - Complete README with quick start guide
  - Inline code documentation (docstrings for all public functions)
  - Architecture diagrams (C4 Model)
  - API reference documentation
  - Jupyter notebook with analysis examples

### Maintainability
- **Code quality standards**:
  - PEP 8 compliance
  - Maximum 150 lines per file
  - Single Responsibility Principle (SRP)
  - DRY (Don't Repeat Yourself)
  - Clear separation of concerns
- **Testing requirements**:
  - Minimum 70% test coverage (target 75%+)
  - Unit tests for all building blocks
  - Integration tests for end-to-end flows
  - Edge case testing (empty inputs, timeouts, errors)
- **Documentation standards**:
  - Docstrings for all modules, classes, functions
  - Google-style docstring format
  - Type hints for function signatures
  - Inline comments for complex logic only

### Compatibility
- **Python version**: 3.9+ (for typing features and modern syntax)
- **Operating systems**:
  - macOS (primary development environment)
  - Linux (Ubuntu 20.04+)
  - Windows (with WSL2 recommended)
- **Dependencies**:
  - Ollama (local LLM server)
  - Core Python libraries: ollama, langchain, chromadb, numpy, matplotlib
  - No cloud dependencies
  - All dependencies specified in pyproject.toml with version constraints

---

## 6. Constraints & Assumptions

### Technical Constraints
- **Local Execution Only**: System must run entirely on local machine (no cloud dependencies)
- **Ollama Requirement**: User must have Ollama installed and running
- **Model Availability**: llama2 model must be downloaded in Ollama
- **Memory**: System must fit within typical laptop RAM (8-16GB)
- **Python Version**: Requires Python 3.9+ (no support for older versions)
- **Processing Time**: Full experiment suite may take 60-90 minutes to complete

### Business Constraints
- **Timeline**: Must be completed within course deadline (5+ days available)
- **Budget**: Zero cost (no cloud API usage)
- **Solo Development**: Single developer (with AI assistance)
- **Academic Requirements**: Must meet all 100 grading criteria

### Assumptions
- User has basic Python knowledge
- User can follow installation instructions
- Ollama service is stable and available locally
- LLM responses are reasonably consistent (temperature=0.0)
- Generated synthetic data is sufficient for demonstrating phenomena
- Hebrew language support in llama2 is adequate for Experiment 3
- User has sufficient disk space for results and visualizations (~100MB)

---

## 7. Dependencies

### External Dependencies
| Dependency | Purpose | Version | Critical? |
|-----------|---------|---------|-----------|
| Python | Runtime environment | 3.9+ | Yes |
| Ollama | Local LLM server | Latest | Yes |
| ollama-python | Python client for Ollama | ^0.1.0 | Yes |
| langchain | LLM application framework | ^0.1.0 | Yes |
| langchain-community | Community integrations | ^0.0.1 | Yes |
| chromadb | Vector database | ^0.4.0 | Yes (Exp 3) |
| numpy | Numerical computations | ^1.24.0 | Yes |
| matplotlib | Plotting library | ^3.7.0 | Yes |
| seaborn | Statistical visualization | ^0.12.0 | Yes |
| pytest | Testing framework | ^7.4.0 | Yes |
| pytest-cov | Coverage reporting | ^4.1.0 | Yes |
| python-dotenv | Environment variables | ^1.0.0 | Yes |
| pyyaml | YAML configuration | ^6.0.0 | Yes |
| tiktoken | Token counting | ^0.5.0 | Yes |

### Internal Dependencies
- All experiments depend on: Document Generator, LLM Interface, Evaluator, Visualizer
- Experiment 3 additionally depends on: RAG Components (Chunker, Embedder, Vector Store)
- Experiment 4 additionally depends on: Context Management Strategies
- CLI depends on: All experiments, Configuration Manager
- Tests depend on: All src modules

---

## 8. Timeline & Milestones

### Development Phases
| Phase | Description | Duration | Key Deliverables |
|-------|-------------|----------|-----------------|
| Planning | Requirements & Design | Day 1 | PRD, Architecture docs, ADRs |
| Setup | Project structure & deps | Day 1 | pyproject.toml, directory structure, configs |
| Development | Core implementation | Day 1-3 | All building blocks + 4 experiments |
| Testing | QA & validation | Day 3 | Test suite with 70%+ coverage |
| Analysis | Results & visualization | Day 4 | Jupyter notebook, graphs, insights |
| Documentation | Final docs & polish | Day 4-5 | README, API docs, user guide |
| Self-Assessment | Grading & submission | Day 5 | Completed checklist, justification |

### Key Milestones
- [x] Milestone 1: Project concept approved (Context Windows Lab)
- [x] Milestone 2: Architecture designed (Building blocks pattern)
- [ ] Milestone 3: Core building blocks implemented
- [ ] Milestone 4: All 4 experiments completed
- [ ] Milestone 5: Testing complete (70%+ coverage)
- [ ] Milestone 6: Analysis notebook with visualizations complete
- [ ] Milestone 7: Documentation complete
- [ ] Milestone 8: Self-assessment complete
- [ ] Milestone 9: Final submission ready

---

## 9. Technical Architecture (Overview)

### System Components
*High-level component breakdown*
1. **Presentation Layer**: CLI interface for user interaction
2. **Experiment Layer**: 4 experiment modules (Exp1-4)
3. **Core Services Layer**: Building blocks (Document Gen, LLM Interface, Evaluator, Visualizer)
4. **RAG Layer**: Chunking, Embedding, Vector Store, Retrieval (for Exp 3)
5. **Infrastructure Layer**: Configuration management, logging, multiprocessing
6. **External Services**: Ollama API (local), ChromaDB (embedded)

### Technology Stack
*Core technologies to be used*
- **Language**: Python 3.9+
- **LLM Server**: Ollama (llama2 model)
- **LLM Framework**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Nomic Embed Text
- **Visualization**: Matplotlib + Seaborn
- **Testing**: pytest + pytest-cov
- **Configuration**: YAML files + python-dotenv
- **Parallelization**: multiprocessing.Pool + concurrent.futures.ThreadPoolExecutor

### Building Blocks
*Main system building blocks (See IMPLEMENTATION_PLAN.md for details)*
1. **Document Generator** - Synthetic data creation
2. **Context Manager** - Context string formatting
3. **LLM Interface** - Ollama API client
4. **RAG Components** - Chunker, Embedder, Vector Store, Retriever
5. **Evaluator** - Accuracy measurement
6. **Visualizer** - Graph and table generation
7. **Experiment Runner** - Orchestration and iteration management

### Integration Points
*How components interact*
- **CLI → Experiments**: Command-line invokes specific experiments
- **Experiments → Building Blocks**: All experiments use Document Generator, LLM Interface, Evaluator, Visualizer
- **LLM Interface → Ollama**: HTTP API calls to localhost:11434
- **RAG Components → ChromaDB**: Embedded vector database
- **Experiments → Results Files**: JSON/CSV output + PNG visualizations
- **Multiprocessing**: Pool distributes experiment iterations across CPU cores
- **Configuration**: YAML files loaded at startup for all parameters

*For detailed architecture diagrams, see docs/architecture/c4_diagrams.md*

---

## 10. Acceptance Criteria

### Functional Acceptance
- [ ] All core features implemented
- [ ] All user stories satisfied
- [ ] All use cases functional

### Technical Acceptance
- [ ] Code quality standards met
- [ ] Test coverage ≥ 70%
- [ ] Performance benchmarks met
- [ ] Security requirements satisfied

### Documentation Acceptance
- [ ] Complete README
- [ ] Architecture documentation
- [ ] API documentation
- [ ] User guide

---

## 11. Out of Scope

*Features explicitly NOT included in this version*
-

---

## 12. Future Enhancements

*Potential future additions*
1.
2.
3.

---

## Appendices

### A. Glossary
*Key terms and definitions*

### B. References
*Related documents and resources*
- Self-Assessment Guide v2.0
- Software Submission Guidelines v2.0

---

## Approval & Sign-off

- [ ] Requirements reviewed and approved
- [ ] Architecture aligned with requirements
- [ ] All stakeholders informed

**Reviewed by:** ________________
**Date:** ________________

---

*This PRD will be updated as requirements are refined and the project evolves.*
