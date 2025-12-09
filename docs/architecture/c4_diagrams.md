# C4 Model Architecture Diagrams

## Overview

This document presents the Context Windows Lab system architecture using the C4 model (Context, Containers, Components, Code). The C4 model provides a hierarchical set of diagrams to understand the system at different levels of abstraction.

---

## Level 1: System Context Diagram

**Purpose**: Shows how the Context Windows Lab system fits into the world, highlighting external actors and dependencies.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                          System Context                               │
│                                                                       │
│    ┌──────────────┐                                                  │
│    │              │                                                  │
│    │    User      │──────┐                                          │
│    │  (Student/   │      │                                          │
│    │ Researcher)  │      │                                          │
│    │              │      │                                          │
│    └──────────────┘      │                                          │
│                          │                                          │
│                          │                                          │
│                          ▼                                          │
│             ┌────────────────────────────┐                         │
│             │                            │                         │
│             │  Context Windows Lab       │                         │
│             │                            │                         │
│             │  Experimental framework     │                         │
│             │  for demonstrating LLM      │                         │
│             │  context window phenomena   │                         │
│             │                            │                         │
│             └────────────┬───────────────┘                         │
│                          │                                          │
│                          │                                          │
│          ┌───────────────┼───────────────┐                         │
│          │               │               │                         │
│          ▼               ▼               ▼                         │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐                 │
│   │            │  │            │  │            │                 │
│   │   Ollama   │  │  ChromaDB  │  │ File System│                 │
│   │            │  │            │  │            │                 │
│   │  (Local    │  │  (Vector   │  │  (Results  │                 │
│   │   LLM)     │  │   Store)   │  │  Storage)  │                 │
│   │            │  │            │  │            │                 │
│   └────────────┘  └────────────┘  └────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Actors:**
- **User**: Student or researcher running experiments to understand context window behavior
- **Ollama**: Local LLM server providing language model inference
- **ChromaDB**: Embedded vector database for RAG experiments
- **File System**: Storage for configuration, results, and visualizations

**System Responsibilities:**
- Generate synthetic test data
- Execute 4 types of experiments on LLM context behavior
- Measure performance metrics (accuracy, latency, tokens)
- Generate visualizations and statistical analysis
- Provide CLI interface for user interaction

---

## Level 2: Container Diagram

**Purpose**: Shows the high-level containers (applications, services) that make up the system and how they interact.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                        Context Windows Lab System                          │
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────┐   │
│    │                                                                   │   │
│    │                    CLI Application                                │   │
│    │                    (Python 3.9+)                                  │   │
│    │                                                                   │   │
│    │  - Argparse-based command-line interface                         │   │
│    │  - Progress bars and colored output                              │   │
│    │  - Configuration loading                                         │   │
│    │  - Experiment orchestration                                      │   │
│    │                                                                   │   │
│    └────────────────────────┬──────────────────────────────────────┘   │
│                             │                                             │
│                             │ calls                                       │
│                             ▼                                             │
│    ┌─────────────────────────────────────────────────────────────────┐   │
│    │                                                                   │   │
│    │              Experiment Engine (Python Package)                   │   │
│    │              src/context_windows_lab/                             │   │
│    │                                                                   │   │
│    │  ┌─────────────────────────────────────────────────────────────┐ │   │
│    │  │ Experiment Modules                                          │ │   │
│    │  │  - Exp1: Needle in Haystack                                │ │   │
│    │  │  - Exp2: Context Size Impact                               │ │   │
│    │  │  - Exp3: RAG vs Full Context                               │ │   │
│    │  │  - Exp4: Context Engineering Strategies                    │ │   │
│    │  └─────────────────────────────────────────────────────────────┘ │   │
│    │                                                                   │   │
│    │  ┌─────────────────────────────────────────────────────────────┐ │   │
│    │  │ Core Building Blocks                                        │ │   │
│    │  │  - Document Generator                                       │ │   │
│    │  │  - Context Manager                                          │ │   │
│    │  │  - LLM Interface (Ollama client)                           │ │   │
│    │  │  - RAG Components (Chunker, Embedder, Retriever)          │ │   │
│    │  │  - Evaluator                                                │ │   │
│    │  │  - Visualizer                                               │ │   │
│    │  └─────────────────────────────────────────────────────────────┘ │   │
│    │                                                                   │   │
│    └────────────────────┬────────────┬────────────┬──────────────────┘   │
│                         │            │            │                       │
└─────────────────────────┼────────────┼────────────┼───────────────────────┘
                          │            │            │
                          │ HTTP       │ API        │ Write
                          │ requests   │ calls      │ files
                          ▼            ▼            ▼
                    ┌──────────┐ ┌──────────┐ ┌──────────┐
                    │          │ │          │ │          │
                    │  Ollama  │ │ ChromaDB │ │   File   │
                    │  Server  │ │ (Vector  │ │  System  │
                    │          │ │  Store)  │ │          │
                    │   :11434 │ │Embedded  │ │results/  │
                    │          │ │          │ │config/   │
                    └──────────┘ └──────────┘ └──────────┘
