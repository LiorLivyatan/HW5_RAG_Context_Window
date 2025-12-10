# Context Windows Lab - Comprehensive Documentation

## Experiment Methodology

### Experiment 1: Needle in Haystack (Lost in the Middle)

**Research Question**: Does the position of critical information within a context affect LLM retrieval accuracy?

**Hypothesis**: Information embedded in the middle of long contexts will show reduced accuracy compared to information at the start or end positions (the "Lost in the Middle" phenomenon).

**Methodology**:

1. **Data Generation**:
   - Generate N documents of M words each
   - Embed a critical fact at one of three positions: START, MIDDLE, or END
   - Position assignment is randomized across iterations for statistical validity
   - Each document contains generic filler text with the embedded fact

2. **Query Execution**:
   - For each document, query the LLM with the context
   - Ask a specific question about the embedded fact
   - Record: response text, latency (ms), tokens used

3. **Evaluation**:
   - Compare LLM response against expected answer
   - Use exact string matching (case-insensitive)
   - Binary accuracy: 1.0 (correct) or 0.0 (incorrect)

4. **Statistical Analysis**:
   - Group results by position (START, MIDDLE, END)
   - Calculate mean accuracy and latency per position
   - Compute 95% confidence intervals
   - Run multiple iterations for significance

**Parameters**:
- Documents per iteration: 5
- Words per document: 200
- Total iterations: 3
- Fact: "The CEO of the company is David Cohen."
- Question: "Who is the CEO of the company?"
- Expected answer: "David Cohen"

**Control Variables**:
- Same LLM model (llama2)
- Same temperature (0.0 for deterministic responses)
- Same embedding strategy
- Same evaluation methodology

---

### Experiment 2: Context Size Impact

**Research Question**: How does increasing context window size affect LLM accuracy and latency?

**Hypothesis**: As context size increases, both accuracy and latency will degrade due to:
1. Increased information retrieval complexity
2. Attention dilution across longer sequences
3. Higher computational overhead

**Methodology**:

1. **Variable Context Sizes**:
   - Test with document counts: [2, 5, 10, 20, 50]
   - Each document is 200 words
   - Total context ranges from ~400 words to ~10,000 words

2. **Fixed Fact Position**:
   - Embed critical fact at MIDDLE position in all cases
   - Ensures position effect doesn't confound context size effect

3. **Query Execution**:
   - For each context size, query the LLM
   - Measure: accuracy, latency, tokens used
   - Repeat across 3 iterations

4. **Comparative Analysis**:
   - Plot accuracy vs context size
   - Plot latency vs context size
   - Identify degradation thresholds

**Expected Outcomes**:
- Accuracy degradation as context size increases beyond model's effective window
- Linear or super-linear latency growth with context size
- Token usage proportional to context size

---

### Experiment 3: RAG Impact - Full Context vs Selective Retrieval

**Research Question**: Does RAG (Retrieval-Augmented Generation) improve performance compared to loading all documents into context?

**Hypothesis**: RAG will show:
1. Higher or equal accuracy (by focusing on relevant documents)
2. Lower latency (fewer tokens to process)
3. Higher token efficiency (only relevant content)

**Methodology**:

1. **Document Corpus**:
   - Use 20 Hebrew medical documents
   - Real-world complexity (multilingual, domain-specific)
   - Question: "מה הם התופעות הלוואי של תרופה X?" (What are the side effects of medicine X?)

2. **Two Modes Compared**:

   **Mode A - Full Context**:
   - Concatenate ALL 20 documents into one large context
   - Query LLM with complete context
   - Measures baseline performance with full information

   **Mode B - RAG (Selective Retrieval)**:
   - Embed all documents using nomic-embed-text
   - Store in ChromaDB vector database
   - Retrieve top-3 most relevant documents for the question
   - Query LLM with only retrieved documents

3. **Evaluation Metrics**:
   - Accuracy: Quality of answer
   - Latency: Response time (ms)
   - Tokens: Number of tokens used
   - Efficiency: Accuracy per token

4. **Statistical Comparison**:
   - Run 3 iterations for each mode
   - Calculate mean and confidence intervals
   - Perform comparative analysis

