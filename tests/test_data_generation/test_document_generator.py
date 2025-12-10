"""
Unit tests for DocumentGenerator.

Tests cover:
- Document generation with different fact positions
- Input validation
- Fact embedding correctness
- Metadata creation
- Reproducibility with seed
- Edge cases
"""

import pytest

from context_windows_lab.data_generation.document_generator import (
    Document,
    DocumentGenerator,
)


class TestDocumentGenerator:
    """Test suite for DocumentGenerator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = DocumentGenerator(seed=42)
        self.fact = "The CEO of the company is David Cohen."
        self.question = "Who is the CEO of the company?"

    def test_initialization(self):
        """Test DocumentGenerator initialization."""
        gen = DocumentGenerator(seed=42)
        assert gen is not None
        assert hasattr(gen, "templates")
        assert hasattr(gen, "fact_library")
        assert hasattr(gen, "_rng")

    def test_initialization_without_seed(self):
        """Test initialization without seed for random generation."""
        gen1 = DocumentGenerator()
        gen2 = DocumentGenerator()
        # Both should initialize successfully
        assert gen1 is not None
        assert gen2 is not None

    def test_generate_documents_start_position(self):
        """Test generating documents with fact at start position."""
        num_docs = 5
        words_per_doc = 200

        documents = self.generator.generate_documents(
            num_docs=num_docs,
            words_per_doc=words_per_doc,
            fact=self.fact,
            fact_position="start",
        )

        assert len(documents) == num_docs

        for doc in documents:
            assert isinstance(doc, Document)
            assert doc.fact == self.fact
            assert doc.fact_position == "start"
            assert self.fact in doc.content
            # Fact should be near the beginning (within first 200 characters)
            fact_index = doc.content.index(self.fact)
            assert fact_index < 200  # Within first 200 characters

    def test_generate_documents_middle_position(self):
        """Test generating documents with fact in middle position."""
        num_docs = 5
        words_per_doc = 200

        documents = self.generator.generate_documents(
            num_docs=num_docs,
            words_per_doc=words_per_doc,
            fact=self.fact,
            fact_position="middle",
        )

        assert len(documents) == num_docs

        for doc in documents:
            assert isinstance(doc, Document)
            assert doc.fact == self.fact
            assert doc.fact_position == "middle"
            assert self.fact in doc.content
            # Fact should be in the middle third
            fact_index = doc.content.index(self.fact)
            content_length = len(doc.content)
            # Check it's roughly in the middle third
            assert content_length * 0.25 < fact_index < content_length * 0.75

    def test_generate_documents_end_position(self):
        """Test generating documents with fact at end position."""
        num_docs = 5
        words_per_doc = 200

        documents = self.generator.generate_documents(
            num_docs=num_docs,
            words_per_doc=words_per_doc,
            fact=self.fact,
            fact_position="end",
        )

        assert len(documents) == num_docs

        for doc in documents:
            assert isinstance(doc, Document)
            assert doc.fact == self.fact
            assert doc.fact_position == "end"
            assert self.fact in doc.content
            # Fact should be near the end
            fact_index = doc.content.index(self.fact)
            content_length = len(doc.content)
            assert fact_index > content_length - 200  # Within last 200 characters

    def test_document_metadata(self):
        """Test that document metadata is correctly populated."""
        documents = self.generator.generate_documents(
            num_docs=3,
            words_per_doc=100,
            fact=self.fact,
            fact_position="start",
        )

        for i, doc in enumerate(documents):
            assert "doc_id" in doc.metadata
            assert doc.metadata["doc_id"] == i
            assert "word_count" in doc.metadata
            assert doc.metadata["word_count"] > 0

    def test_word_count_accuracy(self):
        """Test that generated documents have approximately correct word count."""
        words_per_doc = 200
        documents = self.generator.generate_documents(
            num_docs=5,
            words_per_doc=words_per_doc,
            fact=self.fact,
            fact_position="middle",
        )

        for doc in documents:
            actual_word_count = len(doc.content.split())
            # Allow 10% variance in word count
            assert abs(actual_word_count - words_per_doc) < words_per_doc * 0.1

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same documents."""
        gen1 = DocumentGenerator(seed=123)
        gen2 = DocumentGenerator(seed=123)

        docs1 = gen1.generate_documents(5, 100, self.fact, "middle")
        docs2 = gen2.generate_documents(5, 100, self.fact, "middle")

        for d1, d2 in zip(docs1, docs2):
            assert d1.content == d2.content
            assert d1.fact_position == d2.fact_position

    def test_different_seeds_produce_different_documents(self):
        """Test that different seeds produce different documents."""
        gen1 = DocumentGenerator(seed=123)
        gen2 = DocumentGenerator(seed=456)

        docs1 = gen1.generate_documents(5, 100, self.fact, "middle")
        docs2 = gen2.generate_documents(5, 100, self.fact, "middle")

        # At least some documents should be different
        different = any(d1.content != d2.content for d1, d2 in zip(docs1, docs2))
        assert different

    def test_validation_invalid_num_docs(self):
        """Test validation rejects invalid num_docs."""
        with pytest.raises(ValueError, match="num_docs must be positive"):
            self.generator.generate_documents(
                num_docs=0,
                words_per_doc=100,
                fact=self.fact,
                fact_position="start",
            )

        with pytest.raises(ValueError, match="num_docs must be positive"):
            self.generator.generate_documents(
                num_docs=-5,
                words_per_doc=100,
                fact=self.fact,
                fact_position="start",
            )

    def test_validation_invalid_words_per_doc(self):
        """Test validation rejects invalid words_per_doc."""
        with pytest.raises(ValueError, match="words_per_doc must be >= 100"):
            self.generator.generate_documents(
                num_docs=5,
                words_per_doc=10,
                fact=self.fact,
                fact_position="start",
            )

    def test_validation_empty_fact(self):
        """Test validation rejects empty fact."""
        with pytest.raises(ValueError, match="fact cannot be empty"):
            self.generator.generate_documents(
                num_docs=5,
                words_per_doc=100,
                fact="",
                fact_position="start",
            )

    def test_validation_invalid_position(self):
        """Test validation rejects invalid fact position."""
        with pytest.raises(ValueError, match="fact_position must be one of"):
            self.generator.generate_documents(
                num_docs=5,
                words_per_doc=100,
                fact=self.fact,
                fact_position="invalid",
            )

    def test_fact_appears_exactly_once(self):
        """Test that fact appears exactly once in each document."""
        documents = self.generator.generate_documents(
            num_docs=5,
            words_per_doc=200,
            fact=self.fact,
            fact_position="middle",
        )

        for doc in documents:
            assert doc.content.count(self.fact) == 1

    def test_large_document_generation(self):
        """Test generating large documents."""
        documents = self.generator.generate_documents(
            num_docs=2,
            words_per_doc=1000,
            fact=self.fact,
            fact_position="middle",
        )

        assert len(documents) == 2
        for doc in documents:
            assert self.fact in doc.content
            assert len(doc.content.split()) >= 900  # Allow some variance

    def test_many_documents_generation(self):
        """Test generating many documents."""
        documents = self.generator.generate_documents(
            num_docs=50,
            words_per_doc=100,
            fact=self.fact,
            fact_position="start",
        )

        assert len(documents) == 50
        for doc in documents:
            assert self.fact in doc.content

    def test_document_dataclass_fields(self):
        """Test Document dataclass has all required fields."""
        doc = Document(
            content="Test content",
            fact="Test fact",
            fact_position="start",
            metadata={"doc_id": 0},
        )

        assert doc.content == "Test content"
        assert doc.fact == "Test fact"
        assert doc.fact_position == "start"
        assert doc.metadata == {"doc_id": 0}

    def test_custom_templates(self):
        """Test using custom templates."""
        custom_templates = [
            "This is a custom template about {subject} {verb} {object}.",
            "Another custom template for {subject} {verb} {object}.",
        ]

        gen = DocumentGenerator(templates=custom_templates, seed=42)
        documents = gen.generate_documents(
            num_docs=2,
            words_per_doc=100,  # Changed from 50 to meet minimum
            fact=self.fact,
            fact_position="start",
        )

        assert len(documents) == 2
        for doc in documents:
            assert self.fact in doc.content

    def test_custom_fact_library(self):
        """Test using custom fact library."""
        custom_facts = {
            "topic1": ["Fact 1", "Fact 2"],
            "topic2": ["Fact 3", "Fact 4"],
        }

        gen = DocumentGenerator(fact_library=custom_facts, seed=42)
        documents = gen.generate_documents(
            num_docs=2,
            words_per_doc=100,  # Changed from 50 to meet minimum
            fact=self.fact,
            fact_position="middle",
        )

        assert len(documents) == 2
        for doc in documents:
            assert self.fact in doc.content
