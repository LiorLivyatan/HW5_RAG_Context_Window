"""
Vector Store for RAG

Provides simple vector storage and retrieval capabilities using ChromaDB.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional

try:
    import chromadb
    from chromadb.config import Settings

    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available. Install with: pip install chromadb")

logger = logging.getLogger(__name__)


@dataclass
class RetrievedDocument:
    """A document retrieved from vector store."""

    content: str
    score: float  # Similarity score (higher = more relevant)
    metadata: dict


class VectorStore:
    """
    Simple vector store using ChromaDB.

    Stores document embeddings and retrieves relevant documents based on queries.
    For simplicity, uses ChromaDB's built-in embedding function.
    """

    def __init__(self, collection_name: str = "documents", persist_directory: Optional[str] = None):
        """
        Initialize vector store.

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist embeddings (None = in-memory)
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError(
                "ChromaDB is required for RAG functionality. " "Install with: pip install chromadb"
            )

        self.collection_name = collection_name

        # Create ChromaDB client
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
            logger.info(f"Created persistent vector store at {persist_directory}")
        else:
            self.client = chromadb.Client(Settings(anonymized_telemetry=False))
            logger.info("Created in-memory vector store")

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection '{collection_name}'")
        except Exception:
            self.collection = self.client.create_collection(name=collection_name)
            logger.info(f"Created new collection '{collection_name}'")

    def add_documents(self, documents: List[str], metadatas: Optional[List[dict]] = None) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
        """
        if not documents:
            logger.warning("No documents to add")
            return

        # Generate IDs
        ids = [f"doc_{i}" for i in range(len(documents))]

        # Add to collection
        if metadatas:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        else:
            self.collection.add(documents=documents, ids=ids)

        logger.info(f"Added {len(documents)} documents to collection '{self.collection_name}'")

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievedDocument]:
        """
        Retrieve most relevant documents for a query.

        Args:
            query: Query text
            top_k: Number of documents to retrieve

        Returns:
            List of retrieved documents with scores
        """
        results = self.collection.query(query_texts=[query], n_results=top_k)

        # Parse results
        retrieved = []

        if results["documents"] and results["documents"][0]:
            documents = results["documents"][0]
            distances = results["distances"][0]
            metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(documents)

            for doc, distance, metadata in zip(documents, distances, metadatas):
                # Convert distance to similarity score (lower distance = higher similarity)
                # ChromaDB returns L2 distance, so we invert it
                similarity = 1.0 / (1.0 + distance)

                retrieved.append(
                    RetrievedDocument(content=doc, score=similarity, metadata=metadata or {})
                )

        logger.info(f"Retrieved {len(retrieved)} documents for query (top_k={top_k})")
        return retrieved

    def clear(self) -> None:
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(name=self.collection_name)
            logger.info(f"Cleared collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")

    def count(self) -> int:
        """Get number of documents in collection."""
        return self.collection.count()

    def __repr__(self) -> str:
        """String representation."""
        return f"VectorStore(collection='{self.collection_name}', count={self.count()})"