```

**Container Interactions:**
1. **User → CLI**: Executes commands (`--run-all`, `--experiment N`)
2. **CLI → Experiment Engine**: Loads config, invokes experiments
3. **Experiment Engine → Ollama**: HTTP POST requests with prompts
4. **Experiment Engine → ChromaDB**: Vector operations (store, search)
5. **Experiment Engine → File System**: Save results, visualizations

---

## Level 3: Component Diagram

**Purpose**: Shows the internal components of the Experiment Engine and their responsibilities.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Experiment Engine Components                            │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Experiment Layer                              │   │
│  │                                                                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐│   │
│  │  │              │  │              │  │              │  │          ││   │
│  │  │ Experiment 1 │  │ Experiment 2 │  │ Experiment 3 │  │ Exp 4    ││   │
│  │  │              │  │              │  │              │  │          ││   │
│  │  │ Needle in    │  │ Context Size │  │ RAG Impact   │  │ Context  ││   │
│  │  │ Haystack     │  │ Impact       │  │              │  │ Engineering││   │
│  │  │              │  │              │  │              │  │          ││   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────┬─────┘│   │
│  │         │                  │                  │               │      │   │
│  └─────────┼──────────────────┼──────────────────┼───────────────┼──────┘   │
│            │                  │                  │               │          │
│            │                  │                  │               │          │
│            ▼                  ▼                  ▼               ▼          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Core Services Layer                             │   │
│  │                                                                       │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │   │
│  │  │                │  │                │  │                │        │   │
│  │  │   Document     │  │   Context      │  │      LLM       │        │   │
│  │  │   Generator    │  │   Manager      │  │   Interface    │        │   │
│  │  │                │  │                │  │                │        │   │
│  │  │ - Generate     │  │ - Build        │  │ - Query Ollama │        │   │
│  │  │   synthetic    │  │   context      │  │ - Measure      │        │   │
│  │  │   documents    │  │   strings      │  │   latency      │        │   │
│  │  │ - Embed facts  │  │ - Apply        │  │ - Count tokens │        │   │
│  │  │ - Templates    │  │   strategies   │  │ - Retry logic  │        │   │
│  │  │                │  │                │  │                │        │   │
│  │  └────────────────┘  └────────────────┘  └────────┬───────┘        │   │
│  │                                                     │                │   │
│  │  ┌────────────────┐  ┌────────────────┐          │                │   │
│  │  │                │  │                │          │                │   │
│  │  │   Evaluator    │  │  Visualizer    │◄─────────┘                │   │
│  │  │                │  │                │                            │   │
│  │  │ - Compare      │  │ - Plot graphs  │                            │   │
│  │  │   responses    │  │ - Generate     │                            │   │
│  │  │ - Calculate    │  │   tables       │                            │   │
│  │  │   accuracy     │  │ - Export PNG   │                            │   │
│  │  │ - Statistics   │  │ - Styling      │                            │   │
│  │  │                │  │                │                            │   │
│  │  └────────────────┘  └────────────────┘                            │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         RAG Layer                                    │   │
│  │                      (Used by Experiment 3)                          │   │
│  │                                                                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │          │  │          │  │          │  │          │          │   │
│  │  │ Chunker  │──│ Embedder │──│  Vector  │──│Retriever │          │   │
│  │  │          │  │          │  │  Store   │  │          │          │   │
│  │  │ Split    │  │ Nomic    │  │ ChromaDB │  │Similarity│          │   │
│  │  │ docs     │  │ embed    │  │ storage  │  │ search   │          │   │
│  │  │          │  │          │  │          │  │          │          │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Infrastructure Layer                              │   │
│  │                                                                       │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │   │
│  │  │                │  │                │  │                │        │   │
│  │  │ Configuration  │  │    Logging     │  │Multiprocessing │        │   │
│  │  │   Manager      │  │    System      │  │    Manager     │        │   │
│  │  │                │  │                │  │                │        │   │
│  │  │ Load YAML/env  │  │ Log events     │  │ Pool workers   │        │   │
│  │  │ Validate       │  │ Debug info     │  │ Parallel exec  │        │   │
│  │  │                │  │                │  │                │        │   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘        │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Component Responsibilities:**

**Experiment Layer:**
- Implement specific experiment logic
- Orchestrate building blocks
- Define experiment parameters
- Generate results

**Core Services:**
- **Document Generator**: Create synthetic test data
- **Context Manager**: Format context strings
- **LLM Interface**: Communicate with Ollama
- **Evaluator**: Measure accuracy
- **Visualizer**: Create graphs and tables

**RAG Layer:**
- **Chunker**: Split documents into chunks
- **Embedder**: Generate vector embeddings
- **Vector Store**: Store and manage embeddings
- **Retriever**: Similarity search

**Infrastructure:**
- **Configuration Manager**: Load and validate configs
- **Logging**: Track execution and debug
- **Multiprocessing Manager**: Parallel execution

---

## Level 4: Code Diagram (Key Classes)

**Purpose**: Shows the key classes and their relationships.

```python
# Experiment Base Class
class BaseExperiment:
    """Abstract base class for all experiments"""
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.results = []

    def run(self) -> ExperimentResults:
        """Execute experiment (template method)"""
        pass

    def analyze(self) -> Analysis:
        """Analyze results"""
        pass

    def visualize(self) -> Path:
        """Generate visualizations"""
        pass

