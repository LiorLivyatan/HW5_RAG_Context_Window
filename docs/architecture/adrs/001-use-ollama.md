# ADR 001: Use Ollama for Local LLM

## Status
**Accepted** - 2025-12-09

## Context
The Context Windows Lab requires a Large Language Model (LLM) to conduct experiments on context window behavior. We need to decide between:
1. Cloud-based APIs (OpenAI, Anthropic Claude, Google Gemini)
2. Local LLM solutions (Ollama, LM Studio, llama.cpp)
3. Self-hosted inference servers (vLLM, Text Generation Inference)

### Requirements
- Must support context window experiments with varying sizes
- Must be accessible for academic/educational use
- Should be cost-effective or free
- Must provide consistent, reproducible results
- Should work offline without internet dependency
- Must support temperature=0.0 for deterministic outputs

## Decision
We will use **Ollama** as our LLM solution, specifically running the `llama2` model locally.

## Rationale

### Why Ollama?

**Pros:**
1. **Zero Cost**: No API fees, unlimited queries
2. **Privacy**: All data stays local, no external data transmission
3. **Reproducibility**: Same model version produces consistent results
4. **No Rate Limits**: Can run as many iterations as needed for statistical significance
5. **Offline Operation**: Works without internet connection
6. **Easy Setup**: Simple installation process (`ollama run llama2`)
7. **Good Python Integration**: Official `ollama-python` client library
8. **Suitable Performance**: llama2 provides adequate quality for our experiments
9. **Educational Value**: Students learn about local LLM deployment
10. **No Account Required**: No sign-ups, API keys, or authentication hassles

**Cons:**
1. **Hardware Requirements**: Needs sufficient RAM and CPU (8-16GB RAM minimum)
2. **Slower Than Cloud**: Local inference is slower than optimized cloud APIs
3. **Model Limitations**: llama2 is not state-of-the-art (but sufficient for our purposes)
4. **Setup Required**: Users must install Ollama before running experiments

### Why Not Cloud APIs?

**OpenAI GPT-4:**
- ❌ Cost: $0.03-$0.06 per 1K tokens (experiments would cost $50-100)
- ❌ Rate limits: 3500 RPM limits would slow down experiments
- ❌ Internet required: Can't work offline
- ❌ Data privacy: Prompts sent to external servers
- ✓ Best quality responses

**Anthropic Claude:**
- ❌ Similar cost and limitations as OpenAI
- ❌ Requires API key and account
- ✓ Excellent context window handling (but defeats purpose of demonstrating limitations)

**Google Gemini:**
- ❌ Less mature Python SDK
- ❌ Similar cost considerations
- ✓ Free tier available (but limited)

### Why Not Other Local Solutions?

**LM Studio:**
- ✓ Good UI
- ❌ Less suitable for headless/CLI automation
- ❌ Worse Python integration

**llama.cpp:**
- ✓ Very fast
- ❌ Lower-level, more complex to integrate
- ❌ Requires model file management

**vLLM / TGI:**
- ❌ Overkill for this use case
- ❌ More complex setup
- ✓ Better for production scenarios

## Consequences

### Positive
1. **Student-Friendly**: Easy to set up and use
2. **Cost-Free**: No budget constraints on experimentation
3. **Reproducible**: Same environment and model for all users
4. **Educational**: Students learn about local LLM deployment
5. **Privacy-Preserving**: No data leaves the machine
6. **Flexible**: Can run as many iterations as needed

### Negative
1. **Performance**: Slower than cloud APIs (experiments take longer)
2. **Hardware Dependency**: Requires sufficient local compute resources
3. **Model Quality**: llama2 is not cutting-edge (but adequate)
4. **Setup Barrier**: Users must install Ollama first

### Mitigation Strategies
- **Performance**: Use multiprocessing to parallelize iterations
- **Hardware**: Document minimum requirements clearly in README
- **Model Quality**: Focus on relative comparisons, not absolute quality
- **Setup**: Provide clear installation instructions with troubleshooting

## Implementation Notes

### Configuration
```yaml
ollama:
  base_url: http://localhost:11434
  model: llama2
  temperature: 0.0  # Deterministic outputs
  max_tokens: 500
  timeout: 60
```

### Connection Check
System will verify Ollama availability at startup:
```python
def check_ollama_available():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return response.status_code == 200
    except:
        raise RuntimeError("Ollama not available. Please start Ollama service.")
```

### Model Download
If llama2 is not downloaded, provide helpful error:
```
Error: Model 'llama2' not found.
Please run: ollama pull llama2
```

## Alternatives Considered

### Alternative 1: Hybrid Approach (Ollama + Optional Cloud)
Allow users to configure either Ollama or cloud APIs via environment variables.

**Rejected because:**
- Adds complexity to codebase
- Reduces reproducibility (different users, different results)
- Cloud APIs would demonstrate phenomena differently
- Not aligned with "zero-cost" project goal

### Alternative 2: Use GPT-4 with Free Tier
Use OpenAI's free tier or credits.

**Rejected because:**
- Free tier has strict limits
- Not sustainable for all students
- Still requires internet and API keys
- Creates dependency on external service

## References
- [Ollama Documentation](https://ollama.ai/docs)
- [llama2 Model Card](https://github.com/facebookresearch/llama)
- [ollama-python GitHub](https://github.com/ollama/ollama-python)

## Revision History
- 2025-12-09: Initial decision to use Ollama with llama2
