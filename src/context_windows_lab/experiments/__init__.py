"""
Experiments Module

Contains all 4 experiment implementations plus base experiment class.
"""

from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
    ExperimentResults,
)
from context_windows_lab.experiments.exp1_needle_haystack import (
    NeedleInHaystackExperiment,
)
from context_windows_lab.experiments.exp2_context_size import ContextSizeExperiment

# TODO: Implement remaining experiments
# from context_windows_lab.experiments.exp3_rag_impact import RAGImpactExperiment
# from context_windows_lab.experiments.exp4_engineering_strategies import (
#     EngineeringStrategiesExperiment,
# )

__all__ = [
    "BaseExperiment",
    "ExperimentConfig",
    "ExperimentResults",
    "NeedleInHaystackExperiment",
    "ContextSizeExperiment",
]