# Example Concrete Experiment
class NeedleInHaystackExperiment(BaseExperiment):
    def __init__(self, config, doc_generator, llm_interface, evaluator, visualizer):
        super().__init__(config)
        self.doc_gen = doc_generator
        self.llm = llm_interface
        self.evaluator = evaluator
        self.viz = visualizer

    def run(self) -> ExperimentResults:
        # Generate docs with facts at different positions
        # Query LLM for each document
        # Evaluate responses
        # Return results

# Building Block: Document Generator
class DocumentGenerator:
    def generate_documents(
        self,
        num_docs: int,
        words_per_doc: int,
        fact: str,
        fact_position: Literal['start', 'middle', 'end']
    ) -> List[Document]:
        """Generate synthetic documents with embedded facts"""
        pass

# Building Block: LLM Interface
class OllamaInterface:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def query(self, context: str, question: str) -> LLMResponse:
        """Query Ollama with context and question"""
        # Measure latency
        # Count tokens
        # Return response + metadata
        pass

# Building Block: Evaluator
class AccuracyEvaluator:
    def evaluate(self, response: str, expected: str) -> float:
        """Calculate accuracy score (0.0 - 1.0)"""
        pass

    def calculate_statistics(self, scores: List[float]) -> Statistics:
        """Calculate mean, std, confidence intervals"""
        pass

# Building Block: Visualizer
class Visualizer:
    def plot_bar_chart(self, data: Dict, title: str, output_path: Path):
        """Generate bar chart"""
        pass

    def plot_line_graph(self, x_data: List, y_data: List, output_path: Path):
        """Generate line graph"""
        pass

    def generate_table(self, data: DataFrame, output_path: Path):
        """Generate comparison table"""
        pass
```

**Key Design Patterns:**
1. **Template Method**: BaseExperiment defines structure, subclasses implement specifics
2. **Strategy**: Different context management strategies (SELECT, COMPRESS, WRITE)
3. **Builder**: Document Generator builds documents with flexible configuration
4. **Facade**: LLM Interface provides simplified API for complex Ollama interactions
5. **Dependency Injection**: Experiments receive building blocks via constructor

---

## Data Flow Diagram

**Experiment Execution Flow:**

```
User Input
    │
    ▼
