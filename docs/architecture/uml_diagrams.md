# UML Diagrams

## Overview

This document provides UML (Unified Modeling Language) diagrams for the Context Windows Lab system, focusing on complex processes, class structures, and interaction flows.

---

## Class Diagram

### Core Building Blocks Class Structure

```
┌─────────────────────────────────────┐
│      <<interface>>                  │
│      ExperimentConfig               │
├─────────────────────────────────────┤
│ + num_iterations: int               │
│ + save_results: bool                │
│ + output_dir: Path                  │
└─────────────────────────────────────┘
            △
            │
            │ implements
            │
┌───────────┴─────────────────────────────────────────┐
│                                                       │
┌─────────────────────────┐    ┌──────────────────────────┐
│ Exp1Config              │    │ Exp2Config               │
├─────────────────────────┤    ├──────────────────────────┤
│ + num_documents: int    │    │ + document_counts: List  │
│ + words_per_doc: int    │    │ + iterations: int        │
│ + positions: List[str]  │    └──────────────────────────┘
└─────────────────────────┘

┌──────────────────────────────────────┐
│      BaseExperiment                  │
│      <<abstract>>                    │
├──────────────────────────────────────┤
│ # config: ExperimentConfig           │
│ # results: List[Result]              │
│ # doc_generator: DocumentGenerator   │
│ # llm_interface: OllamaInterface     │
│ # evaluator: AccuracyEvaluator       │
│ # visualizer: Visualizer             │
├──────────────────────────────────────┤
│ + __init__(config, *building_blocks) │
│ + run() -> ExperimentResults         │
│ + analyze() -> Analysis              │
│ + visualize() -> Path                │
│ # _generate_data() -> List[Document] │
│ # _execute_queries() -> List[Response]│
│ # _evaluate_responses() -> List[Score]│
└──────────────────────────────────────┘
            △
            │ inherits
            │
┌───────────┴─────────────┬─────────────────┬──────────────────┐
│                         │                 │                  │
┌─────────────────────┐ ┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
│ NeedleInHaystack    │ │ ContextSize     │ │ RAGImpact    │ │ Engineering  │
│ Experiment          │ │ Experiment      │ │ Experiment   │ │ Strategies   │
├─────────────────────┤ ├─────────────────┤ ├──────────────┤ ├──────────────┤
│ - positions: List   │ │ - sizes: List   │ │ - use_rag:   │ │ - strategies:│
│                     │ │                 │ │   bool       │ │   List[str]  │
├─────────────────────┤ ├─────────────────┤ ├──────────────┤ ├──────────────┤
│ + run()             │ │ + run()         │ │ + run()      │ │ + run()      │
│ + analyze()         │ │ + analyze()     │ │ + analyze()  │ │ + analyze()  │
│ + visualize()       │ │ + visualize()   │ │ + visualize()│ │ + visualize()│
└─────────────────────┘ └─────────────────┘ └──────────────┘ └──────────────┘

┌────────────────────────────────┐
│   DocumentGenerator            │
├────────────────────────────────┤
│ - templates: Dict[str, str]    │
│ - fact_library: List[str]      │
│ - rng: Random                  │
├────────────────────────────────┤
│ + generate_documents(          │
│     num: int,                  │
│     words: int,                │
│     fact: str,                 │
│     position: str              │
│   ) -> List[Document]          │
│ + embed_fact(                  │
│     text: str,                 │
│     fact: str,                 │
│     position: str              │
│   ) -> str                     │
│ - _generate_filler_text(       │
│     words: int                 │
│   ) -> str                     │
└────────────────────────────────┘

┌────────────────────────────────┐
│   OllamaInterface              │
├────────────────────────────────┤
│ - base_url: str                │
│ - model: str                   │
│ - temperature: float           │
│ - max_tokens: int              │
│ - timeout: int                 │
│ - client: httpx.Client         │
├────────────────────────────────┤
│ + query(                       │
│     context: str,              │
│     question: str              │
│   ) -> LLMResponse             │
│ + check_availability() -> bool │
│ + count_tokens(text: str)->int │
│ - _retry_on_failure(           │
│     func: Callable,            │
│     max_retries: int           │
│   ) -> Any                     │
└────────────────────────────────┘

┌────────────────────────────────┐
│   AccuracyEvaluator            │
├────────────────────────────────┤
│ - evaluation_method: str       │
├────────────────────────────────┤
│ + evaluate(                    │
│     response: str,             │
│     expected: str              │
│   ) -> float                   │
│ + calculate_statistics(        │
│     scores: List[float]        │
│   ) -> Statistics              │
│ + exact_match(a: str, b: str)  │
│   -> float                     │
│ + semantic_similarity(         │
│     a: str,                    │
│     b: str                     │
│   ) -> float                   │
└────────────────────────────────┘

┌────────────────────────────────┐
│   Visualizer                   │
├────────────────────────────────┤
│ - style: str                   │
│ - dpi: int                     │
│ - color_palette: List[str]     │
├────────────────────────────────┤
│ + plot_bar_chart(              │
│     data: Dict,                │
│     title: str,                │
│     output: Path               │
│   ) -> Path                    │
│ + plot_line_graph(             │
│     x: List,                   │
│     y: List,                   │
│     output: Path               │
│   ) -> Path                    │
│ + generate_table(              │
│     data: DataFrame,           │
│     output: Path               │
│   ) -> Path                    │
│ - _apply_style() -> None       │
└────────────────────────────────┘

┌────────────────────────────────┐
│   <<dataclass>>                │
│   LLMResponse                  │
├────────────────────────────────┤
│ + text: str                    │
│ + latency_ms: float            │
│ + tokens_used: int             │
│ + model: str                   │
│ + timestamp: datetime          │
└────────────────────────────────┘

┌────────────────────────────────┐
│   <<dataclass>>                │
│   Document                     │
├────────────────────────────────┤
│ + content: str                 │
│ + fact: str                    │
│ + fact_position: str           │
│ + metadata: Dict               │
└────────────────────────────────┘

┌────────────────────────────────┐
│   <<dataclass>>                │
│   ExperimentResults            │
├────────────────────────────────┤
│ + experiment_name: str         │
│ + results: List[Result]        │
│ + statistics: Statistics       │
│ + timestamp: datetime          │
│ + config: ExperimentConfig     │
└────────────────────────────────┘
```

