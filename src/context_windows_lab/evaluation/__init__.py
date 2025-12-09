"""
Evaluation Module

Provides tools for evaluating LLM responses and calculating
accuracy metrics.
"""

from context_windows_lab.evaluation.accuracy_evaluator import AccuracyEvaluator
from context_windows_lab.evaluation.metrics import calculate_statistics

__all__ = [
    "AccuracyEvaluator",
    "calculate_statistics",
]