┌─────────────┐
│ CLI Parser  │
└──────┬──────┘
       │ Load config
       ▼
┌──────────────────┐
│ Config Manager   │
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ Experiment Factory   │
│ (Select Exp 1-4)     │
└──────┬───────────────┘
       │
       ▼
┌───────────────────────┐
│ Experiment Instance   │
│                       │
│  run() method:        │
│  ┌────────────────┐  │
│  │1. Generate Data│  │
│  └───────┬────────┘  │
│          ▼           │
│  ┌────────────────┐  │
│  │2. Build Context│  │
│  └───────┬────────┘  │
│          ▼           │
│  ┌────────────────┐  │
│  │3. Query LLM    │──┼──> Ollama API
│  └───────┬────────┘  │
│          ▼           │
│  ┌────────────────┐  │
│  │4. Evaluate     │  │
│  └───────┬────────┘  │
│          ▼           │
│  ┌────────────────┐  │
│  │5. Aggregate    │  │
│  └───────┬────────┘  │
│          ▼           │
│  ┌────────────────┐  │
│  │6. Visualize    │  │
│  └───────┬────────┘  │
└──────────┼───────────┘
           │
           ▼
    ┌──────────────┐
    │ Save Results │──> File System
    │  - JSON      │     (results/)
    │  - PNG       │
    │  - Stats     │
    └──────────────┘
```

---

## Deployment Diagram

**Physical deployment on development machine:**

```
┌──────────────────────────────────────────────────────────────┐
│                    Developer Machine                          │
│                    (macOS / Linux / Windows)                  │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │            Python 3.9+ Runtime Environment             │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │   context_windows_lab Package                     │  │  │
│  │  │   (Installed via: pip install -e .)               │  │  │
│  │  │                                                    │  │  │
│  │  │   - CLI entry point                                │  │  │
│  │  │   - All experiments                                │  │  │
│  │  │   - Building blocks                                │  │  │
│  │  │   - Dependencies (ollama, langchain, chromadb)    │  │  │
│  │  │                                                    │  │  │
│  │  └────────────────────────┬───────────────────────────┘  │  │
│  │                           │                              │  │
│  │                           │ HTTP: localhost:11434        │  │
│  │                           ▼                              │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │   Ollama Server Process                           │  │  │
│  │  │   - Running llama2 model                          │  │  │
│  │  │   - Listening on port 11434                       │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │             File System                                 │  │
│  │                                                          │  │
│  │  ~/context-windows-lab/                                 │  │
│  │    ├── config/          (YAML configs)                  │  │
│  │    ├── results/         (JSON, PNG outputs)             │  │
│  │    ├── data/            (Synthetic data cache)          │  │
│  │    └── .chroma/         (ChromaDB storage)              │  │
│  │                                                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

**Hardware Requirements:**
- **CPU**: Multi-core (4+ cores recommended for parallel execution)
- **RAM**: 8-16GB (Ollama + experiments)
- **Disk**: ~5GB (Ollama models) + ~100MB (results)
- **Network**: Not required (all local)

---

## Scalability Considerations

### Current Implementation
- **Single machine**: All processing on local machine
- **Multiprocessing**: Utilize all CPU cores for parallel experiment iterations
- **Multithreading**: Parallel LLM API calls (I/O-bound)

### Future Scalability Options
1. **Distributed Execution**: Run experiments across multiple machines
2. **Cloud LLM**: Option to use cloud APIs for faster inference
3. **Batch Processing**: Queue multiple experiment configurations
4. **Result Caching**: Cache LLM responses to avoid redundant calls

---

## Security Architecture

### Security Measures
1. **Local-Only**: No external network calls (except to local Ollama)
2. **No Authentication**: Single-user system, no auth needed
3. **No Sensitive Data**: All data is synthetic
4. **Environment Variables**: .env for future API keys (not checked into git)
5. **Input Validation**: Validate all config files before processing

### Threat Model
- **Low Risk**: Educational tool for local use only
- **No Network Exposure**: No listening ports or external APIs
- **No User Data**: No collection or storage of personal information

---

*This C4 documentation will be updated as the system evolves during implementation.*
