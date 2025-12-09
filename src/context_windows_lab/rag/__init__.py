"""
RAG (Retrieval-Augmented Generation) Module

Provides components for chunking, embedding, vector storage,
and retrieval for RAG experiments.
"""

from context_windows_lab.rag.vector_store import VectorStore, RetrievedDocument

__all__ = [
    "VectorStore",
    "RetrievedDocument",
]
