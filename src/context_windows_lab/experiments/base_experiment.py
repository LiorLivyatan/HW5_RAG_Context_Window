"""
Base Experiment - Abstract Base Class for All Experiments

This module provides the BaseExperiment class that all experiments inherit from,
implementing the Template Method pattern.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
import json
import multiprocessing
import os

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    """Configuration for an experiment."""

    name: str
    output_dir: Path
    iterations: int = 3
    save_results: bool = True
    generate_visualizations: bool = True
    use_multiprocessing: bool = False
    max_workers: Optional[int] = None  # None = use CPU count


@dataclass
class ExperimentResults:
    """Results from an experiment execution."""

    experiment_name: str
    config: ExperimentConfig
    raw_results: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    visualization_paths: List[Path]
    success: bool
    error: Optional[str] = None


class BaseExperiment(ABC):
    """
    Abstract base class for all experiments.

    Implements the Template Method pattern where the run() method defines
    the experiment execution flow, and subclasses implement specific steps.

    All experiments follow this structure:
    1. Setup (load config, initialize building blocks)
    2. Generate data
    3. Execute queries
    4. Evaluate responses
    5. Analyze results (calculate statistics)
    6. Visualize results
    7. Save results
    """

    def __init__(self, config: ExperimentConfig):
        """
        Initialize base experiment.

        Args:
            config: Experiment configuration
        """
        self.config = config
        self.results: List[Dict[str, Any]] = []

        # Ensure output directory exists
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized {self.config.name}")

    def run(self) -> ExperimentResults:
        """
        Run the complete experiment (Template Method).

        This method defines the overall experiment flow. Subclasses should
        implement the specific steps (_generate_data, _execute_queries, etc.)

        If config.iterations > 1 and use_multiprocessing=True, runs multiple
        iterations in parallel using multiprocessing.Pool.

        Returns:
            ExperimentResults with all data and visualizations
        """
        logger.info(f"Starting experiment: {self.config.name}")

        # Check if we should run multiple iterations with multiprocessing
        if self.config.iterations > 1 and self.config.use_multiprocessing:
            return self._run_parallel_iterations()

        try:
            # Step 1: Generate test data
            logger.info("Step 1: Generating data...")
            data = self._generate_data()

            # Step 2: Execute queries
            logger.info("Step 2: Executing queries...")
            responses = self._execute_queries(data)

            # Step 3: Evaluate responses
            logger.info("Step 3: Evaluating responses...")
            evaluations = self._evaluate_responses(responses)

            # Store results
            self.results = evaluations

            # Step 4: Analyze results (calculate statistics)
            logger.info("Step 4: Analyzing results...")
            statistics = self.analyze()

            # Step 5: Visualize results
            visualization_paths = []
            if self.config.generate_visualizations:
                logger.info("Step 5: Generating visualizations...")
                visualization_paths = self.visualize()

            # Step 6: Save results
            if self.config.save_results:
                logger.info("Step 6: Saving results...")
                self._save_results(statistics)

            logger.info(f"Experiment '{self.config.name}' completed successfully")

            return ExperimentResults(
                experiment_name=self.config.name,
                config=self.config,
                raw_results=self.results,
                statistics=statistics,
                visualization_paths=visualization_paths,
                success=True,
            )

        except Exception as e:
            logger.error(f"Experiment '{self.config.name}' failed: {e}", exc_info=True)

            return ExperimentResults(
                experiment_name=self.config.name,
                config=self.config,
                raw_results=self.results,
                statistics={},
                visualization_paths=[],
                success=False,
                error=str(e),
            )

    @abstractmethod
    def _generate_data(self) -> Any:
        """
        Generate test data for the experiment.

        Returns:
            Generated data (format depends on experiment)
        """
        pass

    @abstractmethod
    def _execute_queries(self, data: Any) -> Any:
        """
        Execute LLM queries with generated data.

        Args:
            data: Data from _generate_data()

        Returns:
            Query responses
        """
        pass

    @abstractmethod
    def _evaluate_responses(self, responses: Any) -> List[Dict[str, Any]]:
        """
        Evaluate LLM responses for accuracy.

        Args:
            responses: Responses from _execute_queries()

        Returns:
            List of evaluation results with metadata
        """
        pass

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze experiment results and calculate statistics.

        Returns:
            Dictionary with statistical analysis
        """
        pass

    @abstractmethod
    def visualize(self) -> List[Path]:
        """
        Generate visualizations from experiment results.

        Returns:
            List of paths to generated visualization files
        """
        pass

    def _save_results(self, statistics: Dict[str, Any]) -> None:
        """
        Save experiment results to file.

        Args:
            statistics: Statistical analysis results
        """
        output_file = self.config.output_dir / "results.json"

        data = {
            "experiment": self.config.name,
            "config": {
                "iterations": self.config.iterations,
            },
            "raw_results": self.results,
            "statistics": statistics,
        }

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Results saved to {output_file}")

    def _run_parallel_iterations(self) -> ExperimentResults:
        """
        Run multiple experiment iterations in parallel using multiprocessing.

        This method uses multiprocessing.Pool to run iterations concurrently,
        significantly improving performance for CPU-bound experiment operations.

        Returns:
            ExperimentResults with aggregated data from all iterations
        """
        logger.info(
            f"Running {self.config.iterations} iterations in parallel "
            f"(max_workers={self.config.max_workers or 'CPU count'})"
        )

        # Determine number of workers
        max_workers = self.config.max_workers or multiprocessing.cpu_count()

        # Create a pool of workers
        with multiprocessing.Pool(processes=max_workers) as pool:
            # Run iterations in parallel
            # Note: We pass iteration number to allow different seeds
            iteration_results = pool.map(
                self._run_single_iteration,
                range(self.config.iterations)
            )

        # Aggregate results from all iterations
        logger.info("Aggregating results from parallel iterations...")

        all_results = []
        for iter_result in iteration_results:
            if iter_result:
                all_results.extend(iter_result)

        self.results = all_results

        # Analyze aggregated results
        statistics = self.analyze()

        # Visualize
        visualization_paths = []
        if self.config.generate_visualizations:
            logger.info("Generating visualizations from aggregated results...")
            visualization_paths = self.visualize()

        # Save
        if self.config.save_results:
            logger.info("Saving aggregated results...")
            self._save_results(statistics)

        logger.info(
            f"Parallel experiment '{self.config.name}' completed successfully "
            f"({self.config.iterations} iterations)"
        )

        return ExperimentResults(
            experiment_name=self.config.name,
            config=self.config,
            raw_results=self.results,
            statistics=statistics,
            visualization_paths=visualization_paths,
            success=True,
        )

    def _run_single_iteration(self, iteration: int) -> List[Dict[str, Any]]:
        """
        Run a single experiment iteration.

        This method is called by multiprocessing workers. It runs one complete
        experiment iteration and returns the raw results.

        Args:
            iteration: Iteration number (used for logging and seeding)

        Returns:
            List of result dictionaries from this iteration
        """
        try:
            logger.info(f"Starting iteration {iteration + 1}/{self.config.iterations}")

            # Generate data
            data = self._generate_data()

            # Execute queries
            responses = self._execute_queries(data)

            # Evaluate responses
            results = self._evaluate_responses(responses)

            logger.info(f"Iteration {iteration + 1} completed successfully")
            return results

        except Exception as e:
            logger.error(f"Iteration {iteration + 1} failed: {e}", exc_info=True)
            return []

    def __repr__(self) -> str:
        """String representation of experiment."""
        return f"{self.__class__.__name__}(name='{self.config.name}')"
