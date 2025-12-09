"""
Integration tests for Experiment 1 (Needle in Haystack).

These tests verify the end-to-end execution of the experiment.
"""

import pytest
from pathlib import Path
import tempfile
from context_windows_lab.experiments import (
    ExperimentConfig,
    NeedleInHaystackExperiment,
)
from context_windows_lab.llm.ollama_interface import OllamaInterface


class MockOllamaInterface:
    """Mock LLM interface for testing without actual Ollama."""

    def __init__(self, *args, **kwargs):
        pass

    def check_availability(self):
        return True

    def query(self, context: str, question: str):
        """Return a mock response."""
        from context_windows_lab.llm.ollama_interface import LLMResponse
        from datetime import datetime

        # Return the expected answer for testing
        return LLMResponse(
            text="David Cohen",
            latency_ms=100.0,
            tokens_used=5,
            model="mock-model",
            timestamp=datetime.now(),
            success=True,
        )


class TestNeedleInHaystackIntegration:
    """Integration tests for Needle in Haystack experiment."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "results"
        self.output_dir.mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up temporary files."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_experiment_initialization(self):
        """Test experiment can be initialized."""
        config = ExperimentConfig(
            name="Test Experiment",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        assert exp.config.name == "Test Experiment"
        assert exp.num_documents == 3

    def test_experiment_run_mock(self):
        """Test experiment runs successfully with mock LLM."""
        config = ExperimentConfig(
            name="Mock Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        results = exp.run()

        assert results.success is True
        assert results.experiment_name == "Mock Test"
        assert len(results.raw_results) > 0

    def test_experiment_analyze(self):
        """Test experiment analysis produces statistics."""
        config = ExperimentConfig(
            name="Analysis Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        # Run experiment
        exp.run()

        # Analyze
        stats = exp.analyze()

        assert "start" in stats
        assert "middle" in stats
        assert "end" in stats
        assert "accuracy" in stats["start"]

    def test_experiment_with_visualizations(self):
        """Test experiment with visualization generation."""
        config = ExperimentConfig(
            name="Viz Test",
            iterations=1,
            save_results=True,
            output_dir=self.output_dir,
            generate_visualizations=True,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        results = exp.run()

        assert results.success is True
        assert len(results.visualization_paths) > 0

    def test_experiment_generates_documents(self):
        """Test that experiment generates documents correctly."""
        config = ExperimentConfig(
            name="Doc Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=5,
            words_per_document=100,
        )

        # Access private method for testing
        data = exp._generate_data()

        assert "start" in data
        assert "middle" in data
        assert "end" in data
        assert len(data["start"]) == 5
        assert len(data["middle"]) == 5
        assert len(data["end"]) == 5

    def test_experiment_custom_fact(self):
        """Test experiment with custom fact and question."""
        config = ExperimentConfig(
            name="Custom Fact Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        custom_fact = "The capital of France is Paris."
        custom_question = "What is the capital of France?"
        custom_answer = "Paris"

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            fact=custom_fact,
            question=custom_question,
            expected_answer=custom_answer,
            llm_interface=MockOllamaInterface(),
        )

        assert exp.fact == custom_fact
        assert exp.question == custom_question
        assert exp.expected_answer == custom_answer

    def test_experiment_results_structure(self):
        """Test that experiment results have correct structure."""
        config = ExperimentConfig(
            name="Structure Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        results = exp.run()

        assert hasattr(results, "experiment_name")
        assert hasattr(results, "config")
        assert hasattr(results, "raw_results")
        assert hasattr(results, "statistics")
        assert hasattr(results, "visualization_paths")
        assert hasattr(results, "success")

    def test_experiment_with_small_documents(self):
        """Test experiment with minimum document size."""
        config = ExperimentConfig(
            name="Small Docs",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=2,
            words_per_document=100,  # Minimum
            llm_interface=MockOllamaInterface(),
        )

        results = exp.run()

        assert results.success is True

    def test_experiment_multiple_positions(self):
        """Test that all three positions are tested."""
        config = ExperimentConfig(
            name="Positions Test",
            iterations=1,
            save_results=False,
            generate_visualizations=False,
        )

        exp = NeedleInHaystackExperiment(
            config=config,
            num_documents=3,
            words_per_document=100,
            llm_interface=MockOllamaInterface(),
        )

        exp.run()

        # Check that results include all positions
        positions_tested = set(r["position"] for r in exp.results)
        assert "start" in positions_tested
        assert "middle" in positions_tested
        assert "end" in positions_tested
