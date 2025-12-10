"""
Metrics Module - Statistical Calculations for Evaluation

Provides utility functions for calculating statistics from experiment results.
"""

import math
from dataclasses import dataclass
from typing import List


@dataclass
class Statistics:
    """Statistical summary of a dataset."""

    mean: float
    std: float
    min: float
    max: float
    count: int
    confidence_interval_95: tuple


def calculate_statistics(scores: List[float]) -> Statistics:
    """
    Calculate comprehensive statistics for a list of scores.

    Args:
        scores: List of numerical scores

    Returns:
        Statistics object with mean, std, min, max, etc.

    Raises:
        ValueError: If scores list is empty
    """
    if not scores:
        raise ValueError("Cannot calculate statistics for empty list")

    n = len(scores)
    mean_val = sum(scores) / n

    # Calculate standard deviation
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in scores) / (n - 1)
        std_val = math.sqrt(variance)

        # Calculate 95% confidence interval
        # Using t-distribution approximation (z=1.96 for large n)
        margin = 1.96 * (std_val / math.sqrt(n))
        ci_95 = (mean_val - margin, mean_val + margin)
    else:
        std_val = 0.0
        ci_95 = (mean_val, mean_val)

    return Statistics(
        mean=mean_val,
        std=std_val,
        min=min(scores),
        max=max(scores),
        count=n,
        confidence_interval_95=ci_95,
    )
