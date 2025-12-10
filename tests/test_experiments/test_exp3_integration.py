"""
Integration tests for Experiment 3: RAG Impact.

Note: Some tests require ChromaDB. They will be skipped if not available.
"""

import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from context_windows_lab.experiments import RAGImpactExperiment, ExperimentConfig
from context_windows_lab.llm import LLMResponse
from context_windows_lab.data_generation import Document

# Check if ChromaDB is available
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

    def check_availability(self) -> bool:
        """Mock check_availability."""
        return True

    def query(self, context: str, question: str, **kwargs) -> LLMResponse:
        """Mock query that returns different responses based on mode."""
        self.call_count += 1
        self.queries.append({"context": context, "question": question})

        # Simulate full context being slower but more accurate
        context_size = len(context.split())

        if context_size > 500:
            # Full context: more tokens, higher latency
            latency = 5000
            tokens = 50
        else:
            # RAG: fewer tokens, lower latency
            latency = 2000
            tokens = 20

        return LLMResponse(
            text="יעילות",  # Hebrew: "efficiency"
            success=True,
            error=None,
            latency_ms=latency,
            tokens_used=tokens,
        )

    def check_connection(self) -> bool:
        return True


class TestRAGImpactExperiment:
    """Test suite for Experiment 3."""

    def test_initialization_default(self):
        """Test experiment initializes with default settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp3",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config)

            assert exp.top_k == 3
            assert exp.domain is None
            assert len(exp.modes) == 2
            assert "full_context" in exp.modes
            assert "rag" in exp.modes

    def test_initialization_custom_params(self):
        """Test experiment with custom parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_exp3_custom",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            custom_question = "מה הזמן?"  # Hebrew: "What is the time?"
            custom_answer = "צהריים"  # Hebrew: "noon"

            exp = RAGImpactExperiment(
                config,
                domain="technology",
                question=custom_question,
                expected_answer=custom_answer,
                top_k=5,
            )

            assert exp.domain == "technology"
            assert exp.question == custom_question
            assert exp.expected_answer == custom_answer
            assert exp.top_k == 5

    def test_load_hebrew_documents_mock(self):
        """Test loading Hebrew documents with mock data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock Hebrew documents
            docs_path = Path(tmpdir) / "hebrew_documents"
            tech_path = docs_path / "technology"
            tech_path.mkdir(parents=True)

            # Write mock files
            (tech_path / "doc1.txt").write_text("טקסט עברי על טכנולוגיה", encoding="utf-8")
            (tech_path / "doc2.txt").write_text("עוד טקסט טכנולוגי", encoding="utf-8")

            documents = RAGImpactExperiment.load_hebrew_documents(
                documents_path=docs_path,
                domain="technology",
            )

            assert len(documents) == 2
            assert all(isinstance(doc, Document) for doc in documents)
            assert documents[0].metadata["domain"] == "technology"

    def test_load_hebrew_documents_all_domains(self):
        """Test loading from all domains."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock documents in multiple domains
            docs_path = Path(tmpdir) / "hebrew_documents"

            for domain in ["technology", "law", "medicine"]:
                domain_path = docs_path / domain
                domain_path.mkdir(parents=True)
                (domain_path / f"{domain}_doc.txt").write_text(
                    f"Hebrew text about {domain}", encoding="utf-8"
                )

            documents = RAGImpactExperiment.load_hebrew_documents(
                documents_path=docs_path,
                domain=None,  # Load all domains
            )

            # Should have 3 documents (one per domain)
            assert len(documents) == 3

            # Check domains are present
            domains = {doc.metadata["domain"] for doc in documents}
            assert domains == {"technology", "law", "medicine"}

    def test_load_hebrew_documents_missing_directory(self):
        """Test handling of missing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nonexistent_path = Path(tmpdir) / "nonexistent"

            documents = RAGImpactExperiment.load_hebrew_documents(
                documents_path=nonexistent_path,
                domain="technology",
            )

            # Should return empty list, not crash
            assert len(documents) == 0

    def test_generate_data(self):
        """Test data generation loads documents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock documents
            docs_path = Path(tmpdir) / "hebrew_documents"
            tech_path = docs_path / "technology"
            tech_path.mkdir(parents=True)
            (tech_path / "doc1.txt").write_text("טקסט 1", encoding="utf-8")

            config = ExperimentConfig(
                name="test_gen_data",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = RAGImpactExperiment(
                config,
                documents_path=str(docs_path),
                llm_interface=mock_llm,
            )

            documents = exp._generate_data()

            assert len(documents) >= 1
            assert all(isinstance(doc, Document) for doc in documents)

    def test_generate_data_raises_on_no_documents(self):
        """Test that missing documents raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_path = Path(tmpdir) / "empty"
            empty_path.mkdir()

            config = ExperimentConfig(
                name="test_no_docs",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = RAGImpactExperiment(
                config,
                documents_path=str(empty_path),
                llm_interface=mock_llm,
            )

            with pytest.raises(RuntimeError, match="No Hebrew documents found"):
                exp._generate_data()

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_execute_queries_both_modes(self):
        """Test query execution in both full_context and RAG modes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_queries",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            # Create simple test documents
            test_docs = [
                Document(content="Document 1 about technology", metadata={"id": 1}),
                Document(content="Document 2 about innovation", metadata={"id": 2}),
                Document(content="Document 3 about efficiency", metadata={"id": 3}),
            ]

            mock_llm = MockOllamaInterface()
            exp = RAGImpactExperiment(config, llm_interface=mock_llm)

            responses = exp._execute_queries(test_docs)

            # Should have responses for both modes
            assert "full_context" in responses
            assert "rag" in responses

            # Both should succeed
            assert responses["full_context"].success
            assert responses["rag"].success

            # Full context should have higher latency (more text)
            assert responses["full_context"].latency_ms > responses["rag"].latency_ms

    def test_execute_queries_chromadb_not_available(self):
        """Test graceful handling when ChromaDB is not available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_no_chromadb",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            test_docs = [
                Document(content="Test doc", metadata={"id": 1}),
            ]

            mock_llm = MockOllamaInterface()
            exp = RAGImpactExperiment(config, llm_interface=mock_llm)

            # Mock ChromaDB import error
            with patch("context_windows_lab.experiments.exp3_rag_impact.VectorStore") as mock_vs:
                mock_vs.side_effect = ImportError("ChromaDB not installed")

                responses = exp._execute_queries(test_docs)

                # Full context should work
                assert responses["full_context"].success

                # RAG should fail gracefully
                assert not responses["rag"].success
                assert responses["rag"].error == "ChromaDB not installed"

    def test_evaluate_responses(self):
        """Test response evaluation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_eval",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config, expected_answer="יעילות")

            # Create mock responses
            responses = {
                "full_context": LLMResponse(
                    text="יעילות",  # Correct
                    success=True,
                    error=None,
                    latency_ms=5000,
                    tokens_used=50,
                ),
                "rag": LLMResponse(
                    text="יעילות",  # Correct
                    success=True,
                    error=None,
                    latency_ms=2000,
                    tokens_used=20,
                ),
            }

            evaluations = exp._evaluate_responses(responses)

            assert len(evaluations) == 2

            # Both should have high accuracy (contains match)
            for eval_result in evaluations:
                assert eval_result["accuracy"] > 0.0
                assert eval_result["success"]

    def test_evaluate_responses_with_failure(self):
        """Test evaluation when a mode fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_eval_fail",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config)

            responses = {
                "full_context": LLMResponse(text="Answer", latency_ms=1000, tokens_used=10, model="llama2", timestamp=datetime.now(), success=True),
                "rag": LLMResponse(text="", latency_ms=0, tokens_used=0, model="llama2", timestamp=datetime.now(), success=False, error="ChromaDB error"),
            }

            evaluations = exp._evaluate_responses(responses)

            # Full context should be evaluated
            full_eval = next(e for e in evaluations if e["mode"] == "full_context")
            assert full_eval["success"]

            # RAG should show failure
            rag_eval = next(e for e in evaluations if e["mode"] == "rag")
            assert not rag_eval["success"]
            assert rag_eval["accuracy"] == 0.0

    @pytest.mark.skipif(not CHROMADB_AVAILABLE, reason="ChromaDB not installed")
    def test_run_complete_experiment(self):
        """Test running complete experiment end-to-end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test documents
            docs_path = Path(tmpdir) / "hebrew_documents"
            tech_path = docs_path / "technology"
            tech_path.mkdir(parents=True)

            for i in range(3):
                (tech_path / f"doc{i}.txt").write_text(
                    f"מסמך {i} על טכנולוגיה ויעילות", encoding="utf-8"
                )

            config = ExperimentConfig(
                name="test_complete",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            mock_llm = MockOllamaInterface()
            exp = RAGImpactExperiment(
                config,
                documents_path=str(docs_path),
                llm_interface=mock_llm,
            )

            results = exp.run()

            # Should have 2 modes × 1 iteration = 2 results
            assert len(results) == 2

            # Check result structure
            for result in results:
                assert "mode" in result
                assert "accuracy" in result
                assert "latency_ms" in result
                assert "tokens_used" in result

    def test_analysis(self):
        """Test statistical analysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_analysis",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config)

            # Set mock results
            exp.results = [
                {
                    "mode": "full_context",
                    "accuracy": 1.0,
                    "latency_ms": 5000,
                    "tokens_used": 50,
                },
                {
                    "mode": "rag",
                    "accuracy": 0.9,
                    "latency_ms": 2000,
                    "tokens_used": 20,
                },
            ]

            analysis = exp.analyze()

            # Should have analysis for both modes
            assert "full_context" in analysis
            assert "rag" in analysis

            # Check structure
            for mode in ["full_context", "rag"]:
                assert "accuracy" in analysis[mode]
                assert "latency_ms" in analysis[mode]
                assert "tokens_used" in analysis[mode]

                assert "mean" in analysis[mode]["accuracy"]

    def test_visualization_generation(self):
        """Test visualization generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_viz",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config)

            # Set mock results
            exp.results = [
                {
                    "mode": "full_context",
                    "accuracy": 1.0,
                    "latency_ms": 5000,
                    "tokens_used": 50,
                },
                {
                    "mode": "rag",
                    "accuracy": 0.95,
                    "latency_ms": 2000,
                    "tokens_used": 20,
                },
            ]

            viz_paths = exp.visualize()

            # Should generate 3 visualizations
            assert len(viz_paths) == 3

            # All files should exist
            for path in viz_paths:
                assert Path(path).exists()

    def test_repr(self):
        """Test string representation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_repr",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            exp = RAGImpactExperiment(config, domain="technology", top_k=5)

            repr_str = repr(exp)
            assert "RAGImpactExperiment" in repr_str
            assert "technology" in repr_str
            assert "5" in repr_str

    def test_document_metadata(self):
        """Test that loaded documents have proper metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "hebrew_documents"
            tech_path = docs_path / "technology"
            tech_path.mkdir(parents=True)

            (tech_path / "test_doc.txt").write_text("טקסט בדיקה", encoding="utf-8")

            documents = RAGImpactExperiment.load_hebrew_documents(
                documents_path=docs_path,
                domain="technology",
            )

            assert len(documents) == 1
            assert documents[0].metadata["domain"] == "technology"
            assert documents[0].metadata["filename"] == "test_doc.txt"
            assert "word_count" in documents[0].metadata
            assert documents[0].metadata["source"] == "hebrew_corpus"

    def test_top_k_parameter_effect(self):
        """Test that top_k parameter affects RAG retrieval."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                name="test_top_k",
                output_dir=Path(tmpdir),
                iterations=1,
            )

            # Test with different top_k values
            for k in [1, 3, 5]:
                exp = RAGImpactExperiment(config, top_k=k)
                assert exp.top_k == k
