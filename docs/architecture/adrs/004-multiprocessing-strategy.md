# ADR 004: Multiprocessing Strategy for Parallel Experiment Execution

## Status
**Accepted** - 2025-12-09

## Context
The Context Windows Lab needs to:
1. Meet the "Multiprocessing & Multithreading" grading requirement (12 points)
2. Run multiple experiment iterations for statistical significance (3+ iterations)
3. Optimize runtime performance (experiments can be slow)
4. Demonstrate proper use of Python's concurrency primitives

### Requirements (from Grading Criteria)
- Correct use of multiprocessing for CPU-bound operations
- Correct use of multithreading for I/O-bound operations
- Thread safety (locks, semaphores where needed)
- Proper handling of data sharing between processes
- No race conditions or deadlocks

### Workload Analysis
**CPU-Bound Operations:**
- Generating synthetic documents
- Calculating accuracy metrics
- Statistical computations (mean, std, confidence intervals)
- Running complete experiment iterations (independent work units)

**I/O-Bound Operations:**
- Querying Ollama API (waiting for LLM response)
- Reading/writing configuration files
- Saving results and visualizations
- Loading document templates

## Decision
We will implement a **hybrid parallelization strategy**:

1. **Multiprocessing**: Use `multiprocessing.Pool` to run experiment iterations in parallel
   - Each iteration is an independent process
   - Utilize all available CPU cores
   - No shared state between iterations

2. **Multithreading**: Use `concurrent.futures.ThreadPoolExecutor` for parallel LLM queries within an iteration
   - Multiple LLM API calls in parallel
   - Thread-safe for I/O-bound operations
   - Shared read-only data (documents)

## Rationale

### Why This Hybrid Approach?

**Multiprocessing for Iterations:**
- Each experiment iteration is independent (no shared state)
- Iterations include CPU-intensive work (document generation, evaluation)
- Python's GIL (Global Interpreter Lock) prevents true parallel execution in threads
- Separate processes bypass GIL for true parallelism
- Results can be collected and aggregated after all processes finish

**Multithreading for LLM Queries:**
- LLM queries are I/O-bound (waiting for network/Ollama response)
- Multiple threads can wait concurrently
- Threads share memory (efficient for passing documents)
- No CPU-intensive work during query (GIL not a bottleneck)

### Performance Benefits

**Without Parallelization:**
```
Experiment with 3 iterations, 5 documents each:
- 1 iteration takes ~5 minutes
- Total: 3 iterations × 5 minutes = 15 minutes
```

**With Multiprocessing (4 cores):**
```
- 3 iterations run in parallel on 3 cores
- Total: ~5 minutes (3x speedup)
```

**With Additional Threading:**
```
- Within each iteration, 5 documents queried in parallel
- If each query takes 20s, sequential = 100s total
- With 5 threads: 20s total (5x speedup within iteration)
- Combined speedup: significant improvement
```

## Implementation Details

### Level 1: Multiprocessing for Iterations

```python
from multiprocessing import Pool, cpu_count

def run_single_iteration(config):
    """
    Run a single experiment iteration.
    This function will be executed in a separate process.
    """
    # Generate documents
    # Query LLM
    # Evaluate responses
    # Return results
    return IterationResults(...)

def run_experiment_with_multiprocessing(config, num_iterations=3):
    """
    Run multiple iterations in parallel using multiprocessing.
    """
    # Create pool with number of available CPU cores
    num_workers = min(cpu_count(), num_iterations)

    with Pool(processes=num_workers) as pool:
        # Create configs for each iteration
        configs = [config.copy() for _ in range(num_iterations)]

        # Run iterations in parallel
        results = pool.map(run_single_iteration, configs)

    # Aggregate results
    return aggregate_results(results)
```

**Key Points:**
- Each iteration runs in separate process (true parallelism)
- No shared state (process-safe by design)
- Uses `with` statement for proper cleanup
- Limits workers to available CPU cores

### Level 2: Multithreading for LLM Queries

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def query_llm_parallel(documents, question):
    """
    Query LLM for multiple documents in parallel using threads.
    """
    def query_single_doc(doc):
        return llm_interface.query(doc.content, question)

    # Create thread pool
    max_threads = min(len(documents), 5)  # Limit to 5 concurrent queries

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all queries
        future_to_doc = {
            executor.submit(query_single_doc, doc): doc
            for doc in documents
        }

        # Collect results as they complete
        results = []
        for future in as_completed(future_to_doc):
            doc = future_to_doc[future]
            try:
                result = future.result()
                results.append((doc, result))
            except Exception as e:
                logger.error(f"Query failed for doc {doc.id}: {e}")

    return results
```

**Key Points:**
- Threads for I/O-bound LLM queries
- Limit concurrent threads to avoid overwhelming Ollama
- Exception handling for failed queries
- Results collected as they complete (asynchronous)

### Thread Safety Considerations

**No Shared Mutable State:**
```python
# SAFE: Each process has its own copy
def run_single_iteration(config):
    results = []  # Local to this process
    # ...
    return results

# SAFE: Read-only data in threads
def query_single_doc(doc):  # doc is immutable
    return llm_interface.query(doc.content, question)
```

**If Shared State Were Needed (Not in Our Case):**
```python
from threading import Lock

# Example: Thread-safe counter (not needed in our design)
class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
```

### Progress Reporting

```python
from tqdm import tqdm
import multiprocessing.dummy as mp_dummy

