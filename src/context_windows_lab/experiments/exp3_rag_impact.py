"""
Experiment 3: RAG Impact

This experiment compares Full Context vs RAG-based retrieval using REAL Hebrew documents
to demonstrate how RAG affects accuracy, latency, and token usage.

Research Question:
- How does RAG-based retrieval compare to using full context?
- What are the tradeoffs in accuracy, speed, and cost?
- Does RAG work well with non-English (Hebrew) documents?
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from context_windows_lab.data_generation import Document
from context_windows_lab.evaluation import AccuracyEvaluator, calculate_statistics
from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)
from context_windows_lab.llm import LLMResponse, OllamaInterface
from context_windows_lab.rag import RetrievedDocument, VectorStore
from context_windows_lab.visualization import Plotter

logger = logging.getLogger(__name__)


class RAGImpactExperiment(BaseExperiment):
    """
    Experiment 3: RAG Impact using REAL Hebrew documents.

    Compares two modes:
    1. Full Context: All documents sent to LLM
    2. RAG Mode: Only top-k retrieved documents sent to LLM

    Uses 20 Hebrew documents from data/raw/hebrew_documents/
    """

    def __init__(
        self,
        config: ExperimentConfig,
        documents_path: Optional[str] = None,
        domain: Optional[str] = None,
        question: str = "מהם היתרונות העיקריים של הטכנולוגיה?",
        expected_answer: str = "יעילות",
        top_k: int = 3,
        llm_interface: OllamaInterface = None,
    ):
        """
        Initialize RAG Impact experiment with Hebrew documents.

        Args:
            config: Experiment configuration
            documents_path: Path to Hebrew documents directory (default: data/raw/hebrew_documents)
            domain: Optional domain filter ('technology', 'law', 'medicine', or None for all)
            question: Question to ask (in Hebrew)
            expected_answer: Expected answer (in Hebrew)
            top_k: Number of documents to retrieve in RAG mode
            llm_interface: Optional LLM interface
        """
        super().__init__(config)

        # Set default documents path if not provided
        if documents_path is None:
            # Assume we're running from project root
            self.documents_path = Path("data/raw/hebrew_documents")
        else:
            self.documents_path = Path(documents_path)

        self.domain = domain
        self.question = question
        self.expected_answer = expected_answer
        self.top_k = top_k

        # Initialize building blocks
        self.llm = llm_interface or OllamaInterface()
        self.evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)
        self.plotter = Plotter()

        # Vector store (in-memory)
        self.vector_store = None

        # Modes to test
        self.modes = ["full_context", "rag"]

    @staticmethod
    def load_hebrew_documents(documents_path: Path, domain: Optional[str] = None) -> List[Document]:
        """
        Load Hebrew documents from data/raw/hebrew_documents/.

        Args:
            documents_path: Path to hebrew_documents directory
            domain: Optional domain filter ('technology', 'law', 'medicine')

        Returns:
            List of Document objects with Hebrew content
        """
        documents = []

        # Determine which domains to load
        if domain:
            domains = [domain]
        else:
            domains = ["technology", "law", "medicine"]

        logger.info(f"Loading Hebrew documents from {documents_path}")
        logger.info(f"Domains: {domains}")

        for domain_name in domains:
            domain_path = documents_path / domain_name

            if not domain_path.exists():
                logger.warning(f"Domain directory not found: {domain_path}")
                continue

            # Load all .txt files in this domain
            for txt_file in sorted(domain_path.glob("*.txt")):
                try:
                    content = txt_file.read_text(encoding="utf-8")

                    # Create Document object
                    doc = Document(
                        content=content,
                        metadata={
                            "domain": domain_name,
                            "filename": txt_file.name,
                            "word_count": len(content.split()),
                            "source": "hebrew_corpus",
                        },
                    )
                    documents.append(doc)

                    logger.debug(
                        f"Loaded {txt_file.name}: {len(content)} chars, "
                        f"{len(content.split())} words"
                    )

                except Exception as e:
                    logger.error(f"Error loading {txt_file}: {e}")

        logger.info(f"Successfully loaded {len(documents)} Hebrew documents")
        return documents

    def _generate_data(self) -> List[Document]:
        """
        Load Hebrew documents from data/raw/hebrew_documents/.

        Returns:
            List of Hebrew documents
        """
        logger.info("Loading Hebrew documents for RAG experiment...")

        documents = self.load_hebrew_documents(
            documents_path=self.documents_path, domain=self.domain
        )

        if not documents:
            raise RuntimeError(
                f"No Hebrew documents found at {self.documents_path}. "
                f"Please ensure the documents exist in data/raw/hebrew_documents/"
            )

        logger.info(f"Loaded {len(documents)} Hebrew documents")
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
        logger.debug(f"Full context: {len(full_context)} chars, {len(full_context.split())} words")

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

    def _evaluate_responses(self, responses: Dict[str, LLMResponse]) -> List[Dict[str, Any]]:
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
            f"path={self.documents_path}, "
            f"domain={self.domain or 'all'}, "
            f"top_k={self.top_k})"
        )
