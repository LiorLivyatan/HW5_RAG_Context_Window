"""
Integration tests for Experiment 2: Context Size Impact.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest

from context_windows_lab.experiments import ContextSizeExperiment, ExperimentConfig
from context_windows_lab.llm import LLMResponse


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

    def check_availability(self) -> bool:
        """Mock check_availability."""
        return True

    def query(self, context: str, question: str, **kwargs) -> LLMResponse:
        """Mock query that simulates varying latency based on context size."""
        self.call_count += 1
        self.queries.append({"context": context, "question": question})

        # Simulate that larger context takes longer
        context_word_count = len(context.split())
        simulated_latency = 1000 + (context_word_count * 0.5)  # Base + per-word

        # Always return correct answer (fact is embedded)
        return LLMResponse(
            text="December 15th, 2025",  # Expected answer
            latency_ms=simulated_latency,
            tokens_used=10,
            model="llama2",
            timestamp=datetime.now(),
            success=True,
            error=None,
        )

    def check_connection(self) -> bool:
        return True


class TestContextSizeExperiment:
    """Test suite for Experiment 2."""

    def test_initialization_default(self):
        """Test experiment initializes with default settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp2",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextSizeExperiment(config)

            assert exp.document_counts == [5, 10, 20, 50]
            assert exp.words_per_document == 200
            assert exp.fact_position == "middle"

    def test_initialization_custom_params(self):
        """Test experiment with custom parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp2_custom",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextSizeExperiment(
                config,
                document_counts=[3, 6, 9],
                words_per_document=100,
                fact="Custom fact",
                question="Custom question?",
                expected_answer="custom",
                fact_position="start",
            )

            assert exp.document_counts == [3, 6, 9]
            assert exp.words_per_document == 100
            assert exp.fact == "Custom fact"
            assert exp.question == "Custom question?"
            assert exp.expected_answer == "custom"
            assert exp.fact_position == "start"

    def test_data_generation(self):
        """Test that experiment generates correct document sets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_data_gen",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5, 10],
                llm_interface=mock_llm,
            )

            data = exp._generate_data()

            # Should generate documents for all sizes
            assert 5 in data
            assert 10 in data

            # Each size should have correct number of documents
            assert len(data[5]) == 5
            assert len(data[10]) == 10

    def test_execute_queries(self):
        """Test query execution for all document sizes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_queries",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[3, 5],
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)

            # Should have responses for each document size
            assert "3" in responses
            assert "5" in responses

            # Larger context should have higher latency
            assert responses["5"].latency_ms > responses["3"].latency_ms

    def test_evaluate_responses(self):
        """Test response evaluation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_eval",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5],
                expected_answer="42",
                llm_interface=mock_llm,
            )

            data = exp._generate_data()
            responses = exp._execute_queries(data)
            evaluations = exp._evaluate_responses(responses)

            assert len(evaluations) == 1  # One document size
            assert evaluations[0]["num_documents"] == 5
            assert evaluations[0]["accuracy"] == 1.0  # Mock returns "42"
            assert evaluations[0]["latency_ms"] > 0

    def test_run_complete_experiment(self):
        """Test running complete experiment end-to-end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_complete",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[3, 5],
                llm_interface=mock_llm,
            )

            results = exp.run()

            # Should have results for both sizes × 1 iteration
            assert len(results) == 2

            # Results should contain expected fields
            for result in results:
                assert "num_documents" in result
                assert "accuracy" in result
                assert "latency_ms" in result
                assert "tokens_used" in result

    def test_analysis(self):
        """Test statistical analysis of results."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_analysis",
                output_dir=Path(tmpdir),
                iterations=2,  # Multiple iterations for stats
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5, 10],
                llm_interface=mock_llm,
            )

            exp.run()
            analysis = exp.analyze()

            # Should have analysis for each document size
            assert 5 in analysis
            assert 10 in analysis

            # Check analysis structure
            for num_docs in [5, 10]:
                assert "accuracy" in analysis[num_docs]
                assert "latency_ms" in analysis[num_docs]
                assert "tokens_used" in analysis[num_docs]

                # Check statistics structure
                assert "mean" in analysis[num_docs]["accuracy"]
                assert "std" in analysis[num_docs]["accuracy"]
                assert "ci_95" in analysis[num_docs]["accuracy"]

    def test_visualization_generation(self):
        """Test that visualizations are generated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_viz",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5, 10],
                llm_interface=mock_llm,
            )

            exp.run()
            viz_paths = exp.visualize()

            # Should generate 3 visualizations
            assert len(viz_paths) == 3

            # All files should exist
            for path in viz_paths:
                assert Path(path).exists()

    def test_results_saved_to_json(self):
        """Test that results are saved to JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_json",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5],
                llm_interface=mock_llm,
            )

            exp.run()
            exp.save_results()

            # Check JSON file exists
            json_path = Path(tmpdir) / "results.json"
            assert json_path.exists()

            # Verify it's valid JSON
            import json

            with open(json_path) as f:
                data = json.load(f)

            assert "results" in data
            assert "analysis" in data
            assert "config" in data

    def test_multiple_iterations(self):
        """Test experiment with multiple iterations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_multi_iter",
                output_dir=Path(tmpdir),
                iterations=3,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5],
                llm_interface=mock_llm,
            )

            results = exp.run()

            # Should have 1 size × 3 iterations = 3 results
            assert len(results) == 3

            # All results should be for 5 documents
            assert all(r["num_documents"] == 5 for r in results)

    def test_latency_increases_with_context_size(self):
        """Test that latency increases with larger context."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_latency",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5, 10, 20],
                llm_interface=mock_llm,
            )

            exp.run()
            analysis = exp.analyze()

            # Latency should increase with size
            latency_5 = analysis[5]["latency_ms"]["mean"]
            latency_10 = analysis[10]["latency_ms"]["mean"]
            latency_20 = analysis[20]["latency_ms"]["mean"]

            assert latency_5 < latency_10 < latency_20

    def test_repr(self):
        """Test string representation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_repr",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = ContextSizeExperiment(
                config,
                document_counts=[5, 10],
            )

            repr_str = repr(exp)
            assert "ContextSizeExperiment" in repr_str
            assert "5" in repr_str or "[5" in repr_str

    def test_custom_fact_and_question(self):
        """Test experiment with custom fact and question."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_custom",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            custom_fact = "The secret code is ALPHA."
            custom_question = "What is the secret code?"

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[5],
                fact=custom_fact,
                question=custom_question,
                expected_answer="ALPHA",
                llm_interface=mock_llm,
            )

            results = exp.run()

            assert len(results) == 1
            # Fact should be in generated documents
            data = exp._generate_data()
            all_content = " ".join([doc.content for doc in data["5"]])
            assert custom_fact in all_content

    def test_different_fact_positions(self):
        """Test with facts at different positions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for position in ["start", "middle", "end"]:
                config = ExperimentConfig(
                    name=f"test_pos_{position}",
                    output_dir=Path(tmpdir),
                    iterations=1,
                )

                mock_llm = MockOllamaInterface()
                exp = ContextSizeExperiment(
                    config,
                    document_counts=[5],
                    fact_position=position,
                    llm_interface=mock_llm,
                )

                results = exp.run()
                assert len(results) == 1

    def test_edge_case_single_document(self):
        """Test with single document size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_single",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[1],
                llm_interface=mock_llm,
            )

            results = exp.run()
            assert len(results) == 1
            assert results[0]["num_documents"] == 1

    def test_edge_case_large_document_count(self):
        """Test with large document count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_large",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = ContextSizeExperiment(
                config,
                document_counts=[50],
                words_per_document=100,
                llm_interface=mock_llm,
            )

            results = exp.run()
            assert len(results) == 1
            assert results[0]["num_documents"] == 50
