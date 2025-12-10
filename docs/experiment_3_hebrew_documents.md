# Experiment 3: RAG Impact with Hebrew Documents

## Summary

**Updated**: 2025-12-10

Experiment 3 has been updated to use **real Hebrew documents** instead of synthetic documents, as required by the assignment.

## What Changed

### Previous Implementation (INCORRECT)
- Used `DocumentGenerator` to create synthetic documents in-memory
- Generated 20 documents with 200 words each
- Embedded a test fact in the middle document
- **Problem**: Assignment requires REAL Hebrew documents, not synthetic

### New Implementation (CORRECT)
- Loads 20 real Hebrew documents from `data/raw/hebrew_documents/`
- Documents are organized by domain:
  - **Technology** (7 documents): AI, Cybersecurity, Cloud, IoT, Blockchain, Software Dev, Mobile Apps
  - **Law** (7 documents): Contracts, IP, Privacy, Employment, Corporate Law, Consumer Protection, Digital Rights
  - **Medicine** (6 documents): Cardiology, Neurology, Pharmacology, Diabetes, Mental Health, Preventive Medicine
- Each document is 500-700 words of real Hebrew content
- Tests RAG retrieval with multilingual (Hebrew) documents

## Assignment Requirement

From `context-windows-lab.pdf` page 5:

> **מאגר של 20 מסמכים בעברית** (נושאים: טכנולוגיה, משפט, רפואה)
>
> "A repository of 20 documents in Hebrew" (topics: technology, law, medicine)

## Files Modified

1. **`src/context_windows_lab/experiments/exp3_rag_impact.py`**:
   - Removed `DocumentGenerator` dependency
   - Added `load_hebrew_documents()` static method
   - Updated constructor to accept `documents_path` and `domain` parameters
   - Changed `_generate_data()` to load from files instead of generating

2. **`src/context_windows_lab/data_generation/document_generator.py`**:
   - Made `fact` and `fact_position` optional in `Document` dataclass
   - Allows Document to represent both synthetic (with embedded facts) and real documents

3. **`src/context_windows_lab/cli.py`**:
   - Updated `run_experiment_3()` to use new constructor
   - Added Hebrew question: "מהם היתרונות העיקריים של הטכנולוגיה?" ("What are the main advantages of technology?")
   - Expected answer: "יעילות" ("efficiency")

## Files Created

1. **`data/raw/hebrew_documents/questions.json`**:
   - Domain-specific Hebrew questions for all 3 domains
   - Expected keywords for evaluation
   - Difficulty ratings
   - 16 total questions (5 technology, 5 law, 6 medicine)

## How It Works Now

### Step 1: Load Hebrew Documents
```python
documents = self.load_hebrew_documents(
    documents_path=Path("data/raw/hebrew_documents"),
    domain=None  # Load all domains
)
# Returns: 20 Document objects with Hebrew content
```

### Step 2: Full Context Mode
- Concatenates all 20 documents into one large context (~10,000 words)
- Sends entire context + question to LLM
- **Trade-off**: High accuracy (all info available), slow latency, high token usage

### Step 3: RAG Mode
- Embeds all 20 documents into ChromaDB vector store
- Retrieves top-3 most relevant documents using similarity search
- Sends only relevant context + question to LLM
- **Trade-off**: Fast, low token usage, but depends on retrieval quality

### Step 4: Comparison
Compares:
- Accuracy (does the answer contain expected keywords?)
- Latency (response time in milliseconds)
- Token usage (number of tokens processed)

## Example Run

```bash
cd "/Users/liorlivyatan/Desktop/Livyatan/MSc CS/LLM Course/HW5"
source venv/bin/activate
context-windows-lab --experiment 3 --iterations 1
```

**Output**:
- `results/experiment_3/results.json` - Full results
- `results/experiment_3/accuracy_comparison.png` - Bar chart
- `results/experiment_3/latency_comparison.png` - Bar chart
- `results/experiment_3/tokens_comparison.png` - Bar chart

## Expected Results

### Full Context Mode
- **Accuracy**: High (all documents available)
- **Latency**: Slow (~15-30 seconds for 10K words)
- **Tokens**: High (~12K tokens)
- **Problem**: Information overload, slow, expensive

### RAG Mode
- **Accuracy**: Medium-High (depends on retrieval quality)
- **Latency**: Fast (~3-5 seconds)
- **Tokens**: Low (~1K tokens for top-3 docs)
- **Advantage**: Selective, fast, cost-effective

## Hebrew Document Statistics

| Domain | Count | Avg Words | Total Words | Encoding |
|--------|-------|-----------|-------------|----------|
| Technology | 7 | ~600 | ~4,200 | UTF-8 |
| Law | 7 | ~600 | ~4,200 | UTF-8 |
| Medicine | 6 | ~600 | ~3,600 | UTF-8 |
| **TOTAL** | **20** | ~600 | **~12,000** | UTF-8 |

## Why Real Hebrew Documents Matter

1. **Assignment Compliance**: Directly matches PDF requirement
2. **Realistic RAG Testing**: Real documents have natural semantic structure
3. **Multilingual Challenge**: Tests if embedding models work well with Hebrew
4. **Domain Diversity**: Technology, Law, and Medicine have different terminology
5. **Transparency**: All documents are in git, fully inspectable

## Benefits Over Synthetic Data

| Aspect | Synthetic Documents | Real Hebrew Documents |
|--------|---------------------|----------------------|
| **Assignment Match** | ❌ Not required | ✅ Required by PDF |
| **Semantic Structure** | ❌ Random templates | ✅ Natural language |
| **RAG Quality** | ❌ Poor embeddings | ✅ Rich semantic meaning |
| **Domain Knowledge** | ❌ Generic phrases | ✅ Real terminology |
| **Transparency** | ❌ Generated at runtime | ✅ Visible in git |
| **Reproducibility** | ✅ Seeded generation | ✅ Fixed documents |

## Future Enhancements

Potential improvements:
- [ ] Test with different questions per domain
- [ ] Vary `top_k` retrieval count (1, 3, 5, 10)
- [ ] Compare different embedding models (nomic-embed-text vs multilingual)
- [ ] Add cross-domain questions (e.g., ask tech question but retrieve law docs)
- [ ] Measure retrieval precision (did RAG retrieve the right documents?)

## References

- **Assignment PDF**: `context-windows-lab.pdf` (page 5)
- **Hebrew Documents**: `data/raw/hebrew_documents/`
- **Questions**: `data/raw/hebrew_documents/questions.json`
- **Implementation**: `src/context_windows_lab/experiments/exp3_rag_impact.py`
- **Data Documentation**: `data/README.md`

---

**Last Updated**: 2025-12-10
**Status**: ✅ Implemented and Ready for Testing
