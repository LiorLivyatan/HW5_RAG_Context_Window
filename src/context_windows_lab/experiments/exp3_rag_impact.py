"""
Experiment 3: RAG Impact

This experiment compares Full Context vs RAG-based retrieval to demonstrate
how RAG affects accuracy, latency, and token usage.

Research Question:
- How does RAG-based retrieval compare to using full context?
- What are the tradeoffs in accuracy, speed, and cost?
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from context_windows_lab.data_generation import DocumentGenerator, Document
from context_windows_lab.llm import OllamaInterface, LLMResponse
from context_windows_lab.rag import VectorStore, RetrievedDocument
from context_windows_lab.evaluation import AccuracyEvaluator, calculate_statistics
from context_windows_lab.visualization import Plotter
from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)

logger = logging.getLogger(__name__)


class RAGImpactExperiment(BaseExperiment):
    """
    Experiment 3: RAG Impact.

    Compares two modes:
    1. Full Context: All documents sent to LLM
    2. RAG Mode: Only top-k retrieved documents sent to LLM
    """

    def __init__(
        self,
        config: ExperimentConfig,
        num_documents: int = 20,
        words_per_document: int = 200,
        fact: str = "The quarterly revenue increased by 47% compared to last year.",
        question: str = "What was the quarterly revenue growth?",
        expected_answer: str = "47%",
        top_k: int = 3,
        llm_interface: OllamaInterface = None,
    ):
        """
        Initialize RAG Impact experiment.

        Args:
            config: Experiment configuration
            num_documents: Number of documents to generate
            words_per_document: Words per document
            fact: Critical fact to embed in middle document
            question: Question to ask
            expected_answer: Expected answer
            top_k: Number of documents to retrieve in RAG mode
            llm_interface: Optional LLM interface
        """
        super().__init__(config)

        self.num_documents = num_documents
        self.words_per_document = words_per_document
        self.fact = fact
        self.question = question
        self.expected_answer = expected_answer
        self.top_k = top_k

        # Initialize building blocks
        self.doc_generator = DocumentGenerator(seed=42)
        self.llm = llm_interface or OllamaInterface()
        self.evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)
        self.plotter = Plotter()

        # Vector store (in-memory)
        self.vector_store = None

        # Modes to test
        self.modes = ["full_context", "rag"]

    def _generate_data(self) -> List[Document]:
        """
        Generate documents with fact embedded in middle.

        Returns:
            List of documents
        """
        logger.info(
            f"Generating {self.num_documents} documents with fact in middle..."
        )

        documents = self.doc_generator.generate_documents(
            num_docs=self.num_documents,
            words_per_doc=self.words_per_document,
            fact=self.fact,
            fact_position="middle",  # Embed fact in middle document
        )

        return documents

    def _execute_queries(self, data: List[Document]) -> Dict[str, LLMResponse]:
        """
        Execute queries in both modes.

        Args:
            data: List of documents

        Returns:
            Dictionary mapping mode to LLM response
        """
        responses = {}

        # Mode 1: Full Context - use all documents
        logger.info("Querying with FULL CONTEXT (all documents)...")
        full_context = "\n\n".join([doc.content for doc in data])
        logger.debug(
            f"Full context: {len(full_context)} chars, {len(full_context.split())} words"
        )

        response_full = self.llm.query(context=full_context, question=self.question)
        responses["full_context"] = response_full

        # Mode 2: RAG - retrieve top-k documents
        logger.info(f"Querying with RAG (top-{self.top_k} retrieved documents)...")

        # Initialize vector store and add documents
        try:
            self.vector_store = VectorStore(collection_name=f"rag_exp_{id(self)}")
            doc_texts = [doc.content for doc in data]
            self.vector_store.add_documents(doc_texts)

            # Retrieve relevant documents
            retrieved = self.vector_store.retrieve(query=self.question, top_k=self.top_k)

            # Build RAG context from retrieved docs
            rag_context = "\n\n".join([doc.content for doc in retrieved])
            logger.debug(
                f"RAG context: {len(rag_context)} chars, {len(rag_context.split())} words, "
                f"scores: {[f'{doc.score:.3f}' for doc in retrieved]}"
            )

            response_rag = self.llm.query(context=rag_context, question=self.question)
            responses["rag"] = response_rag

        except ImportError as e:
            logger.error(f"ChromaDB not available: {e}")
            # Create a dummy failed response
            responses["rag"] = LLMResponse(
                text="",
                success=False,
                error="ChromaDB not installed",
                latency_ms=0,
                tokens_used=0,
            )

        return responses

    def _evaluate_responses(
        self, responses: Dict[str, LLMResponse]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate responses for both modes.

        Args:
            responses: Responses by mode

        Returns:
            List of evaluation results
        """
        logger.info("Evaluating responses...")
        evaluations = []

        for mode, response in responses.items():
            if response.success:
                accuracy = self.evaluator.evaluate(response.text, self.expected_answer)

                evaluation = {
                    "mode": mode,
                    "accuracy": accuracy,
                    "latency_ms": response.latency_ms,
                    "tokens_used": response.tokens_used,
                    "response_text": response.text,
                    "success": True,
                }

                logger.debug(
                    f"Mode={mode}, Accuracy={accuracy:.2f}, "
                    f"Latency={response.latency_ms:.0f}ms, "
                    f"Tokens={response.tokens_used}"
                )
            else:
                evaluation = {
                    "mode": mode,
                    "accuracy": 0.0,
                    "latency_ms": 0.0,
                    "tokens_used": 0,
                    "response_text": "",
                    "success": False,
                    "error": response.error,
                }

                logger.warning(f"Query failed for mode={mode}: {response.error}")

            evaluations.append(evaluation)

        return evaluations

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze results by mode.

        Returns:
            Dictionary with analysis by mode
        """
        logger.info("Analyzing results across modes...")
        analysis = {}

        for mode in self.modes:
            # Get results for this mode
            mode_results = [r for r in self.results if r["mode"] == mode]

            if not mode_results:
                continue

            # Calculate statistics
            accuracies = [r["accuracy"] for r in mode_results]
            latencies = [r["latency_ms"] for r in mode_results]
            tokens = [r["tokens_used"] for r in mode_results]

            acc_stats = calculate_statistics(accuracies)
            lat_stats = calculate_statistics(latencies)
            tok_stats = calculate_statistics(tokens)

            analysis[mode] = {
                "accuracy": {
                    "mean": acc_stats.mean,
                    "std": acc_stats.std,
                    "ci_95": acc_stats.confidence_interval_95,
                },
                "latency_ms": {"mean": lat_stats.mean, "std": lat_stats.std},
                "tokens_used": {"mean": tok_stats.mean, "std": tok_stats.std},
            }

            logger.info(
                f"Mode '{mode}': "
                f"Accuracy={acc_stats.mean:.2f}±{acc_stats.std:.2f}, "
                f"Latency={lat_stats.mean:.0f}±{lat_stats.std:.0f}ms, "
                f"Tokens={tok_stats.mean:.0f}±{tok_stats.std:.0f}"
            )

        return analysis

    def visualize(self) -> List[Path]:
        """
        Generate visualizations for RAG comparison.

        Returns:
            List of paths to generated visualizations
        """
        logger.info("Generating visualizations...")

        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        visualization_paths = []

        # Get statistics
        stats = self.analyze()

        # 1. Accuracy Comparison
        accuracy_data = {
            mode.replace("_", " ").title(): stats[mode]["accuracy"]["mean"]
            for mode in self.modes
            if mode in stats
        }

        if accuracy_data:
            accuracy_path = output_dir / "accuracy_comparison.png"
            self.plotter.plot_bar_chart(
                data=accuracy_data,
                title="Experiment 3: Accuracy - Full Context vs RAG",
                xlabel="Mode",
                ylabel="Accuracy (0.0-1.0)",
                output_path=accuracy_path,
                show_values=True,
            )
            visualization_paths.append(accuracy_path)
            logger.info(f"Saved accuracy visualization to {accuracy_path}")

        # 2. Latency Comparison
        latency_data = {
            mode.replace("_", " ").title(): stats[mode]["latency_ms"]["mean"]
            for mode in self.modes
            if mode in stats
        }

        if latency_data:
            latency_path = output_dir / "latency_comparison.png"
            self.plotter.plot_bar_chart(
                data=latency_data,
                title="Experiment 3: Latency - Full Context vs RAG",
                xlabel="Mode",
                ylabel="Latency (ms)",
                output_path=latency_path,
                show_values=True,
            )
            visualization_paths.append(latency_path)
            logger.info(f"Saved latency visualization to {latency_path}")

        # 3. Token Usage Comparison
        tokens_data = {
            mode.replace("_", " ").title(): stats[mode]["tokens_used"]["mean"]
            for mode in self.modes
            if mode in stats
        }

        if tokens_data:
            tokens_path = output_dir / "tokens_comparison.png"
            self.plotter.plot_bar_chart(
                data=tokens_data,
                title="Experiment 3: Token Usage - Full Context vs RAG",
                xlabel="Mode",
                ylabel="Tokens Used",
                output_path=tokens_path,
                show_values=True,
            )
            visualization_paths.append(tokens_path)
            logger.info(f"Saved tokens visualization to {tokens_path}")

        return visualization_paths

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"RAGImpactExperiment("
            f"docs={self.num_documents}, "
            f"top_k={self.top_k})"
        )
