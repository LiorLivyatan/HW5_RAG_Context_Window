"""
Data Generation Module

Provides tools for generating synthetic documents and test data
for context window experiments.
"""

from context_windows_lab.data_generation.document_generator import (
    DocumentGenerator,
    Document,
)

__all__ = [
    "DocumentGenerator",
    "Document",
]
