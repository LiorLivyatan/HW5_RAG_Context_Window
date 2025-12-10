# Using Weaker Models to Demonstrate "Lost in the Middle"

## Problem
With `llama2` (7B/13B parameters), the model is too powerful and achieves 100% accuracy even with 5 documents × 200 words.

## Solutions Implemented

### 1. **Distractors** ✅ (Implemented)
Added confusing similar facts to documents:
- Wrong CEO names (Michael Anderson, Sarah Williams, etc.)
- Similar executive roles (COO, CFO, CTO)
- Dates and numbers to confuse the model
- Other plausible but incorrect company details

**How to enable:**
```bash
# Edit config/experiments.yaml
experiment_1:
  add_distractors: true  # Change to true

# Or use the test script:
python test_harder_exp1.py
```

### 2. **Weaker Models** (Recommended)
Use smaller models that struggle more with context:

#### Option A: TinyLlama (1.1B parameters) - BEST FOR TESTING
```bash
# Pull the model (1.1GB download)
ollama pull tinyllama

# Run experiment with tinyllama
python test_harder_exp1.py
```

**Why tinyllama?**
- Only 1.1B parameters (vs llama2's 7B/13B)
- Much more likely to get confused by:
  - Middle-positioned facts
  - Distractors and similar names
  - Longer contexts

#### Option B: Phi-2 (2.7B parameters)
```bash
ollama pull phi-2
```

#### Option C: Gemma 2B
```bash
ollama pull gemma:2b
```

## Comparison Chart

| Model | Size | Expected Accuracy | Lost in Middle? |
|-------|------|------------------|-----------------|
| llama2 | 7-13B | ~95-100% | ❌ Too strong |
| llama2 + distractors | 7-13B | ~70-90% | ⚠️ Maybe |
| phi-2 | 2.7B | ~60-80% | ✅ Likely |
| tinyllama | 1.1B | ~40-70% | ✅✅ Very likely |
| tinyllama + distractors | 1.1B | ~30-60% | ✅✅✅ Guaranteed |

## Testing Workflow

### Step 1: Test with distractors + llama2
```bash
cd "/Users/liorlivyatan/Desktop/Livyatan/MSc CS/LLM Course/HW5"
source venv/bin/activate
python test_harder_exp1.py
```

Expected: Some accuracy drop, especially at middle position

### Step 2: Pull tinyllama
```bash
ollama pull tinyllama
```

### Step 3: Test with distractors + tinyllama
```bash
python test_harder_exp1.py
```

Expected: Significant accuracy drop at middle position (~40-60%)

## Modifying Experiment Configuration

You can also run via CLI with different models:

```bash
# Edit config/llm_config.yaml
ollama:
  model: "tinyllama"  # Change from "llama2"

# Then run normally
context-windows-lab --experiment 1 --iterations 3 --verbose
```

## Expected Results with Distractors + TinyLlama

```
Position    | Accuracy
------------|----------
Start       | 70-80%  (easier to find)
Middle      | 30-50%  (LOST IN THE MIDDLE!)
End         | 60-75%  (recency bias helps)
```

This demonstrates the true "Lost in the Middle" phenomenon where facts embedded in the middle of context are significantly harder to retrieve than those at the start or end.

## References

- TinyLlama: https://ollama.com/library/tinyllama
- Phi-2: https://ollama.com/library/phi
- Gemma: https://ollama.com/library/gemma

## Quick Test Summary

1. ✅ **Distractors added** - Creates confusing similar facts
2. ⏳ **Test running** - Comparing with/without distractors
3. 🔜 **Next**: Pull tinyllama and test with weaker model
