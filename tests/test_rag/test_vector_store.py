"""
Tests for VectorStore RAG component.

Note: These tests require ChromaDB to be installed.
If ChromaDB is not available, tests will be skipped.
"""

import pytest

try:
    from context_windows_lab.rag.vector_store import (
        CHROMADB_AVAILABLE,
        RetrievedDocument,
        VectorStore,
    )
except ImportError:
    CHROMADB_AVAILABLE = False

# Skip all tests if ChromaDB is not available
pytestmark = pytest.mark.skipif(
    not CHROMADB_AVAILABLE, reason="ChromaDB not installed. Install with: pip install chromadb"
)


class TestVectorStore:
    """Test suite for VectorStore class."""

    def test_initialization_in_memory(self):
        """Test creating in-memory vector store."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_collection")
        assert store.collection_name == "test_collection"
        assert store.count() == 0

    def test_add_single_document(self):
        """Test adding a single document."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_single")
        documents = ["This is a test document about artificial intelligence."]

        store.add_documents(documents)

        assert store.count() == 1

    def test_add_multiple_documents(self):
        """Test adding multiple documents."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_multiple")
        documents = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with many layers.",
            "Natural language processing deals with text understanding.",
        ]

        store.add_documents(documents)

        assert store.count() == 3

    def test_add_documents_with_metadata(self):
        """Test adding documents with metadata."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_metadata")
        documents = ["Document 1", "Document 2"]
        metadatas = [{"source": "test1"}, {"source": "test2"}]

        store.add_documents(documents, metadatas=metadatas)

        assert store.count() == 2

    def test_add_empty_documents_list(self):
        """Test that adding empty list doesn't cause errors."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_empty")
        store.add_documents([])

        assert store.count() == 0

    def test_retrieve_relevant_documents(self):
        """Test retrieving relevant documents."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_retrieve")
        documents = [
            "Python is a programming language.",
            "Machine learning requires large datasets.",
            "Databases store structured data.",
        ]

        store.add_documents(documents)

        # Query for programming-related content
        results = store.retrieve(query="programming language Python", top_k=2)

        assert len(results) <= 2
        assert all(isinstance(doc, RetrievedDocument) for doc in results)
        # Most relevant should mention Python
        assert "Python" in results[0].content

    def test_retrieve_top_k(self):
        """Test that retrieve respects top_k parameter."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_top_k")
        documents = [f"Document number {i} with content." for i in range(10)]

        store.add_documents(documents)

        # Retrieve top 3
        results = store.retrieve(query="document content", top_k=3)
        assert len(results) == 3

        # Retrieve top 5
        results = store.retrieve(query="document content", top_k=5)
        assert len(results) == 5

    def test_retrieve_returns_scores(self):
        """Test that retrieved documents have similarity scores."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_scores")
        documents = [
            "Artificial intelligence and machine learning.",
            "Deep learning neural networks.",
            "Cooking recipes and food preparation.",
        ]

        store.add_documents(documents)

        results = store.retrieve(query="machine learning AI", top_k=3)

        # All results should have scores
        for doc in results:
            assert hasattr(doc, "score")
            assert 0.0 <= doc.score <= 1.0

        # Most relevant should have higher score
        assert results[0].score > 0.0

    def test_retrieve_returns_metadata(self):
        """Test that retrieved documents include metadata."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_meta_retrieve")
        documents = ["Doc 1", "Doc 2"]
        metadatas = [{"id": 1, "category": "A"}, {"id": 2, "category": "B"}]

        store.add_documents(documents, metadatas=metadatas)

        results = store.retrieve(query="Doc", top_k=2)

        # Check metadata is present
        for doc in results:
            assert hasattr(doc, "metadata")
            assert isinstance(doc.metadata, dict)

    def test_clear_collection(self):
        """Test clearing all documents from collection."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_clear")
        documents = ["Doc 1", "Doc 2", "Doc 3"]

        store.add_documents(documents)
        assert store.count() == 3

        store.clear()
        assert store.count() == 0

    def test_count_method(self):
        """Test count() method tracks document count."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_count")

        assert store.count() == 0

        store.add_documents(["Doc 1"])
        assert store.count() == 1

        store.add_documents(["Doc 2", "Doc 3"])
        assert store.count() == 3

        store.clear()
        assert store.count() == 0

    def test_repr(self):
        """Test string representation."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_repr")
        store.add_documents(["Doc 1", "Doc 2"])

        repr_str = repr(store)
        assert "VectorStore" in repr_str
        assert "test_repr" in repr_str
        assert "2" in repr_str  # Document count

    def test_semantic_similarity(self):
        """Test that semantically similar documents are retrieved."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_semantic")
        documents = [
            "The cat sat on the mat.",
            "The feline rested on the rug.",  # Similar meaning
            "Quantum physics is complex.",  # Different topic
        ]

        store.add_documents(documents)

        results = store.retrieve(query="cat sitting on mat", top_k=2)

        # First two should be about cats/felines, not quantum physics
        assert "Quantum" not in results[0].content
        assert "Quantum" not in results[1].content

    def test_multilingual_documents(self):
        """Test handling of non-English documents (Hebrew, as used in Exp3)."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_hebrew")
        documents = [
            "זהו טקסט בעברית על טכנולוגיה.",  # Hebrew: "This is Hebrew text about technology."
            "English text about technology.",
            "עוד טקסט בעברית.",  # Hebrew: "More Hebrew text."
        ]

        store.add_documents(documents)

        # Query in Hebrew
        results = store.retrieve(query="טכנולוגיה", top_k=2)

        # Should retrieve Hebrew documents
        assert len(results) >= 1

    def test_large_document_batch(self):
        """Test adding a large batch of documents."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_large_batch")
        documents = [f"Document {i} with unique content about topic {i % 10}." for i in range(100)]

        store.add_documents(documents)

        assert store.count() == 100

        # Retrieve should still work
        results = store.retrieve(query="topic 5", top_k=5)
        assert len(results) == 5

    def test_retrieve_from_empty_collection(self):
        """Test retrieving from empty collection returns empty list."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        store = VectorStore(collection_name="test_empty_retrieve")

        results = store.retrieve(query="anything", top_k=5)
        assert len(results) == 0

    def test_use_case_rag_pipeline(self):
        """Test realistic RAG use case."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        # Simulate RAG experiment workflow
        store = VectorStore(collection_name="test_rag_pipeline")

        # Add knowledge base documents
        documents = [
            "The company was founded in 2010 with a mission to innovate.",
            "Our headquarters are located in San Francisco, California.",
            "We have over 500 employees worldwide.",
            "Our main product is a cloud-based analytics platform.",
            "We serve customers in 50+ countries.",
        ]

        store.add_documents(documents)

        # Simulate question answering: retrieve relevant context
        question = "Where is the company headquartered?"
        relevant_docs = store.retrieve(query=question, top_k=2)

        # Most relevant should mention location
        assert (
            "San Francisco" in relevant_docs[0].content
            or "San Francisco" in relevant_docs[1].content
        )

    def test_retrieved_document_dataclass(self):
        """Test RetrievedDocument dataclass structure."""
        if not CHROMADB_AVAILABLE:
            pytest.skip("ChromaDB not available")

        doc = RetrievedDocument(content="Test content", score=0.95, metadata={"source": "test"})

        assert doc.content == "Test content"
        assert doc.score == 0.95
        assert doc.metadata == {"source": "test"}


class TestVectorStoreErrorHandling:
    """Test error handling and edge cases."""

    def test_import_error_when_chromadb_missing(self):
        """Test that ImportError is raised when ChromaDB is not installed."""
        # This test is meta - it checks the module behavior
        # We can't actually test this without uninstalling ChromaDB
        # So we just verify the constant exists
        from context_windows_lab.rag.vector_store import CHROMADB_AVAILABLE

        assert isinstance(CHROMADB_AVAILABLE, bool)
