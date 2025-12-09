"""
Experiment 1: Needle in Haystack (Lost in the Middle)

This experiment demonstrates the "Lost in the Middle" phenomenon where LLMs
have reduced accuracy for information embedded in the middle of contexts.
"""

from pathlib import Path
from typing import Dict, List, Any
import logging

from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)
from context_windows_lab.data_generation.document_generator import (
    DocumentGenerator,
    Document,
)
from context_windows_lab.llm.ollama_interface import OllamaInterface, LLMResponse
from context_windows_lab.evaluation.accuracy_evaluator import AccuracyEvaluator
from context_windows_lab.evaluation.metrics import calculate_statistics
from context_windows_lab.visualization.plotter import Plotter

logger = logging.getLogger(__name__)


class NeedleInHaystackExperiment(BaseExperiment):
    """
    Experiment 1: Needle in Haystack

    Tests LLM accuracy for facts embedded at different positions:
    - Start of context
    - Middle of context
    - End of context

    Expected result: Accuracy drops in the middle position.
    """

    def __init__(
        self,
        config: ExperimentConfig,
        num_documents: int = 5,
        words_per_document: int = 200,
        fact: str = "The CEO of the company is David Cohen.",
        question: str = "Who is the CEO of the company?",
        expected_answer: str = "David Cohen",
        llm_interface: OllamaInterface = None,
    ):
        """
        Initialize Needle in Haystack experiment.

        Args:
            config: Experiment configuration
            num_documents: Number of documents per position
            words_per_document: Words in each document
            fact: Critical fact to embed
            question: Question to ask LLM
            expected_answer: Expected answer for evaluation
            llm_interface: Optional LLM interface (will create if None)
        """
        super().__init__(config)

        self.num_documents = num_documents
        self.words_per_document = words_per_document
        self.fact = fact
        self.question = question
        self.expected_answer = expected_answer

        # Initialize building blocks
        self.doc_generator = DocumentGenerator(seed=42)
        self.llm = llm_interface or OllamaInterface()
        self.evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)
        self.plotter = Plotter()

        # Test positions
        self.positions = ["start", "middle", "end"]

    def _generate_data(self) -> Dict[str, List[Document]]:
        """
        Generate documents with facts at different positions.

        Returns:
            Dictionary mapping positions to document lists
        """
        data = {}

        for position in self.positions:
            logger.info(
                f"Generating {self.num_documents} documents with fact at {position}"
            )

            documents = self.doc_generator.generate_documents(
                num_docs=self.num_documents,
                words_per_doc=self.words_per_document,
                fact=self.fact,
                fact_position=position,
            )

            data[position] = documents

        return data

    def _execute_queries(
        self, data: Dict[str, List[Document]]
    ) -> Dict[str, List[LLMResponse]]:
        """
        Query LLM for each document.

        Args:
            data: Documents by position

        Returns:
            LLM responses by position
        """
        responses = {}

        for position, documents in data.items():
            logger.info(f"Querying LLM for {position} position documents")
            position_responses = []

            for i, doc in enumerate(documents):
                logger.debug(f"Query {i+1}/{len(documents)} for {position}")

                # Query LLM
                response = self.llm.query(context=doc.content, question=self.question)

                position_responses.append(response)

            responses[position] = position_responses

        return responses

    def _evaluate_responses(
        self, responses: Dict[str, List[LLMResponse]]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate accuracy of responses by position.

        Args:
            responses: LLM responses by position

        Returns:
            List of evaluation results with metadata
        """
        evaluations = []

        for position, position_responses in responses.items():
            for i, response in enumerate(position_responses):
                # Evaluate accuracy
                accuracy = self.evaluator.evaluate(
                    response.text, self.expected_answer
                )

                evaluation = {
                    "position": position,
                    "doc_index": i,
                    "accuracy": accuracy,
                    "latency_ms": response.latency_ms,
                    "tokens_used": response.tokens_used,
                    "response_text": response.text,
                    "success": response.success,
                }

                evaluations.append(evaluation)

                logger.debug(
                    f"Position={position}, Doc={i}, "
                    f"Accuracy={accuracy:.2f}, "
                    f"Latency={response.latency_ms:.0f}ms"
                )

        return evaluations

    def analyze(self) -> Dict[str, Any]:
        """
        Calculate statistics by position.

        Returns:
            Dictionary with mean accuracy, std, etc. by position
        """
        analysis = {}

        for position in self.positions:
            # Filter results for this position
            position_results = [r for r in self.results if r["position"] == position]

            # Extract accuracy scores
            accuracies = [r["accuracy"] for r in position_results]
            latencies = [r["latency_ms"] for r in position_results]

            # Calculate statistics
            acc_stats = calculate_statistics(accuracies)
            lat_stats = calculate_statistics(latencies)

            analysis[position] = {
                "accuracy": {
                    "mean": acc_stats.mean,
                    "std": acc_stats.std,
                    "min": acc_stats.min,
                    "max": acc_stats.max,
                    "count": acc_stats.count,
                    "ci_95": acc_stats.confidence_interval_95,
                },
                "latency_ms": {
                    "mean": lat_stats.mean,
                    "std": lat_stats.std,
                },
            }

            logger.info(
                f"Position '{position}': "
                f"Accuracy={acc_stats.mean:.2f}±{acc_stats.std:.2f}, "
                f"Latency={lat_stats.mean:.0f}±{lat_stats.std:.0f}ms"
            )

        return analysis

    def visualize(self) -> List[Path]:
        """
        Generate bar chart of accuracy by position.

        Returns:
            List with path to visualization
        """
        # Prepare data for plotting
        analysis = self.analyze()

        accuracy_data = {
            position: analysis[position]["accuracy"]["mean"]
            for position in self.positions
        }

        # Create output path
        output_path = self.config.output_dir / "accuracy_by_position.png"

        # Generate bar chart
        self.plotter.plot_bar_chart(
            data=accuracy_data,
            title="Experiment 1: Lost in the Middle - Accuracy by Fact Position",
            xlabel="Fact Position in Context",
            ylabel="Accuracy (0.0 - 1.0)",
            output_path=output_path,
            show_values=True,
        )

        return [output_path]

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"NeedleInHaystackExperiment("
            f"docs={self.num_documents}, "
            f"words={self.words_per_document})"
        )