def run_with_progress(configs):
    """
    Run iterations with progress bar.
    """
    with Pool() as pool:
        # Use imap for progress updates
        results = list(tqdm(
            pool.imap(run_single_iteration, configs),
            total=len(configs),
            desc="Running iterations"
        ))
    return results
```

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Main Process                               │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Experiment Orchestrator                              │   │
│  │                                                        │   │
│  │  1. Create multiprocessing.Pool                       │   │
│  │  2. Distribute iterations to worker processes         │   │
│  │  3. Collect results                                   │   │
│  │  4. Aggregate statistics                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                                │
└────────────┬───────────────┬───────────────┬──────────────────┘
             │               │               │
     ┌───────┴──────┐  ┌────┴────┐  ┌───────┴──────┐
     │              │  │         │  │              │
     ▼              ▼  ▼         ▼  ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Worker  │  │ Worker  │  │ Worker  │  │ Worker  │
│Process 1│  │Process 2│  │Process 3│  │Process 4│
│         │  │         │  │         │  │         │
│Iteration│  │Iteration│  │Iteration│  │(Idle if │
│   1     │  │   2     │  │   3     │  │ n<cores)│
│         │  │         │  │         │  │         │
└────┬────┘  └────┬────┘  └────┬────┘  └─────────┘
     │            │            │
     │  Within each process:  │
     │  ThreadPoolExecutor    │
     │  for parallel LLM      │
     │  queries               │
     │            │            │
     └────────────┴────────────┘
                  │
                  ▼
          [Results Collected]
```

## Consequences

### Positive
1. **Performance**: Significant speedup (3-4x for iterations, 5x for queries)
2. **Grading Compliance**: Demonstrates both multiprocessing and multithreading correctly
3. **CPU Utilization**: Makes use of all available cores
4. **Scalability**: Can run more iterations without proportional time increase
5. **Safety**: Process isolation prevents race conditions
6. **Clean Design**: Separation of concerns (iterations vs queries)

### Negative
1. **Complexity**: More complex than sequential execution
2. **Memory**: Each process has memory overhead
3. **Debugging**: Harder to debug parallel execution
4. **Platform Differences**: Multiprocessing behaves differently on Windows vs Unix

### Mitigation
- **Complexity**: Well-documented, clear separation of concerns
- **Memory**: Limit concurrent processes to cpu_count()
- **Debugging**: Provide --no-parallel flag for debugging
- **Platform**: Test on multiple platforms, provide clear error messages

## Configuration

```yaml
parallelization:
  # Multiprocessing settings
  use_multiprocessing: true
  max_processes: null  # null = use cpu_count()

  # Multithreading settings
  use_multithreading: true
  max_threads_per_process: 5

  # Debugging
  disable_parallel: false  # Set true for debugging
```

## Testing Strategy

### Unit Tests
```python
def test_multiprocessing_pool():
    """Test that pool executes functions in parallel"""
    # Time sequential execution
    # Time parallel execution
    # Assert parallel is faster

def test_thread_safety():
    """Test no race conditions in threaded queries"""
    # Run same queries in threads
    # Verify results are consistent

def test_exception_handling():
    """Test that exceptions in workers don't crash main"""
    # Inject failure in worker
    # Verify main process handles gracefully
```

### Integration Tests
```python
def test_full_parallel_experiment():
    """Test complete experiment with parallelization"""
    # Run experiment with parallelization
    # Verify results match sequential version
    # Verify all iterations completed
```

## Performance Benchmarks

Expected on 4-core machine:
```
Sequential Execution:
- 1 iteration: 5 minutes
- 3 iterations: 15 minutes

With Multiprocessing (4 cores):
- 3 iterations: ~5 minutes (3x speedup)

With Additional Threading:
- Per-iteration speedup: ~4-5x
- Total time: ~1-2 minutes (10-15x overall speedup)
```

## Alternatives Considered

### Alternative 1: Only Multithreading (No Multiprocessing)
Use threads for everything.

**Rejected because:**
- GIL prevents true parallelism for CPU-bound work
- Doesn't demonstrate multiprocessing requirement
- Less performance gain

### Alternative 2: Only Multiprocessing (No Multithreading)
Use processes for everything.

**Rejected because:**
- Less efficient for I/O-bound LLM queries
- Doesn't demonstrate multithreading requirement
- More memory overhead

### Alternative 3: async/await with asyncio
Use asynchronous programming.

**Rejected because:**
- More complex to implement and understand
- Ollama client may not be async-compatible
- Multiprocessing still needed for CPU-bound work
- Threading is simpler for I/O-bound operations

## References
- [Python multiprocessing documentation](https://docs.python.org/3/library/multiprocessing.html)
- [Python concurrent.futures documentation](https://docs.python.org/3/library/concurrent.futures.html)
- [Understanding the Python GIL](https://realpython.com/python-gil/)
- [When to Use Threading vs Multiprocessing](https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/)

## Validation Checklist
- [x] Multiprocessing used for CPU-bound operations (iterations)
- [x] Multithreading used for I/O-bound operations (LLM queries)
- [x] Thread safety ensured (no shared mutable state)
- [x] Proper data handling between processes (immutable configs)
- [x] No race conditions (process isolation)
- [x] No deadlocks (no locks needed with our design)

## Revision History
- 2025-12-09: Initial ADR defining parallelization strategy
