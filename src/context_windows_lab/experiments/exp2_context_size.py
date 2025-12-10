"""
Experiment 2: Context Size Impact

This experiment investigates how increasing context size affects LLM accuracy.
It varies the number of documents while keeping the fact position constant (middle).

Research Question:
- How does context window size impact the model's ability to retrieve information?
- At what context size does accuracy start to degrade?
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from context_windows_lab.data_generation import Document, DocumentGenerator
from context_windows_lab.evaluation import AccuracyEvaluator, calculate_statistics
from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)
from context_windows_lab.llm import LLMResponse, OllamaInterface
from context_windows_lab.visualization import Plotter

logger = logging.getLogger(__name__)


class ContextSizeExperiment(BaseExperiment):
    """
    Experiment 2: Context Size Impact.

    Tests how varying the number of documents (context size) affects
    the model's ability to retrieve a fact embedded in the middle.
    """

    def __init__(
        self,
        config: ExperimentConfig,
        document_counts: List[int] = None,
        words_per_document: int = 200,
        fact: str = "The project deadline is December 15th, 2025.",
        question: str = "When is the project deadline?",
        expected_answer: str = "December 15th, 2025",
        fact_position: str = "middle",
        llm_interface: OllamaInterface = None,
    ):
        """
        Initialize Experiment 2.

        Args:
            config: Experiment configuration
            document_counts: List of document counts to test (e.g., [5, 10, 20, 50])
            words_per_document: Words per document
            fact: Critical fact to embed
            question: Question to ask about the fact
            expected_answer: Expected answer to the question
            fact_position: Position of fact (default: "middle")
            llm_interface: Optional LLM interface (will create if None)
        """
        super().__init__(config)

        self.document_counts = document_counts or [5, 10, 20, 50]
        self.words_per_document = words_per_document
        self.fact = fact
        self.question = question
        self.expected_answer = expected_answer
        self.fact_position = fact_position

        # Initialize building blocks
        self.doc_generator = DocumentGenerator(seed=42)
        self.llm = llm_interface or OllamaInterface()
        self.evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)
        self.plotter = Plotter()

        logger.info(
            f"Initialized Context Size Experiment with document counts: {self.document_counts}"
        )

    def _generate_data(self) -> Dict[int, List[Document]]:
        """
        Generate documents for each document count.

        Returns:
            Dictionary mapping document count to list of documents
        """
        logger.info("Generating documents for different context sizes...")
        data = {}

        for count in self.document_counts:
            logger.info(f"Generating {count} documents with fact at {self.fact_position}")

            documents = self.doc_generator.generate_documents(
                num_docs=count,
                words_per_doc=self.words_per_document,
                fact=self.fact,
                fact_position=self.fact_position,
            )

            data[count] = documents

        return data

    def _execute_queries(self, data: Dict[int, List[Document]]) -> Dict[int, List[LLMResponse]]:
        """
        Execute LLM queries for each document count.

        Args:
            data: Dictionary mapping document count to documents

        Returns:
            Dictionary mapping document count to list of responses
        """
        logger.info("Executing LLM queries for each context size...")
        responses = {}

        for count, documents in data.items():
            logger.info(f"Querying LLM with {count} documents")

            # Build context from all documents
            context = "\n\n".join([doc.content for doc in documents])

            # Query the LLM
            logger.debug(f"Context size: {len(context)} characters, {len(context.split())} words")
            response = self.llm.query(context=context, question=self.question)

            responses[count] = response

        return responses

    def _evaluate_responses(self, responses: Dict[int, LLMResponse]) -> List[Dict[str, Any]]:
        """
        Evaluate responses and store results.

        Args:
            responses: Dictionary mapping document count to LLM response

        Returns:
            List of result dictionaries
        """
        logger.info("Evaluating responses...")

        for count, response in responses.items():
            if response.success:
                accuracy = self.evaluator.evaluate(response.text, self.expected_answer)

                result = {
                    "document_count": count,
                    "accuracy": accuracy,
                    "latency_ms": response.latency_ms,
                    "tokens_used": response.tokens_used,
                    "response_text": response.text,
                    "success": True,
                }

                logger.debug(
                    f"Count={count}, Accuracy={accuracy:.2f}, Latency={response.latency_ms:.0f}ms"
                )
            else:
                result = {
                    "document_count": count,
                    "accuracy": 0.0,
                    "latency_ms": 0.0,
                    "tokens_used": 0,
                    "response_text": "",
                    "success": False,
                    "error": response.error,
                }

                logger.warning(f"Query failed for count={count}: {response.error}")

            self.results.append(result)

        return self.results

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze results across different document counts.

        Returns:
            Dictionary containing analysis by document count
        """
        logger.info("Analyzing results across context sizes...")

        analysis = {}

        for count in self.document_counts:
            # Get results for this document count
            count_results = [r for r in self.results if r["document_count"] == count]

            if not count_results:
                continue

            # Calculate statistics
            accuracies = [r["accuracy"] for r in count_results]
            latencies = [r["latency_ms"] for r in count_results]
            tokens = [r["tokens_used"] for r in count_results]

            acc_stats = calculate_statistics(accuracies)
            lat_stats = calculate_statistics(latencies)
            tok_stats = calculate_statistics(tokens)

            analysis[count] = {
                "accuracy": {
                    "mean": acc_stats.mean,
                    "std": acc_stats.std,
                    "ci_95": acc_stats.confidence_interval_95,
                },
                "latency_ms": {"mean": lat_stats.mean, "std": lat_stats.std},
                "tokens_used": {"mean": tok_stats.mean, "std": tok_stats.std},
            }

            logger.info(
                f"Count {count}: Accuracy={acc_stats.mean:.2f}±{acc_stats.std:.2f}, "
                f"Latency={lat_stats.mean:.0f}±{lat_stats.std:.0f}ms"
            )

        return analysis

    def visualize(self) -> List[Path]:
        """
        Generate visualizations for context size impact.

        Returns:
            List of paths to generated visualizations
        """
        logger.info("Generating visualizations...")

        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        visualization_paths = []

        # Get statistics by document count
        stats = self.analyze()

        # 1. Accuracy vs Context Size
        accuracy_data = {
            str(count): stats[count]["accuracy"]["mean"]
            for count in self.document_counts
            if count in stats
        }

        if accuracy_data:
            accuracy_path = output_dir / "accuracy_vs_context_size.png"
            self.plotter.plot_line_graph(
                x_data=list(range(len(accuracy_data))),
                y_data=list(accuracy_data.values()),
                title="Experiment 2: Accuracy vs Context Size",
                xlabel="Number of Documents",
                ylabel="Accuracy (0.0-1.0)",
                output_path=accuracy_path,
            )
            visualization_paths.append(accuracy_path)
            logger.info(f"Saved accuracy visualization to {accuracy_path}")

        # 2. Latency vs Context Size
        latency_data = {
            str(count): stats[count]["latency_ms"]["mean"]
            for count in self.document_counts
            if count in stats
        }

        if latency_data:
            latency_path = output_dir / "latency_vs_context_size.png"
            self.plotter.plot_line_graph(
                x_data=list(range(len(latency_data))),
                y_data=list(latency_data.values()),
                title="Experiment 2: Latency vs Context Size",
                xlabel="Number of Documents",
                ylabel="Latency (ms)",
                output_path=latency_path,
            )
            visualization_paths.append(latency_path)
            logger.info(f"Saved latency visualization to {latency_path}")

        # 3. Combined comparison (accuracy as bar chart)
        comparison_path = output_dir / "context_size_comparison.png"
        self.plotter.plot_bar_chart(
            data=accuracy_data,
            title="Experiment 2: Accuracy by Context Size",
            xlabel="Number of Documents",
            ylabel="Accuracy (0.0-1.0)",
            output_path=comparison_path,
            show_values=True,
        )
        visualization_paths.append(comparison_path)
        logger.info(f"Saved comparison visualization to {comparison_path}")

        return visualization_paths