**Relationships:**
- **Inheritance**: All experiments inherit from BaseExperiment (template method pattern)
- **Composition**: BaseExperiment contains building blocks (dependency injection)
- **Association**: Experiments use data classes (Document, LLMResponse, ExperimentResults)

---

## Sequence Diagram: Experiment 1 Execution Flow

```
User      CLI     Exp1Factory  NeedleExp  DocGen   LLM      Evaluator  Visualizer  FileSystem
 │         │           │           │         │       │           │          │           │
 │ run exp1│           │           │         │       │           │          │           │
 ├────────>│           │           │         │       │           │          │           │
 │         │ create    │           │         │       │           │          │           │
 │         ├──────────>│           │         │       │           │          │           │
 │         │           │ new(config)         │       │           │          │           │
 │         │           ├──────────>│         │       │           │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ run()   │       │           │          │           │
 │         │           │           │────┐    │       │           │          │           │
 │         │           │           │    │    │       │           │          │           │
 │         │           │           │<───┘    │       │           │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ generate_documents(5, 200, fact, "start")         │
 │         │           │           ├────────>│       │           │          │           │
 │         │           │           │         │─┐     │           │          │           │
 │         │           │           │         │ │ create docs    │          │           │
 │         │           │           │         │<┘     │           │          │           │
 │         │           │           │<────────┤       │           │          │           │
 │         │           │           │  [docs] │       │           │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ Loop for each document     │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ query(doc, question)       │          │           │
 │         │           │           ├────────────────>│           │          │           │
 │         │           │           │         │       │─┐         │          │           │
 │         │           │           │         │       │ │ POST    │          │           │
 │         │           │           │         │       │ │ to      │          │           │
 │         │           │           │         │       │ │ Ollama  │          │           │
 │         │           │           │         │       │<┘         │          │           │
 │         │           │           │<────────────────┤           │          │           │
 │         │           │           │    LLMResponse  │           │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ evaluate(response, expected)│          │           │
 │         │           │           ├────────────────────────────>│          │           │
 │         │           │           │         │       │           │─┐        │           │
 │         │           │           │         │       │           │ │compare │           │
 │         │           │           │         │       │           │<┘        │           │
 │         │           │           │<────────────────────────────┤          │           │
 │         │           │           │      accuracy_score         │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ [repeat for middle & end positions]    │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ calculate_statistics(scores)│          │           │
 │         │           │           ├────────────────────────────>│          │           │
 │         │           │           │<────────────────────────────┤          │           │
 │         │           │           │      Statistics             │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ visualize(results)          │          │           │
 │         │           │           ├──────────────────────────────────────>│           │
 │         │           │           │         │       │           │          │─┐         │
 │         │           │           │         │       │           │          │ │plot     │
 │         │           │           │         │       │           │          │<┘         │
 │         │           │           │<──────────────────────────────────────┤           │
 │         │           │           │      graph_path             │          │           │
 │         │           │           │         │       │           │          │           │
 │         │           │           │ save_results(results, graph_path)     │           │
 │         │           │           ├────────────────────────────────────────────────────>│
 │         │           │           │         │       │           │          │           │─┐
 │         │           │           │         │       │           │          │           │ │
 │         │           │           │         │       │           │          │           │<┘
 │         │           │           │<────────────────────────────────────────────────────┤
 │         │           │           │         │       │           │          │           │
 │         │<──────────────────────┤         │       │           │          │           │
 │         │   ExperimentResults   │         │       │           │          │           │
 │<────────┤           │           │         │       │           │          │           │
 │ Success │           │           │         │       │           │          │           │
```

