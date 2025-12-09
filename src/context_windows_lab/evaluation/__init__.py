"""
Evaluation Module

Provides tools for evaluating LLM responses and calculating
accuracy metrics.
"""

from context_windows_lab.evaluation.accuracy_evaluator import (
    AccuracyEvaluator,
    EvaluationResult,
)
from context_windows_lab.evaluation.metrics import calculate_statistics, Statistics

__all__ = [
    "AccuracyEvaluator",
    "EvaluationResult",
    "calculate_statistics",
    "Statistics",
]
