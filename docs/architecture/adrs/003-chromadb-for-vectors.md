# ADR 003: Use ChromaDB for Vector Storage in RAG Experiment

## Status
**Accepted** - 2025-12-09

## Context
Experiment 3 (RAG Impact) requires a vector database to:
1. Store document embeddings
2. Perform similarity search for retrieval
3. Compare full context vs RAG approaches

We need to choose a vector database solution that:
- Works locally (no cloud dependency)
- Integrates well with Python
- Supports embedding storage and similarity search
- Has minimal setup requirements
- Is suitable for small-scale experiments (~20 documents, ~40 chunks)

### Options Considered
1. **ChromaDB** - Embedded vector database
2. **Pinecone** - Cloud-based vector database
3. **Weaviate** - Self-hosted vector database
4. **FAISS** - Facebook's similarity search library
5. **Milvus** - Open-source vector database
6. **Qdrant** - Vector search engine

## Decision
We will use **ChromaDB** as the vector database for Experiment 3.

## Rationale

### Why ChromaDB?

**Pros:**
1. **Embedded**: No separate server process required
2. **Zero Setup**: Works out of the box, no configuration
3. **Local-First**: Data stored locally, no cloud dependency
4. **Python-Native**: Excellent Python integration
5. **LangChain Integration**: Official LangChain ChromaDB integration
6. **Lightweight**: Suitable for small datasets
7. **Persistent Storage**: Data saved to disk, survives restarts
8. **MIT License**: Open source, permissive license
9. **Good Documentation**: Clear examples and tutorials
10. **Actively Maintained**: Regular updates and bug fixes

**Cons:**
1. **Not Production-Scale**: Limited to single-machine, modest datasets
2. **Performance**: Slower than specialized solutions for large scale
3. **Features**: Fewer advanced features than Weaviate/Milvus
4. **Query Language**: Simpler query interface

**For Our Use Case:**
- ✓ We have small dataset (20 docs, ~40 chunks)
- ✓ Need simple similarity search (top-k)
- ✓ Educational/experimental context
- ✓ Local execution requirement
- ✓ Easy setup critical for students

### Why Not Alternatives?

#### Pinecone
❌ **Rejected:**
- Cloud-based (requires internet)
- Costs money (free tier has limits)
- Requires API key and account
- Adds external dependency
- Data leaves local machine

✓ **Advantages it has:**
- Production-ready
- Excellent performance
- Managed service (no maintenance)

#### Weaviate
❌ **Rejected:**
- Requires Docker container or separate server
- More complex setup
- Overkill for our scale
- Steeper learning curve

✓ **Advantages it has:**
- Rich query language
- Better for production
- More features (hybrid search, etc.)

#### FAISS
⚠️ **Considered but rejected:**
- Very fast for similarity search
- Facebook-backed, well-tested
- No built-in persistence (need to manage)
- Lower-level API (more code to write)
- No native metadata filtering
- Would require more manual integration

✓ **Better for:**
- Large-scale similarity search
- Performance-critical applications
- When you need fine control

#### Milvus
❌ **Rejected:**
- Requires Docker/Kubernetes deployment
- Production-focused (overkill for experiments)
- More complex architecture
- Harder for students to set up

#### Qdrant
❌ **Rejected:**
- Requires separate server process
- Less mature Python ecosystem
- More setup than ChromaDB
- Fewer LangChain examples

## Consequences

### Positive
1. **Student-Friendly**: Pip install + 3 lines of code to get started
2. **No Setup Barrier**: Works immediately, no Docker/servers
3. **LangChain Compatible**: Seamless integration with LangChain ecosystem
4. **Local Development**: All data stays on machine
5. **Good Enough**: Adequate performance for our dataset size
6. **Clear Examples**: Many tutorials and docs available
7. **Persistent**: Results saved to disk for later analysis

### Negative
1. **Scale Limitations**: Won't work for millions of vectors (not our use case)
2. **Performance**: Slower than specialized solutions (acceptable for experiments)
3. **Features**: Missing advanced features like hybrid search (don't need)
4. **Production Readiness**: Not recommended for production (this is educational)

### Mitigation
- **Scale**: Our dataset is tiny (~40 chunks), ChromaDB handles this easily
- **Performance**: Acceptable latency for experimental purposes (<1s)
- **Features**: We only need basic similarity search (top-k)
- **Production**: This is an educational project, not production system

## Implementation Details

### Installation
```bash
pip install chromadb
```

### Basic Usage
```python
import chromadb

# Create client (persistent storage)
client = chromadb.PersistentClient(path="./.chroma")

# Create or get collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"description": "Hebrew documents for RAG experiment"}
)

# Add documents with embeddings
collection.add(
    documents=chunks,  # Text chunks
    embeddings=embeddings,  # Nomic vectors (768-dim)
    metadatas=metadata,  # Document metadata
    ids=ids  # Unique IDs
)

# Query for similar documents
results = collection.query(
    query_embeddings=[query_vector],
    n_results=3  # Top-3 retrieval
)
```

### Integration with LangChain
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./.chroma"
)

# Retrieval
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.get_relevant_documents(query)
```

### Configuration
```yaml
rag:
  vector_store:
    type: chromadb
    persist_directory: "./.chroma"
    collection_name: "experiment_3_docs"

  chunking:
    chunk_size: 500
    chunk_overlap: 50

  retrieval:
    top_k: 3
    search_type: "similarity"
```

### Storage Location
```
context-windows-lab/
  .chroma/              # ChromaDB persistent storage
    chroma.sqlite3      # SQLite database
    [uuid]/             # Collection data
```

## Testing Strategy

### Unit Tests
```python
def test_chromadb_storage():
    """Test document storage and retrieval"""
    # Setup ChromaDB with test documents
    # Verify documents are stored
    # Query and verify retrieval works
    # Clean up test data

def test_similarity_search():
    """Test top-k similarity search"""
    # Add documents with known similarities
    # Query and verify correct documents returned
    # Verify ranking order
```

### Integration Test
```python
def test_rag_pipeline():
    """Test full RAG pipeline with ChromaDB"""
    # Chunk documents
    # Generate embeddings
    # Store in ChromaDB
    # Perform retrieval
    # Verify end-to-end flow
```

## Performance Expectations

For Experiment 3:
- **Dataset**: 20 documents → ~40 chunks (500 chars each)
- **Embedding**: Nomic embeddings (768 dimensions)
- **Storage Time**: <1 second to store all embeddings
- **Query Time**: <100ms per similarity search
- **Memory**: <100MB for full dataset
- **Disk**: <10MB persistent storage

These are well within ChromaDB's capabilities.

## Alternatives for Future Consideration

If we need to scale up in future versions:

1. **FAISS**: For much larger datasets (100K+ documents)
2. **Weaviate**: For production deployment with advanced features
3. **Qdrant**: For better performance with medium-scale datasets
4. **Cloud Solutions** (Pinecone, Supabase): If cloud deployment is acceptable

But for current requirements, ChromaDB is optimal.

## References
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain ChromaDB Integration](https://python.langchain.com/docs/integrations/vectorstores/chroma)
- [ChromaDB GitHub](https://github.com/chroma-core/chroma)
- [Nomic Embeddings](https://docs.nomic.ai/reference/endpoints/nomic-embed-text)

## Validation Checklist
- [x] Meets local-execution requirement
- [x] Zero-cost solution
- [x] Easy setup for students
- [x] Good Python/LangChain integration
- [x] Adequate performance for dataset size
- [x] Persistent storage for results
- [x] Clear documentation available

## Revision History
- 2025-12-09: Initial decision to use ChromaDB for Experiment 3