**Key Interactions:**
1. User initiates experiment via CLI
2. Factory creates experiment instance with dependencies
3. Experiment orchestrates building blocks in sequence
4. Document Generator creates synthetic data
5. LLM Interface queries Ollama for each document
6. Evaluator measures accuracy of responses
7. Statistics calculated across all positions
8. Visualizer generates bar chart
9. Results saved to file system

---

## Activity Diagram: Multiprocessing Execution Flow

```
                    [Start: Run Experiment with 3 iterations]
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Create multiprocessing.Pool   │
                    │ with cpu_count() workers      │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Prepare 3 experiment configs  │
                    │ (one per iteration)           │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ pool.map(run_single_iteration,│
                    │         [config1, config2,    │
                    │          config3])            │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌──────────────────────┐      ┌──────────────────────┐
        │ Worker Process 1     │      │ Worker Process 2     │
        │                      │      │                      │
        │ Run iteration 1:     │      │ Run iteration 2:     │
        │ - Generate docs      │      │ - Generate docs      │
        │ - Query LLM          │      │ - Query LLM          │
        │ - Evaluate           │      │ - Evaluate           │
        │                      │      │                      │
        └──────────┬───────────┘      └──────────┬───────────┘
                   │                             │
                   │  ┌───────────────────────┐  │
                   │  │ Worker Process 3      │  │
                   │  │                       │  │
                   │  │ Run iteration 3:      │  │
                   │  │ - Generate docs       │  │
                   │  │ - Query LLM           │  │
                   │  │ - Evaluate            │  │
                   │  │                       │  │
                   │  └──────────┬────────────┘  │
                   │             │               │
                   └─────────────┼───────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────┐
                │ Collect results from all workers│
                │ [results1, results2, results3]  │
                └────────────────┬────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────┐
                │ Aggregate statistics:           │
                │ - Calculate mean accuracy       │
                │ - Calculate std deviation       │
                │ - Calculate confidence intervals│
                └────────────────┬────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────┐
                │ Generate visualization with     │
                │ error bars (std)                │
                └────────────────┬────────────────┘
                                 │
                                 ▼
                          [End: Results Ready]
```

**Parallelization Strategy:**
- **CPU-bound operations**: Experiment iterations run in parallel across multiple processes
- **I/O-bound operations**: LLM queries within each iteration can use threading
- **Data independence**: Each iteration is independent, no shared state
- **Result aggregation**: Main process collects and aggregates results after all workers complete

---

## State Diagram: Experiment Execution States

```
                    [Initial]
                        │
                        ▼
                ┌──────────────┐
                │ Configuring  │
                └──────┬───────┘
                       │ config loaded
                       ▼
                ┌──────────────┐
                │  Generating  │◄─────┐
                │    Data      │      │
                └──────┬───────┘      │
                       │ data ready    │
                       ▼               │
                ┌──────────────┐      │
                │  Executing   │      │
                │   Queries    │      │ retry
                └──────┬───────┘      │
                       │              │
                       │ LLM error    │
                       ├──────────────┘
                       │ all queries done
                       ▼
                ┌──────────────┐
                │  Evaluating  │
                │  Responses   │
                └──────┬───────┘
                       │ evaluation done
                       ▼
                ┌──────────────┐
                │ Analyzing    │
                │ Statistics   │
                └──────┬───────┘
                       │ analysis done
                       ▼
                ┌──────────────┐
                │ Visualizing  │
                │   Results    │
                └──────┬───────┘
                       │ visualization done
                       ▼
                ┌──────────────┐
                │   Saving     │
                │   Results    │
                └──────┬───────┘
                       │
                       ▼
                  [Completed]
                       │
                       │ critical error
                       ▼
                   [Failed]
```

