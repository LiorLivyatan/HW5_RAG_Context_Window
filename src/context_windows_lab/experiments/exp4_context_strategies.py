"""
Experiment 4: Context Engineering Strategies

Tests different strategies for managing context in multi-step agent interactions:
- SELECT: RAG-based retrieval of relevant context
- COMPRESS: Automatic summarization to reduce context
- WRITE: External memory (scratchpad) for storing key information
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from context_windows_lab.context_management.scratchpad import Scratchpad
from context_windows_lab.context_management.summarizer import Summarizer
from context_windows_lab.data_generation.document_generator import Document, DocumentGenerator
from context_windows_lab.evaluation.accuracy_evaluator import AccuracyEvaluator
from context_windows_lab.experiments.base_experiment import (
    BaseExperiment,
    ExperimentConfig,
)
from context_windows_lab.llm.ollama_interface import LLMResponse, OllamaInterface
from context_windows_lab.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class ContextStrategiesExperiment(BaseExperiment):
    """
    Experiment 4: Context Engineering Strategies.

    Tests different strategies for managing context over multiple steps:
    - SELECT: Uses RAG to retrieve only relevant context
    - COMPRESS: Uses summarization to compress context
    - WRITE: Uses external memory (scratchpad) to store key facts

    The experiment simulates a multi-step agent interaction where context
    grows with each step, testing how each strategy maintains performance.
    """

    def __init__(
        self,
        config: ExperimentConfig,
        num_documents: int = 20,
        words_per_document: int = 200,
        num_steps: int = 5,
        facts: Optional[List[str]] = None,
        questions: Optional[List[str]] = None,
        expected_answers: Optional[List[str]] = None,
        top_k: int = 5,  # Assignment pseudocode specifies k=5 for SELECT strategy
        max_summary_words: int = 200,
        llm_interface: OllamaInterface = None,
    ):
        """
        Initialize Context Strategies Experiment.

        Args:
            config: Experiment configuration
            num_documents: Number of documents to generate
            words_per_document: Words per document
            num_steps: Number of interaction steps to simulate
            facts: List of facts to embed (one per step)
            questions: List of questions to ask (one per step)
            expected_answers: List of expected answers (one per step)
            top_k: Number of documents to retrieve in SELECT mode
            max_summary_words: Maximum words for COMPRESS mode
            llm_interface: Optional LLM interface
        """
        super().__init__(config)

        self.num_documents = num_documents
        self.words_per_document = words_per_document
        self.num_steps = num_steps
        self.top_k = top_k
        self.max_summary_words = max_summary_words

        # Default facts, questions, and answers for multi-step scenario (10 steps)
        if facts is None:
            self.facts = [
                "The project budget is $2.5 million for Q1 2025.",
                "The team consists of 15 engineers and 3 designers.",
                "The launch date is scheduled for March 15th, 2025.",
                "The customer satisfaction rate is currently 94%.",
                "The monthly active users increased to 150,000.",
                "The technical stack uses React, Node.js, and PostgreSQL.",
                "The average response time is 120 milliseconds.",
                "The market share increased to 23% this quarter.",
                "The code coverage is maintained at 85%.",
                "The next major feature release is Q2 2025.",
            ][:self.num_steps]
        else:
            self.facts = facts

        if questions is None:
            self.questions = [
                "What is the project budget for Q1 2025?",
                "How many engineers are on the team?",
                "When is the launch date?",
                "What is the customer satisfaction rate?",
                "How many monthly active users are there?",
                "What is the technical stack?",
                "What is the average response time?",
                "What is the current market share?",
                "What is the code coverage percentage?",
                "When is the next major feature release?",
            ][:self.num_steps]
        else:
            self.questions = questions

        if expected_answers is None:
            self.expected_answers = [
                "$2.5 million",
                "15",
                "March 15th, 2025",
                "94%",
                "150,000",
                "React, Node.js, and PostgreSQL",
                "120 milliseconds",
                "23%",
                "85%",
                "Q2 2025",
            ][:self.num_steps]
        else:
            self.expected_answers = expected_answers

        # Ensure consistency
        assert len(self.facts) == num_steps, "Must have one fact per step"
        assert len(self.questions) == num_steps, "Must have one question per step"
        assert len(self.expected_answers) == num_steps, "Must have one expected answer per step"

        # Initialize LLM interface
        self.llm = llm_interface or OllamaInterface()

        # Initialize evaluator
        self.evaluator = AccuracyEvaluator()

        # Initialize plotter
        from context_windows_lab.visualization.plotter import Plotter

        self.plotter = Plotter()

        # Strategies to test
        self.strategies = ["SELECT", "COMPRESS", "WRITE"]

        # Strategy-specific components
        self.vector_stores: Dict[str, VectorStore] = {}
        self.summarizers: Dict[str, Summarizer] = {}
        self.scratchpads: Dict[str, Scratchpad] = {}

    def _generate_data(self) -> List[Document]:
        """
        Generate synthetic documents for the experiment.

        Returns:
            List of generated documents
        """
        logger.info(
            f"Generating {self.num_documents} documents "
            f"with {self.words_per_document} words each"
        )

        generator = DocumentGenerator()

        # Generate base documents
        # We'll add facts dynamically in _execute_queries
        # Use a placeholder fact for generation, we won't use it
        documents = generator.generate_documents(
            num_docs=self.num_documents,
            words_per_doc=self.words_per_document,
            fact="This is a placeholder fact for document generation.",
            fact_position="middle",
        )

        logger.info(f"Generated {len(documents)} base documents")
        return documents

    def _execute_queries(self, data: List[Document]) -> Dict[str, List[LLMResponse]]:
        """
        Execute queries for each strategy over multiple steps.

        Args:
            data: List of documents

        Returns:
            Dictionary mapping strategy to list of responses (one per step)
        """
        responses = {strategy: [] for strategy in self.strategies}

        # Initialize strategy components
        for strategy in self.strategies:
            if strategy == "SELECT":
                self.vector_stores[strategy] = VectorStore(
                    collection_name=f"exp4_{strategy}_{id(self)}"
                )
                # Add all documents to vector store
                self.vector_stores[strategy].add_documents([doc.content for doc in data])

            elif strategy == "COMPRESS":
                self.summarizers[strategy] = Summarizer(max_words=self.max_summary_words)

            elif strategy == "WRITE":
                self.scratchpads[strategy] = Scratchpad()

        # Run multi-step queries for each strategy
        for step_idx in range(self.num_steps):
            fact = self.facts[step_idx]
            question = self.questions[step_idx]

            logger.info(f"Step {step_idx + 1}/{self.num_steps}: {question}")

            # Add the fact to one of the documents for this step
            step_data = data.copy()
            fact_doc_idx = step_idx % len(step_data)
            step_data[fact_doc_idx] = Document(
                content=step_data[fact_doc_idx].content + f"\n\n{fact}",
                fact=fact,
                fact_position="middle",
                metadata=step_data[fact_doc_idx].metadata,
            )

            for strategy in self.strategies:
                if strategy == "SELECT":
                    # Use RAG: retrieve top-k relevant documents
                    retrieved = self.vector_stores[strategy].retrieve(
                        query=question, top_k=self.top_k
                    )
                    context = "\n\n".join([doc.content for doc in retrieved])

                    # Update vector store with new fact
                    self.vector_stores[strategy].add_documents(
                        [step_data[fact_doc_idx].content],
                        metadatas=[{"step": step_idx}],
                    )

                elif strategy == "COMPRESS":
                    # Use summarization: compress all documents
                    full_context = "\n\n".join([doc.content for doc in step_data])
                    context = self.summarizers[strategy].summarize(
                        full_context, method="first_last"
                    )

                elif strategy == "WRITE":
                    # Use scratchpad: store key facts externally
                    # First, extract and store the fact
                    fact_key = f"step_{step_idx + 1}"
                    self.scratchpads[strategy].write(fact_key, fact)

                    # Build context from scratchpad + relevant documents
                    scratchpad_summary = self.scratchpads[strategy].get_summary()
                    # Use RAG to get relevant docs
                    if strategy not in self.vector_stores:
                        self.vector_stores[strategy] = VectorStore(
                            collection_name=f"exp4_{strategy}_{id(self)}"
                        )
                        self.vector_stores[strategy].add_documents([doc.content for doc in data])

                    retrieved = self.vector_stores[strategy].retrieve(
                        query=question, top_k=self.top_k
                    )
                    docs_context = "\n\n".join([doc.content for doc in retrieved])

                    context = f"{scratchpad_summary}\n\nRelevant Documents:\n{docs_context}"

                    # Update vector store with new fact
                    self.vector_stores[strategy].add_documents(
                        [step_data[fact_doc_idx].content],
                        metadatas=[{"step": step_idx}],
                    )

                # Query LLM
                response = self.llm.query(context=context, question=question)
                responses[strategy].append(response)

                logger.info(
                    f"  {strategy}: {response.text[:100]}... " f"({response.latency_ms:.0f}ms)"
                )

        return responses

    def _evaluate_responses(self, responses: Dict[str, List[LLMResponse]]) -> List[Dict]:
        """
        Evaluate responses for each strategy across all steps.

        Args:
            responses: Dictionary mapping strategy to list of responses

        Returns:
            List of result dictionaries
        """
        results = []

        for strategy in self.strategies:
            strategy_responses = responses[strategy]

            for step_idx, response in enumerate(strategy_responses):
                expected_answer = self.expected_answers[step_idx]

                # Evaluate accuracy
                is_correct = self.evaluator.evaluate(response.text, expected_answer)
                accuracy = 1.0 if is_correct else 0.0

                result = {
                    "strategy": strategy,
                    "step": step_idx + 1,
                    "question": self.questions[step_idx],
                    "expected_answer": expected_answer,
                    "response": response.text,
                    "accuracy": accuracy,
                    "latency_ms": response.latency_ms,
                    "tokens_used": response.tokens_used,
                    "success": response.success,
                }

                results.append(result)

        return results

    def analyze(self) -> Dict[str, Dict]:
        """
        Analyze experiment results by strategy and step.

        Returns:
            Dictionary of statistics by strategy
        """
        if not self.results:
            return {}

        statistics = {}

        for strategy in self.strategies:
            strategy_results = [r for r in self.results if r["strategy"] == strategy]

            if not strategy_results:
                continue

            # Calculate metrics by step
            step_metrics = {}
            for step in range(1, self.num_steps + 1):
                step_results = [r for r in strategy_results if r["step"] == step]

                if step_results:
                    step_metrics[f"step_{step}"] = {
                        "accuracy": {
                            "mean": sum(r["accuracy"] for r in step_results) / len(step_results),
                        },
                        "latency_ms": {
                            "mean": sum(r["latency_ms"] for r in step_results) / len(step_results),
                        },
                    }

            # Overall strategy metrics
            statistics[strategy] = {
                "overall": {
                    "accuracy": {
                        "mean": sum(r["accuracy"] for r in strategy_results)
                        / len(strategy_results),
                    },
                    "latency_ms": {
                        "mean": sum(r["latency_ms"] for r in strategy_results)
                        / len(strategy_results),
                    },
                    "tokens_used": {
                        "mean": sum(r["tokens_used"] for r in strategy_results)
                        / len(strategy_results),
                    },
                },
                "by_step": step_metrics,
            }

        logger.info("Analysis complete")
        return statistics

    def visualize(self) -> List[Path]:
        """
        Create visualizations comparing strategies.

        Returns:
            List of paths to generated visualization files
        """
        viz_paths = []

        # Get statistics from analyze()
        statistics = self.analyze()
        if not statistics:
            logger.warning("No statistics available for visualization")
            return []

        # Extract data for plotting
        strategies = list(statistics.keys())
        steps = list(range(1, self.num_steps + 1))

        # 1. Overall accuracy comparison
        overall_accuracy = {
            strategy: statistics[strategy]["overall"]["accuracy"]["mean"] for strategy in strategies
        }

        accuracy_path = self.config.output_dir / "overall_accuracy_by_strategy.png"
        self.plotter.plot_bar_chart(
            data=overall_accuracy,
            title="Overall Accuracy by Strategy",
            xlabel="Strategy",
            ylabel="Accuracy",
            output_path=accuracy_path,
        )
        viz_paths.append(accuracy_path)

        # 2. Latency comparison
        latency_data = {
            strategy: statistics[strategy]["overall"]["latency_ms"]["mean"]
            for strategy in strategies
        }

        latency_path = self.config.output_dir / "latency_by_strategy.png"
        self.plotter.plot_bar_chart(
            data=latency_data,
            title="Average Latency by Strategy",
            xlabel="Strategy",
            ylabel="Latency (ms)",
            output_path=latency_path,
        )
        viz_paths.append(latency_path)

        logger.info(f"Generated {len(viz_paths)} visualizations")
        return viz_paths