**Challenge - Hebrew Language**:
Note: The local llama2 model has limited Hebrew language support. Results may show:
- Responses in English instead of Hebrew
- Difficulty extracting information from Hebrew documents
- This limitation is documented as a finding about model capabilities

---

### Experiment 4: Context Engineering Strategies

**Research Question**: Which context management strategy performs best for multi-turn interactions?

**Hypothesis**: Different strategies will show distinct trade-offs:
- SELECT (RAG): High accuracy, moderate latency
- COMPRESS (Summarization): Moderate accuracy, low latency
- WRITE (Scratchpad): Highest accuracy, highest latency

**Methodology**:

1. **Simulated Multi-Turn Agent**:
   - Simulate 10-step information gathering process
   - Each step asks a different question
   - Context accumulates over steps

2. **Three Strategies Tested**:

   **SELECT Strategy (RAG)**:
   - Use vector retrieval at each step
   - Retrieve top-k=5 relevant documents
   - Add LLM responses to database for future retrieval
   - Context size remains bounded

   **COMPRESS Strategy (Summarization)**:
   - Summarize context after each step
   - Keep only summaries (not full responses)
   - Context grows slowly with summaries
   - Potential information loss through compression

   **WRITE Strategy (Scratchpad)**:
   - LLM writes structured notes after each query
   - Notes include key facts and relationships
   - Full conversation history retained
   - Unbounded context growth

3. **Evaluation Per Step**:
   - Measure accuracy of each response
   - Track latency over steps
   - Monitor context size growth
   - Calculate cumulative metrics

4. **Comparative Analysis**:
   - Plot accuracy over steps (all strategies)
   - Plot latency over steps
   - Identify optimal strategy for different scenarios

**Parameters**:
- Base documents: 20 documents, 200 words each
- Steps: 10 questions
- top_k for SELECT: 5
- Iterations: 3

---

## Mathematical Formulas

### Accuracy Calculation

For a single query:

```
Accuracy = {
  1.0  if response matches expected answer (exact string match, case-insensitive)
  0.0  otherwise
}
```

For a group of queries (e.g., all queries at a position):

```
Mean Accuracy = (Σ Accuracy_i) / N

where:
  N = total number of queries
  Accuracy_i = accuracy of query i
```

### Latency Measurement

Latency is measured in milliseconds from query submission to response completion:

```
Latency = t_response - t_query

Mean Latency = (Σ Latency_i) / N
```

### Standard Deviation

