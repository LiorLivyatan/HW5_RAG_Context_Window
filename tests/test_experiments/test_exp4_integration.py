"""
Integration tests for Experiment 4: Context Engineering Strategies.

Tests the three strategies: SELECT (RAG), COMPRESS (Summarization), WRITE (Scratchpad).
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest

from context_windows_lab.experiments import ContextStrategiesExperiment, ExperimentConfig
from context_windows_lab.llm import LLMResponse

# Check if ChromaDB is available (required for SELECT and WRITE strategies)
try:
    from context_windows_lab.rag.vector_store import CHROMADB_AVAILABLE
except ImportError:
    CHROMADB_AVAILABLE = False


class MockOllamaInterface:
    """Mock LLM interface for testing."""

    def __init__(self):
        # Initialize without calling parent to avoid ollama dependency
        self.base_url = "http://localhost:11434"
        self.model = "llama2"
        self.temperature = 0.0
        self.max_tokens = 500
        self.timeout = 60
        self.max_retries = 3
        self.call_count = 0
        self.queries = []
        self.response_map = {
            0: "$2.5 million",  # Step 1: budget
            1: "15",  # Step 2: engineers
            2: "March 15th, 2025",  # Step 3: launch date
            3: "94%",  # Step 4: satisfaction
            4: "150,000",  # Step 5: users
        }

    def check_availability(self) -> bool:
        """Mock check_availability."""
        return True

    def query(self, context: str, question: str, **kwargs) -> LLMResponse:
        """Mock query that returns context-appropriate answers."""
        query_idx = self.call_count % len(self.response_map)
        response_text = self.response_map.get(query_idx, "Answer")

        self.call_count += 1
        self.queries.append({"context": context, "question": question})

        return LLMResponse(
            text=response_text,
            latency_ms=1000,
            tokens_used=10,
            model="llama2",
            timestamp=datetime.now(),
            success=True,
            error=None,
        )

    def check_connection(self) -> bool:
        return True


class TestContextStrategiesExperiment:
    """Test suite for Experiment 4."""

    def test_initialization_default(self):
        """Test experiment initializes with default settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp4",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(config)

            assert exp.num_documents == 20
            assert exp.words_per_document == 200
            assert exp.num_steps == 5
            assert exp.top_k == 5
            assert len(exp.strategies) == 3
            assert "SELECT" in exp.strategies
            assert "COMPRESS" in exp.strategies
            assert "WRITE" in exp.strategies

    def test_initialization_custom_params(self):
        """Test experiment with custom parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp4_custom",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            custom_facts = ["Fact 1", "Fact 2", "Fact 3"]
            custom_questions = ["Q1?", "Q2?", "Q3?"]
            custom_answers = ["A1", "A2", "A3"]

            exp = ContextStrategiesExperiment(
                config,
                num_documents=10,
                words_per_document=100,
                num_steps=3,
                facts=custom_facts,
                questions=custom_questions,
                expected_answers=custom_answers,
                top_k=3,
                max_summary_words=100,
            )

            assert exp.num_documents == 10
            assert exp.words_per_document == 100
            assert exp.num_steps == 3
            assert exp.facts == custom_facts
            assert exp.questions == custom_questions
            assert exp.expected_answers == custom_answers
            assert exp.top_k == 3
            assert exp.max_summary_words == 100

    def test_initialization_validation(self):
        """Test that initialization validates input consistency."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_validation",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            # Mismatched lengths should raise assertion error
            with pytest.raises(AssertionError):
                ContextStrategiesExperiment(
                    config,
                    num_steps=3,
                    facts=["F1", "F2"],  # Only 2 facts for 3 steps
                    questions=["Q1", "Q2", "Q3"],
                    expected_answers=["A1", "A2", "A3"],
                )

    def test_generate_data(self):
        """Test data generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_gen",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=5,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
                llm_interface=mock_llm,
            )

            data = exp._generate_data()

            assert len(data) == 5
            # Each document should have ~200 words (default)
            for doc in data:
                assert len(doc.content.split()) > 0

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_execute_queries_all_strategies(self):
        """Test query execution for all three strategies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_queries",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=5,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)

            # Should have responses for all 3 strategies
            assert "SELECT" in responses
            assert "COMPRESS" in responses
            assert "WRITE" in responses

            # Each strategy should have responses for all steps
            assert len(responses["SELECT"]) == 3
            assert len(responses["COMPRESS"]) == 3
            assert len(responses["WRITE"]) == 3

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_select_strategy(self):
        """Test SELECT (RAG) strategy specifically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_select",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=10,
                num_steps=2,
                facts=["Fact 1", "Fact 2"],
                questions=["Q1?", "Q2?"],
                expected_answers=["A1", "A2"],
                top_k=3,
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)

            # SELECT should use vector store
            assert exp.vector_stores.get("SELECT") is not None

            # Should retrieve top_k documents
            assert responses["SELECT"][0].success

    def test_compress_strategy(self):
        """Test COMPRESS (Summarization) strategy specifically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_compress",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=10,
                num_steps=2,
                facts=["Fact 1", "Fact 2"],
                questions=["Q1?", "Q2?"],
                expected_answers=["A1", "A2"],
                max_summary_words=100,
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)

            # COMPRESS should use summarizer
            assert exp.summarizers.get("COMPRESS") is not None

            # Should receive compressed context
            assert responses["COMPRESS"][0].success

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_write_strategy(self):
        """Test WRITE (Scratchpad) strategy specifically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_write",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=10,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)

            # WRITE should use scratchpad
            assert exp.scratchpads.get("WRITE") is not None

            # Scratchpad should have entries for each step
            scratchpad = exp.scratchpads["WRITE"]
            assert len(scratchpad) == 3  # 3 steps

            assert responses["WRITE"][0].success

    def test_evaluate_responses(self):
        """Test response evaluation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_eval",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_steps=2,
                facts=["Fact 1", "Fact 2"],
                questions=["Q1?", "Q2?"],
                expected_answers=["$2.5 million", "15"],
                llm_interface=mock_llm,
            )

            # Create mock responses
            responses = {
                "SELECT": [
                    LLMResponse(
                        text="$2.5 million",
                        latency_ms=1000,
                        tokens_used=10,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                    LLMResponse(
                        text="15",
                        latency_ms=1000,
                        tokens_used=10,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                ],
                "COMPRESS": [
                    LLMResponse(
                        text="$2.5 million",
                        latency_ms=1500,
                        tokens_used=15,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                    LLMResponse(
                        text="15",
                        latency_ms=1500,
                        tokens_used=15,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                ],
                "WRITE": [
                    LLMResponse(
                        text="$2.5 million",
                        latency_ms=1200,
                        tokens_used=12,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                    LLMResponse(
                        text="15",
                        latency_ms=1200,
                        tokens_used=12,
                        model="llama2",
                        timestamp=datetime.now(),
                        success=True,
                    ),
                ],
            }

            evaluations = exp._evaluate_responses(responses)

            # Should have 3 strategies × 2 steps = 6 evaluations
            assert len(evaluations) == 6

            # Check structure
            for eval_result in evaluations:
                assert "strategy" in eval_result
                assert "step" in eval_result
                assert "accuracy" in eval_result
                assert "latency_ms" in eval_result
                assert "tokens_used" in eval_result

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_run_complete_experiment(self):
        """Test running complete experiment end-to-end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_complete",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=5,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
                llm_interface=mock_llm,
            )

            results = exp.run()

            # Should have 3 strategies × 3 steps × 1 iteration = 9 results
            assert len(results.raw_results) == 9

            # Check that all strategies are present
            strategies = {r["strategy"] for r in results.raw_results}
            assert strategies == {"SELECT", "COMPRESS", "WRITE"}

    def test_analysis(self):
        """Test statistical analysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_analysis",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(
                config,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
            )

            # Set mock results
            exp.results = []
            for strategy in ["SELECT", "COMPRESS", "WRITE"]:
                for step in range(1, 4):
                    exp.results.append(
                        {
                            "strategy": strategy,
                            "step": step,
                            "question": "Q?",
                            "expected_answer": "A",
                            "response": "A",
                            "accuracy": 1.0,
                            "latency_ms": 1000,
                            "tokens_used": 10,
                            "success": True,
                        }
                    )

            analysis = exp.analyze()

            # Should have analysis for all 3 strategies
            assert "SELECT" in analysis
            assert "COMPRESS" in analysis
            assert "WRITE" in analysis

            # Check structure
            for strategy in exp.strategies:
                assert "overall" in analysis[strategy]
                assert "by_step" in analysis[strategy]

                assert "accuracy" in analysis[strategy]["overall"]
                assert "latency_ms" in analysis[strategy]["overall"]

    def test_visualization_generation(self):
        """Test visualization generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_viz",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(
                config,
                num_steps=3,
                facts=["Fact 1", "Fact 2", "Fact 3"],
                questions=["Q1?", "Q2?", "Q3?"],
                expected_answers=["A1", "A2", "A3"],
            )

            # Set mock results
            exp.results = []
            for strategy in ["SELECT", "COMPRESS", "WRITE"]:
                for step in range(1, 4):
                    exp.results.append(
                        {
                            "strategy": strategy,
                            "step": step,
                            "question": "Q?",
                            "expected_answer": "A",
                            "response": "A",
                            "accuracy": 0.9,
                            "latency_ms": 1000,
                            "tokens_used": 10,
                            "success": True,
                        }
                    )

            viz_paths = exp.visualize()

            # Should generate 2 visualizations (accuracy + latency)
            assert len(viz_paths) == 2

            # All files should exist
            for path in viz_paths:
                assert Path(path).exists()

    def test_multi_step_progression(self):
        """Test that experiment handles multiple steps correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_multi_step",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            # Test with 5 steps (default)
            exp = ContextStrategiesExperiment(config, num_steps=5)

            assert len(exp.facts) == 5
            assert len(exp.questions) == 5
            assert len(exp.expected_answers) == 5

    def test_top_k_parameter(self):
        """Test that top_k parameter affects SELECT strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_top_k",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(config, top_k=7)
            assert exp.top_k == 7

    def test_max_summary_words_parameter(self):
        """Test that max_summary_words affects COMPRESS strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_summary_words",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(config, max_summary_words=150)
            assert exp.max_summary_words == 150

    def test_default_facts_and_questions(self):
        """Test that default facts and questions are properly defined."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_defaults",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(config, num_steps=5)

            # Should have 10 default facts/questions (but use first 5)
            assert len(exp.facts) >= 5
            assert len(exp.questions) >= 5
            assert len(exp.expected_answers) >= 5

            # First fact should be about budget
            assert "budget" in exp.facts[0].lower()
            assert "2.5 million" in exp.facts[0]

    def test_different_num_steps(self):
        """Test with different number of steps."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for num_steps in [1, 3, 5, 7]:
                config = ExperimentConfig(
                    name=f"test_steps_{num_steps}",
                    output_dir=Path(tmpdir),
                    iterations=1,
                )

                # Generate custom facts/questions for this num_steps
                facts = [f"Fact {i}" for i in range(num_steps)]
                questions = [f"Question {i}?" for i in range(num_steps)]
                answers = [f"Answer {i}" for i in range(num_steps)]

                exp = ContextStrategiesExperiment(
                    config,
                    num_steps=num_steps,
                    facts=facts,
                    questions=questions,
                    expected_answers=answers,
                )

                assert exp.num_steps == num_steps

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_multiple_iterations(self):
        """Test experiment with multiple iterations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_multi_iter",
                output_dir=Path(tmpdir),
                iterations=2,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextStrategiesExperiment(
                config,
                num_documents=5,
                num_steps=2,
                facts=["Fact 1", "Fact 2"],
                questions=["Q1?", "Q2?"],
                expected_answers=["A1", "A2"],
                llm_interface=mock_llm,
            )

            results = exp.run()

            # Should have 3 strategies × 2 steps × 2 iterations = 12 results
            assert len(results.raw_results) == 12

    def test_repr(self):
        """Test string representation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_repr",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextStrategiesExperiment(config)
            repr_str = repr(exp)

            # Should contain class name
            assert "ContextStrategiesExperiment" in repr_str
