# Data Flow Explanation - Context Windows Lab

## Where is All the Data?

This document explains where all the documents and data come from, how they're fed to the LLM, and where results are stored.

## Overview: Data is Generated Synthetically In-Memory

**KEY POINT**: Documents are **NOT** stored in files on disk. They are **generated synthetically in memory** at runtime using the `DocumentGenerator` building block.

## Complete Data Flow

### 1. Document Generation (In-Memory)

**Location**: `src/context_windows_lab/data_generation/document_generator.py`

**How it works**:
- Documents are generated on-the-fly when an experiment runs
- Uses random templates and filler text (generic business phrases)
- Embeds a specific fact at a specified position (start/middle/end)
- All generation happens in memory - no files written

**Example**:
```python
from context_windows_lab.data_generation.document_generator import DocumentGenerator

gen = DocumentGenerator(seed=42)
docs = gen.generate_documents(
    num_docs=5,
    words_per_doc=200,
    fact='The capital of Zanzibar is Stone Town.',
    fact_position='middle'
)
# docs is a list of Document objects in memory
```

**What the generated documents look like**:
```
In recent developments, The company has demonstrated the need for detailed
planning. Research indicates that The team requires systematic approach in most
scenarios. In recent developments, The data has demonstrated the need for careful
analysis. The company needs detailed planning for optimal performance and
efficiency. Stakeholder feedback emphasizes that The data requires systematic
approach. Research indicates that The data supports detailed planning in most
scenarios. The capital of Zanzibar is Stone Town. Technical documentation confirms
that The data provides careful analysis. According to industry standards, The
system provides comprehensive testing to ensure quality...
```

Notice:
- Filler text: Generic phrases like "The company has demonstrated the need for..."
- Embedded fact: "The capital of Zanzibar is Stone Town." (in the middle)
- This is synthetic data designed to test LLM context window handling

### 2. Document Templates

**Default templates** (defined in `document_generator.py`):
```python
templates = [
    "{subject} {verb} {object}.",
    "According to industry standards, {subject} {verb} {object} to ensure quality.",
    "Research indicates that {subject} {verb} {object} in most scenarios.",
    "In recent developments, {subject} has demonstrated the need for {object}.",
    "Performance metrics reveal that {subject} consistently {verb} {object}.",
    "Technical documentation confirms that {subject} {verb} {object}.",
    "Stakeholder feedback emphasizes that {subject} {verb} {object}.",
    "Best practices suggest that {subject} should prioritize {object}.",
    "Historical data shows that {subject} consistently {verb} {object}.",
    "The implementation of {subject} {verb} {object} across all departments.",
]
```

**Placeholders filled with**:
- subjects: ["The company", "The team", "The project", "The system", "The data"]
- verbs: ["requires", "needs", "provides", "supports", "manages"]
- objects: ["careful analysis", "detailed planning", "comprehensive testing", "thorough review", "systematic approach"]

**Result**: Generic, boring text that serves as "haystack" to hide the "needle" (fact)

### 3. Context Construction

When an experiment runs, documents are concatenated into a single context string:

```python
# Combine all documents into one context
context = '\n\n'.join([doc.content for doc in docs])
```

**Example context size**:
- 5 documents × 200 words = ~1,000 words = ~8KB = ~2,000 tokens
- 20 documents × 200 words = ~4,000 words = ~32KB = ~8,000 tokens
- 30 documents × 300 words = ~9,000 words = ~72KB = ~18,000 tokens

### 4. Prompt Construction

**Location**: `src/context_windows_lab/llm/ollama_interface.py` - `_build_prompt()` method

The prompt sent to Ollama LLM has this format:

```
Context:
[Document 1 content]

[Document 2 content]

[Document 3 content]

... [more documents] ...

Question: What is the capital of Zanzibar?

Answer:
```

The LLM fills in the "Answer:" part by reading the context and finding the fact.

### 5. LLM Query

**Location**: `src/context_windows_lab/llm/ollama_interface.py` - `query()` method

```python
response = ollama.generate(
    model='llama2',
    prompt=prompt,  # Context + Question + "Answer: "
    options={
        'temperature': 0.1,
        'num_predict': 100,
    }
)
```

**What happens**:
1. Prompt (context + question) sent to Ollama server (localhost:11434)
2. llama2 model processes the prompt
3. LLM generates an answer based on the context
4. Response returned (text, latency, token count)

### 6. Response Evaluation

**Location**: `src/context_windows_lab/evaluation/accuracy_evaluator.py`

The LLM's response is compared to the expected answer:

```python
evaluator = AccuracyEvaluator()
is_correct = evaluator.evaluate(
    response="Stone Town",
    expected_answer="Stone Town",
    method="contains"
)
# Returns: 1.0 (100% accuracy)
```

**Evaluation methods**:
- `exact`: Exact string match (case-insensitive)
- `contains`: Expected answer appears anywhere in response
- `partial`: Jaccard similarity (word overlap)

### 7. Results Storage

**Location**: `results/` directory

After an experiment completes, results are saved to:

```
results/
├── experiment_1/
│   ├── results.json           # All query data (questions, responses, accuracy, latency)
│   └── accuracy_by_position.png  # Visualization
├── experiment_2/
│   ├── results.json
│   ├── accuracy_vs_context_size.png
│   ├── latency_vs_context_size.png
│   └── context_size_comparison.png
├── experiment_3/
│   ├── results.json
│   ├── accuracy_comparison.png
│   ├── latency_comparison.png
│   └── tokens_comparison.png
└── experiment_4/
    ├── results.json
    ├── overall_accuracy_by_strategy.png
    └── latency_by_strategy.png
```