Sample standard deviation (Bessel's correction, n-1 denominator):

```
σ = sqrt( Σ(x_i - μ)² / (n-1) )

where:
  x_i = individual measurement
  μ = mean of measurements
  n = number of measurements
```

### 95% Confidence Interval

For a metric with mean μ and standard deviation σ:

```
CI_95% = μ ± (1.96 × σ / sqrt(n))

where:
  1.96 = z-score for 95% confidence (normal distribution)
  n = sample size
```

Interpretation: We are 95% confident the true population mean lies within this interval.

### Token Efficiency

For RAG vs Full Context comparison:

```
Token Efficiency = Accuracy / Tokens Used

Higher efficiency = Better performance per token
```

### Context Size

```
Context Size (words) = Num Documents × Words Per Document

Context Size (tokens) ≈ Context Size (words) × 1.3  (English approximation)
```

### Accuracy Degradation Rate

For Context Size Impact experiment:

```
Degradation Rate = (Accuracy_small - Accuracy_large) / (ContextSize_large - ContextSize_small)

Units: Accuracy loss per additional word of context
```

---

## Results Interpretation

### Experiment 1: Lost in the Middle

**[Results to be populated after experiment completion]**

**Key Findings**:
- START position accuracy: [X%] ± [Y%]
- MIDDLE position accuracy: [X%] ± [Y%]
- END position accuracy: [X%] ± [Y%]

**Interpretation**:
- [Analyze whether middle position shows accuracy drop]
- [Discuss statistical significance]
- [Compare to literature findings]

**Latency Analysis**:
- [Discuss whether position affects processing time]
- [Analyze variance in latency]

**Implications**:
- [Practical guidance for prompt engineering]
- [Recommendations for context organization]

---

### Experiment 2: Context Size Impact

**[Results to be populated after experiment completion]**

**Key Findings**:
- Accuracy trend: [describe relationship with context size]
- Latency trend: [describe growth pattern]
- Critical threshold: [context size where degradation begins]

**Interpretation**:
- [Analyze effective context window for llama2]
- [Discuss computational cost vs accuracy trade-off]
- [Compare to model's specified context limit]

**Practical Recommendations**:
- [Optimal context size for this model]
- [When to use chunking or RAG]

---

### Experiment 3: RAG Impact

**[Results to be populated after experiment completion]**

**Key Findings**:
- Full Context: Accuracy [X%], Latency [Y]ms, Tokens [Z]
- RAG (top-3): Accuracy [X%], Latency [Y]ms, Tokens [Z]
- Efficiency gain: [X]%

**Interpretation**:
- [Analyze accuracy comparison]
- [Discuss token savings]
- [Evaluate latency benefits]

**Hebrew Language Challenge**:
- [Document observed llama2 limitations with Hebrew]
- [Discuss implications for multilingual applications]
- [Recommendations for production use]

---

### Experiment 4: Context Engineering Strategies

**[Results to be populated after experiment completion]**

**Key Findings**:
- SELECT (RAG): Accuracy [X%], Latency [Y]ms
- COMPRESS (Summary): Accuracy [X%], Latency [Y]ms
- WRITE (Scratchpad): Accuracy [X%], Latency [Y]ms

**Interpretation**:
- [Analyze accuracy trends over steps]
- [Discuss latency accumulation]
- [Identify optimal strategy for different scenarios]

**Strategy Recommendations**:
- SELECT: [when to use]
- COMPRESS: [when to use]
- WRITE: [when to use]

---

## Prompt Engineering Summary

### Core Prompting Strategy

All experiments use a consistent prompt template:

```
Context:
[DOCUMENT TEXT]

Question: [QUESTION]

Instructions: Answer the question based strictly on the information in the context above. Provide a concise, direct answer.

Answer:
```

**Design Rationale**:
1. **Clear structure**: Separates context, question, and instructions
2. **Explicit instructions**: Directs LLM to use only provided context
3. **Constrained response**: Requests concise answers for accurate evaluation
4. **Temperature 0.0**: Ensures deterministic, reproducible responses

### Hebrew Language Prompts (Experiment 3)

For Hebrew questions, the prompt is adapted:

```hebrew
להלן הטקסט:
[HEBREW DOCUMENT TEXT]

שאלה: [HEBREW QUESTION]

הוראות: ענה על השאלה בעברית בהתבסס בדיוק על המידע המופיע בטקסט. תן תשובה קצרה וישירה.

תשובה:
```

**Challenges Encountered**:
- llama2 model responds in English despite Hebrew prompt
- Limited Hebrew language understanding
- Recommendation: Use multilingual models (e.g., mT5, mBERT) for production

### Prompt Engineering Lessons Learned

1. **Explicit Instructions Matter**: Without "Answer based on context above", LLM may use general knowledge
2. **Temperature 0.0 for Evaluation**: Critical for reproducible accuracy measurement
3. **Concise Answers**: Easier to evaluate than verbose responses
4. **Language Detection**: Implemented automatic Hebrew detection in code
5. **Position Independence**: Prompt structure should not bias toward any context position

---

## Cost and Token Analysis

### Token Usage Statistics

**[To be populated with actual experiment data]**

| Experiment | Total Queries | Tokens/Query (avg) | Total Tokens | Cost (if using API) |
|------------|---------------|-------------------|--------------|---------------------|
| Exp 1      | [N]           | [X]               | [Y]          | $0 (local)          |
| Exp 2      | [N]           | [X]               | [Y]          | $0 (local)          |
| Exp 3      | [N]           | [X]               | [Y]          | $0 (local)          |
| Exp 4      | [N]           | [X]               | [Y]          | $0 (local)          |
| **Total**  | **[N]**       | **[X]**           | **[Y]**      | **$0**              |

### Cost Comparison: Local vs API

**Using Ollama (Local)**:
- Hardware: Standard laptop/desktop
- Cost: $0 (electricity negligible)
- Latency: Varies by hardware (~1-30 seconds per query)
- Privacy: Complete (all data stays local)
- Scalability: Limited by local compute

**Using Claude API (Hypothetical)**:
- Cost per 1K tokens: ~$0.002 (input) + $0.006 (output)
- Estimated total cost for all experiments: $[X]
- Latency: Lower (~0.5-3 seconds per query)
- Privacy: Data sent to Anthropic
- Scalability: Unlimited

**Trade-off Analysis**:
- Local execution chosen for privacy, cost-effectiveness, and educational value
- Production deployment might prefer API for performance and scalability
- Hybrid approach: RAG reduces tokens, making API usage more affordable

---

## Statistical Significance

All experiments run with **3 iterations minimum** to ensure statistical validity.

### Sample Size Justification

For binary accuracy measurements:
- 3 iterations × N queries = sufficient for 95% confidence intervals
- Larger sample sizes reduce confidence interval width
- Trade-off between compute time and precision

### Confidence Interval Interpretation

Example:
```
Accuracy = 0.85 ± 0.12 (95% CI)
```

Interpretation:
- Mean accuracy: 85%
- Margin of error: ±12 percentage points
- True accuracy likely between 73% and 97% with 95% confidence
- Narrower intervals indicate more precise estimates

### Statistical Significance Testing

For comparing two strategies (e.g., Full Context vs RAG):

**Null Hypothesis (H0)**: No difference in accuracy
**Alternative Hypothesis (H1)**: Strategies differ in accuracy

If confidence intervals do not overlap, difference is statistically significant at 95% level.

---

## Visualization Methodology

All visualizations generated with:
- **Library**: Matplotlib + Seaborn
- **Resolution**: 300 DPI (publication quality)
- **Format**: PNG
- **Error bars**: 95% confidence intervals
- **Style**: Clean, professional, accessible colors

### Chart Types

1. **Bar Charts**: Compare metrics across categories (e.g., accuracy by position)
2. **Line Graphs**: Show trends over time or increasing variable (e.g., accuracy vs context size)
3. **Comparison Charts**: Side-by-side comparisons (e.g., Full Context vs RAG)

---

## Reproducibility

All experiments are fully reproducible:

1. **Fixed Random Seeds**: Ensures identical document generation
2. **Deterministic LLM**: Temperature = 0.0
3. **Version Control**: All code and configs in git
4. **Documented Environment**: Python 3.9+, specific library versions
5. **Configuration Files**: YAML-based parameter storage
6. **Result Archiving**: All outputs saved with timestamps

To reproduce:
```bash
# Clone repository
git clone [repo]

# Install dependencies
pip install -e .

# Run experiment
context-windows-lab --experiment [N] --iterations 3
```

Results should match within statistical variance (due to LLM non-determinism and system load affecting latency).

---

## Future Work

### Potential Extensions

1. **Larger Scale**:
   - Test with 100+ documents
   - Longer documents (1000+ words)
   - Evaluate true long-context models (100K+ tokens)

2. **Additional Strategies**:
   - Hybrid approaches (SELECT + COMPRESS)
   - Hierarchical summarization
   - Attention-based relevance scoring

3. **Model Comparison**:
   - Compare llama2, GPT-3.5, GPT-4, Claude
   - Evaluate specialized models (e.g., Longformer)
   - Test multilingual models for Hebrew

4. **Real-World Applications**:
   - Production deployment with API
   - User study with actual questions
   - Domain-specific benchmarks (legal, medical)

5. **Advanced Evaluation**:
   - Semantic similarity (not just exact match)
   - Fact extraction accuracy
   - Response quality scoring

---

## Acknowledgments

This work was conducted using:
- **Ollama**: Local LLM inference
- **llama2**: Meta's open-source LLM
- **ChromaDB**: Vector database
- **Claude Code**: AI development assistant

Academic integrity: All AI assistance is documented in CLAUDE.md development log.

---

**Last Updated**: 2025-12-10
