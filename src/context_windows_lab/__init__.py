"""
Context Windows Lab - Experimental Framework for LLM Context Management

This package provides tools and experiments for investigating context window
behavior in Large Language Models, including the "Lost in the Middle" phenomenon,
context size impact, RAG effectiveness, and context engineering strategies.
"""

__version__ = "1.0.0"
__author__ = "Lior Livyatan"
__email__ = "lior@example.com"

# Expose key components for easier imports
from context_windows_lab.experiments import (
    BaseExperiment,
    ExperimentConfig,
    NeedleInHaystackExperiment,
)

__all__ = [
    "__version__",
    "__author__",
    "BaseExperiment",
    "ExperimentConfig",
    "NeedleInHaystackExperiment",
]
