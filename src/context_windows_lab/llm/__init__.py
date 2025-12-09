"""
LLM Interface Module

Provides interface for querying Ollama and managing LLM interactions.
"""

from context_windows_lab.llm.ollama_interface import OllamaInterface
from context_windows_lab.llm.response_parser import ResponseParser

__all__ = [
    "OllamaInterface",
    "ResponseParser",
]
