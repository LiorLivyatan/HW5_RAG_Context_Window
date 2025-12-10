"""
Experiment 1: Needle in Haystack (Lost in the Middle)

This experiment demonstrates the "Lost in the Middle" phenomenon where LLMs
have reduced accuracy for information embedded in the middle of contexts.
"""

import logging
import random
from pathlib import Path
from typing import Any, Dict, List

from context_windows_lab.data_generation.document_generator import (
    Document,
    DocumentGenerator,
)
from context_windows_lab.evaluation.accuracy_evaluator import AccuracyEvaluator
from context_windows_lab.evaluation.metrics import calculate_statistics
from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)
from context_windows_lab.llm.ollama_interface import LLMResponse, OllamaInterface
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
        add_distractors: bool = False,
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
            add_distractors: Whether to add confusing similar facts (default: False)
        """
        super().__init__(config)

        self.num_documents = num_documents
        self.words_per_document = words_per_document
        self.fact = fact
        self.question = question
        self.expected_answer = expected_answer
        self.add_distractors = add_distractors

        # Initialize building blocks
        self.doc_generator = DocumentGenerator(seed=42, add_distractors=add_distractors)
        self.llm = llm_interface or OllamaInterface()
        self.evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)
        self.plotter = Plotter()

        # Test positions
        self.positions = ["start", "middle", "end"]

    def _generate_data(self) -> List[Document]:
        """
        Generate documents with facts at randomly chosen positions.

        Matches assignment pseudocode:
        - Generate num_docs documents (default 5)
        - Each document randomly gets fact at start/middle/end

        Returns:
            List of documents with random fact positions
        """
        logger.info(f"Generating {self.num_documents} documents with randomly positioned facts")

        documents = []

        for i in range(self.num_documents):
            # Randomly choose position for THIS document (matches pseudocode)
            fact_position = random.choice(["start", "middle", "end"])

            # Generate single document with fact at chosen position
            doc = self.doc_generator.generate_documents(
                num_docs=1,
                words_per_doc=self.words_per_document,
                fact=self.fact,
                fact_position=fact_position,
            )[
                0
            ]  # Take the single generated document

            documents.append(doc)

            logger.debug(f"Document {i+1}/{self.num_documents}: fact at '{fact_position}'")

        # Log distribution of positions
        position_counts = {}
        for doc in documents:
            pos = doc.fact_position
            position_counts[pos] = position_counts.get(pos, 0) + 1

        logger.info(f"Position distribution: {position_counts}")

        # Store for later access in _evaluate_responses
        self.documents = documents

        return documents

    def _execute_queries(self, data: List[Document]) -> List[LLMResponse]:
        """
        Query LLM for each document.

        Matches assignment pseudocode:
        - Iterate through all documents
        - Query each document with same question
        - Return list of responses (will be grouped by position later)

        Args:
            data: List of documents with random fact positions

        Returns:
            List of LLM responses (same order as documents)
        """
        logger.info(f"Querying LLM for {len(data)} documents")
        responses = []

        for i, doc in enumerate(data):
            logger.debug(f"Query {i+1}/{len(data)}: fact at '{doc.fact_position}'")

            # Query LLM with document content
            response = self.llm.query(context=doc.content, question=self.question)

            responses.append(response)

        logger.info(f"Completed {len(responses)} queries")
        return responses

    def _evaluate_responses(self, responses: List[LLMResponse]) -> List[Dict[str, Any]]:
        """
        Evaluate accuracy of responses and group by fact position.

        Matches assignment pseudocode:
        - Pair each document with its response
        - Evaluate accuracy
        - Include fact_position from document for later grouping

        Args:
            responses: List of LLM responses (same order as documents)

        Returns:
            List of evaluation results with metadata
        """
        evaluations = []

        # Pair documents with responses and evaluate
        for i, (doc, response) in enumerate(zip(self.documents, responses)):
            # Evaluate accuracy
            accuracy = self.evaluator.evaluate(response.text, self.expected_answer)

            evaluation = {
                "position": doc.fact_position,  # Get from document
                "doc_index": i,
                "accuracy": accuracy,
                "latency_ms": response.latency_ms,
                "tokens_used": response.tokens_used,
                "response_text": response.text,
                "success": response.success,
            }

            evaluations.append(evaluation)

            logger.debug(
                f"Doc {i+1}/{len(self.documents)}: position='{doc.fact_position}', "
                f"accuracy={accuracy:.2f}, "
                f"latency={response.latency_ms:.0f}ms"
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
            position: analysis[position]["accuracy"]["mean"] for position in self.positions
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
