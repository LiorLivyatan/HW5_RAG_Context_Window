# ADR 002: Building Blocks Pattern for Modular Architecture

## Status
**Accepted** - 2025-12-09

## Context
The Context Windows Lab system needs an architectural pattern that:
1. Supports 4 different experiments with shared functionality
2. Meets the "Building Blocks Design" grading requirement (12 points)
3. Enables code reuse across experiments
4. Facilitates testing of individual components
5. Allows future extensibility for new experiments

### Requirements (from Grading Criteria)
- Clear input data definitions for each block
- Clear output data definitions for each block
- Clear setup data definitions for each block
- Proper validation for all inputs
- Single Responsibility Principle (SRP)
- Separation of concerns
- Reusability across different contexts
- Independent testability

## Decision
We will implement a **Building Blocks Pattern** where the system is decomposed into 7 modular, reusable components:

1. **Document Generator** - Synthetic data creation
2. **Context Manager** - Context string formatting
3. **LLM Interface** - Ollama API client
4. **RAG Components** - Chunking, embedding, retrieval
5. **Evaluator** - Accuracy measurement
6. **Visualizer** - Graph and table generation
7. **Experiment Runner** - Orchestration

Each building block has:
- Clearly defined input/output interfaces
- Configuration parameters (setup data)
- Input validation
- Single responsibility
- No dependencies on other building blocks (except via interfaces)

## Rationale

### Why Building Blocks Pattern?

**Advantages:**
1. **Modularity**: Each block can be developed, tested, and maintained independently
2. **Reusability**: Same blocks used across all 4 experiments
3. **Testability**: Easy to write unit tests for each block in isolation
4. **Clarity**: Clear boundaries and responsibilities
5. **Extensibility**: Easy to add new blocks or experiments
6. **Grading Compliance**: Directly addresses Building Blocks requirement
7. **Composition Over Inheritance**: Flexibility in combining blocks

**Compared to Alternatives:**
- **Monolithic Design**: Would violate SRP, hard to test, poor reusability
- **Microservices**: Overkill for single-machine system, adds networking overhead
- **Plugin Architecture**: Too complex for this scope
- **Pure OOP Inheritance**: Less flexible than composition

### Building Block Specifications

#### 1. Document Generator
```python
class DocumentGenerator:
    """Generate synthetic documents with embedded facts."""

    # Input Data
    def generate_documents(
        self,
        num_docs: int,          # How many documents
        words_per_doc: int,     # Document length
        fact: str,              # Fact to embed
        fact_position: Literal['start', 'middle', 'end']  # Where to place fact
    ) -> List[Document]:
        """Generate documents with specified parameters."""

    # Setup Data
    def __init__(
        self,
        templates: Dict[str, str],  # Text templates
        fact_library: List[str],    # Fact database
        seed: Optional[int] = None  # For reproducibility
    ):
        """Initialize with configuration."""

    # Output Data
    @dataclass
    class Document:
        content: str           # Full document text
        fact: str              # Embedded fact
        fact_position: str     # Position where fact was placed
        metadata: Dict         # Additional info

    # Validation
    def _validate_inputs(self, num_docs, words_per_doc, fact):
        assert num_docs > 0, "num_docs must be positive"
        assert words_per_doc >= 100, "Documents too short"
        assert fact.strip(), "Fact cannot be empty"
```

#### 2. LLM Interface
```python
class OllamaInterface:
    """Interface for querying Ollama LLM."""

    # Input Data
    def query(
        self,
        context: str,   # Context to provide
        question: str   # Question to ask
    ) -> LLMResponse:
        """Query LLM with context and question."""

    # Setup Data
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2",
        temperature: float = 0.0,
        max_tokens: int = 500,
        timeout: int = 60
    ):
        """Initialize Ollama client."""

    # Output Data
    @dataclass
    class LLMResponse:
        text: str              # Generated text
        latency_ms: float      # Response time
        tokens_used: int       # Token count
        model: str             # Model name
        timestamp: datetime    # When query was made

    # Validation
    def _validate_connection(self):
        """Check if Ollama is reachable."""
```