**State Transitions:**
- Normal flow: Configuring → Generating → Executing → Evaluating → Analyzing → Visualizing → Saving → Completed
- Error handling: Executing can retry on transient errors (up to 3 attempts)
- Failure state: Any critical error leads to Failed state with partial results saved

---

## Use Case Diagram

```
                                Context Windows Lab System
    ┌────────────────────────────────────────────────────────────┐
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             Run All Experiments                      │  │
    │  └─────────────────────────────────────────────────────┘  │
    │           │                                                 │
    │           │ <<includes>>                                    │
    │           ▼                                                 │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             Run Single Experiment                    │  │
    │  └─────────────────────────────────────────────────────┘  │
    │           │                                                 │
    │           │ <<includes>>                                    │
    │           ▼                                                 │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             Load Configuration                       │  │
    │  └─────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             View Results                             │  │
    │  └─────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             Analyze in Notebook                      │  │
    │  └─────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │             Export Visualizations                    │  │
    │  └─────────────────────────────────────────────────────┘  │
    │                                                              │
    └────────────────────────────────────────────────────────────┘
            │                          │                  │
            │                          │                  │
        ┌───┴────┐              ┌─────┴────┐      ┌─────┴────┐
        │        │              │          │      │          │
        │Student │              │Researcher│      │Instructor│
        │        │              │          │      │          │
        └────────┘              └──────────┘      └──────────┘
```

---

## Component Diagram: RAG Pipeline (Experiment 3)

```
┌───────────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                                  │
│                                                                     │
│  [Input Documents]                                                 │
│        │                                                           │
│        ▼                                                           │
│  ┌─────────────┐                                                  │
│  │   Chunker   │                                                  │
│  │             │                                                  │
│  │ - Split     │                                                  │
│  │   documents │                                                  │
│  │ - chunk_size│                                                  │
│  │   = 500     │                                                  │
│  └──────┬──────┘                                                  │
│         │ [List[Chunk]]                                           │
│         ▼                                                          │
│  ┌─────────────┐                                                  │
│  │  Embedder   │                                                  │
│  │             │                                                  │
│  │ - Nomic     │                                                  │
│  │   embed     │                                                  │
│  │   text      │                                                  │
│  │ - dim=768   │                                                  │
│  └──────┬──────┘                                                  │
│         │ [List[Vector]]                                          │
│         ▼                                                          │
│  ┌─────────────────┐                                              │
│  │  Vector Store   │                                              │
│  │  (ChromaDB)     │                                              │
│  │                 │                                              │
│  │ - Store vectors │                                              │
│  │ - Index         │                                              │
│  │ - Metadata      │                                              │
│  └─────────┬───────┘                                              │
│            │                                                       │
│            │ [Query]                                               │
│            ▼                                                       │
│  ┌─────────────────┐                                              │
│  │   Retriever     │                                              │
│  │                 │                                              │
│  │ - Similarity    │                                              │
│  │   search        │                                              │
│  │ - Top-k=3       │                                              │
│  └─────────┬───────┘                                              │
│            │                                                       │
│            ▼                                                       │
│     [Relevant Documents]                                           │
│            │                                                       │
│            ▼                                                       │
│    ┌─────────────┐                                                │
│    │   Context   │                                                │
│    │   Builder   │                                                │
│    └──────┬──────┘                                                │
│           │                                                        │
│           ▼                                                        │
│    [LLM Query]                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. Input: 20 Hebrew documents
2. Chunker: Split into ~40 chunks (500 chars each)
3. Embedder: Convert to 768-dim vectors using Nomic
4. Vector Store: Index vectors in ChromaDB
5. Retriever: Given query, find top-3 similar chunks
6. Context Builder: Format retrieved chunks as context
7. LLM Query: Send to Ollama with relevant context only

---

*This UML documentation provides detailed views of the system's structure and behavior. Diagrams will be updated as implementation progresses.*