**results.json structure**:
```json
{
  "experiment": "Context Strategies",
  "config": {
    "iterations": 1
  },
  "raw_results": [
    {
      "strategy": "WRITE",
      "step": 1,
      "question": "What is the project budget for Q1 2025?",
      "expected_answer": "$2.5 million",
      "response": "The project budget for Q1 2025 is $2.5 million.",
      "accuracy": 1.0,
      "latency_ms": 2361.46,
      "tokens_used": 11,
      "success": true
    },
    ...
  ],
  "statistics": {
    "overall_accuracy": 0.3333,
    "overall_latency_ms": 4684.56
  }
}
```

## Example: Experiment 1 Data Flow

Let's trace a complete example from Experiment 1 (Needle in Haystack):

### Step 1: Generate 5 Documents
```python
docs = generator.generate_documents(
    num_docs=5,
    words_per_doc=200,
    fact="The magic number is 42.",
    fact_position="middle"
)
```

**Generated documents** (in memory):
- Document 1: 200 words of filler + "The magic number is 42." in middle
- Document 2: 200 words of filler + "The magic number is 42." in middle
- Document 3: 200 words of filler + "The magic number is 42." in middle
- Document 4: 200 words of filler + "The magic number is 42." in middle
- Document 5: 200 words of filler + "The magic number is 42." in middle

### Step 2: Build Context
```python
context = '\n\n'.join([doc.content for doc in docs])
# context is now ~1,000 words of text with the fact embedded 5 times
```

### Step 3: Build Prompt
```python
prompt = f"""Context:
{context}

Question: What is the magic number?

Answer: """
```

### Step 4: Query LLM
```python
response = ollama.generate(model='llama2', prompt=prompt)
# response.text = "The magic number is 42."
```

### Step 5: Evaluate
```python
accuracy = evaluator.evaluate(
    response="The magic number is 42.",
    expected_answer="42",
    method="contains"
)
# accuracy = 1.0 (correct!)
```

### Step 6: Save Results
```json
{
  "position": "middle",
  "question": "What is the magic number?",
  "expected_answer": "42",
  "response": "The magic number is 42.",
  "accuracy": 1.0,
  "latency_ms": 2500,
  "tokens_used": 15,
  "success": true
}
```

## Real Data from Our Experiments

Here are examples of actual data from our experiments:

### Experiment 4 - WRITE Strategy (Successful)

**Query 1**:
- Question: "What is the project budget for Q1 2025?"
- Expected: "$2.5 million"
- LLM Response: "The project budget for Q1 2025 is $2.5 million."
- Accuracy: 1.0 (100%)
- Latency: 2,361ms

**Query 2**:
- Question: "How many engineers are on the team?"
- Expected: "15"
- LLM Response: "Based on the information provided in the scratchpad memory, there are 15 engineers on the team."
- Accuracy: 1.0 (100%)
- Latency: 2,582ms

### Experiment 4 - SELECT Strategy (Failed)

**Query 1**:
- Question: "What is the project budget for Q1 2025?"
- Expected: "$2.5 million"
- LLM Response: "Based on the provided text, there is no direct answer to the question of the project budget for Q1 2025. However, there are several hints and clues throughout the text that could be used to estimate the budget. Here are some possible factors to consider: 1. Historical data: The text mentions that the company has consistently managed careful analysis in the past. This suggests that the company has a history of investing in research and development, which could indicate a higher budget for Q1 2025..." [continues for 423 tokens]
- Accuracy: 0.0 (0%)
- Latency: 9,679ms

## Why Synthetic Data?

**Benefits**:
1. **Reproducibility**: Seeded random generation = same results every time
2. **Controlled Experiments**: We know exactly where the fact is embedded
3. **Scalability**: Can generate thousands of documents instantly
4. **Ground Truth**: We know the correct answer (the fact we embedded)
5. **No Copyright Issues**: All text is generated, not copied

**Trade-offs**:
1. **Not Realistic**: Real documents have semantic structure
2. **Poor Embeddings**: Generic text confuses vector similarity models
3. **Limited Insights**: Results may not generalize to real-world documents

## Summary

**Data Generation**: Documents generated in-memory using templates
↓
**Context Construction**: All documents concatenated into single string
↓
**Prompt Construction**: Context + Question + "Answer: "
↓
**LLM Query**: Sent to Ollama (llama2 model)
↓
**Response**: LLM generates answer
↓
**Evaluation**: Compare response to expected answer
↓
**Storage**: Save results to results/{experiment_name}/results.json

**Key Takeaway**: All documents are synthetic and exist only in memory during experiment execution. Results are the only artifacts saved to disk.

## Visualizing the Data

To see what data is actually generated, you can run:

```bash
cd /path/to/project
source venv/bin/activate
python -c "
from context_windows_lab.data_generation.document_generator import DocumentGenerator

gen = DocumentGenerator(seed=42)
docs = gen.generate_documents(
    num_docs=3,
    words_per_doc=150,
    fact='Your custom fact here',
    fact_position='middle'
)

for i, doc in enumerate(docs, 1):
    print(f'Document {i}:')
    print(doc.content)
    print()
"
```

This will show you exactly what the LLM sees as input.