#### 3. Evaluator
```python
class AccuracyEvaluator:
    """Evaluate LLM response accuracy."""

    # Input Data
    def evaluate(
        self,
        response: str,     # LLM response
        expected: str      # Expected answer
    ) -> float:
        """Calculate accuracy score (0.0-1.0)."""

    # Setup Data
    def __init__(
        self,
        method: Literal['exact', 'semantic'] = 'exact',
        case_sensitive: bool = False
    ):
        """Initialize evaluator."""

    # Output Data
    @dataclass
    class EvaluationResult:
        score: float           # Accuracy (0.0-1.0)
        method: str            # Evaluation method
        match_details: Dict    # Additional info

    # Validation
    def _validate_inputs(self, response, expected):
        assert isinstance(response, str), "Response must be string"
        assert isinstance(expected, str), "Expected must be string"
```

*(Similar specifications for other 4 building blocks)*

## Consequences

### Positive
1. **Meets Grading Requirements**: Explicitly addresses 12-point Building Blocks criterion
2. **Code Reuse**: All experiments use same building blocks
3. **Testability**: Each block can be unit tested independently
4. **Maintainability**: Changes to one block don't affect others
5. **Documentation**: Clear interfaces make system easy to understand
6. **Extensibility**: New experiments can be added by composing existing blocks
7. **Team Development**: Different blocks could be developed in parallel (if team project)

### Negative
1. **Initial Overhead**: More upfront design work
2. **Interfaces**: Need to maintain clean interfaces between blocks
3. **Over-Engineering Risk**: Could be simpler for 4 experiments only

### Mitigation
- **Overhead**: Front-load design work (documented here)
- **Interfaces**: Use Python typing and dataclasses for clear contracts
- **Over-Engineering**: Keep blocks simple, avoid premature abstraction

## Implementation Guidelines

### Dependency Injection
Experiments receive building blocks via constructor:
```python
class NeedleInHaystackExperiment(BaseExperiment):
    def __init__(
        self,
        config: ExperimentConfig,
        doc_generator: DocumentGenerator,
        llm_interface: OllamaInterface,
        evaluator: AccuracyEvaluator,
        visualizer: Visualizer
    ):
        self.config = config
        self.doc_gen = doc_generator
        self.llm = llm_interface
        self.evaluator = evaluator
        self.viz = visualizer
```

### Interface Consistency
All building blocks follow same pattern:
1. `__init__()`: Setup data (configuration)
2. Primary method: Input data → Output data
3. Validation: Check inputs before processing
4. No side effects: Pure functions where possible
5. Logging: Log important events

### Testing Strategy
Each building block gets own test module:
```
tests/
  test_document_generator.py
  test_llm_interface.py
  test_evaluator.py
  test_visualizer.py
  test_rag_components.py
```

## Alternatives Considered

### Alternative 1: Monolithic Experiment Classes
Each experiment as self-contained class with all logic embedded.

**Rejected because:**
- Massive code duplication across experiments
- Violates DRY principle
- Hard to test individual components
- Doesn't meet Building Blocks requirement
- Poor extensibility

### Alternative 2: Inheritance-Based Design
Deep inheritance hierarchy with experiments inheriting from base classes.

**Rejected because:**
- Composition is more flexible than inheritance
- Deep hierarchies are hard to understand
- Tight coupling between parent and child classes
- Doesn't demonstrate "building blocks" as clearly

### Alternative 3: Pipeline Pattern
Experiments as pipelines with stages.

**Considered but rejected because:**
- Less clear separation of concerns
- Not all experiments follow same pipeline
- Building Blocks pattern is more explicit
- Would still need similar components

## Validation Checklist
From grading criteria, this design ensures:
- [x] Clear input data definitions for each block
- [x] Clear output data definitions for each block
- [x] Clear setup data definitions for each block
- [x] Proper validation for all inputs
- [x] Single Responsibility Principle
- [x] Separation of concerns
- [x] Reusability (blocks used across all experiments)
- [x] Independent testability

## References
- Software Engineering Best Practices: Building Blocks Pattern
- ISO/IEC 25010 Software Quality Model (Modularity)
- Clean Architecture by Robert C. Martin

## Revision History
- 2025-12-09: Initial ADR defining building blocks architecture
