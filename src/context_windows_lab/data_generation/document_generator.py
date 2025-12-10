"""
Document Generator - Building Block for Synthetic Data Creation

This module provides the DocumentGenerator class for creating synthetic documents
with embedded facts at specified positions (start, middle, end).
"""

import random
from dataclasses import dataclass
from typing import List, Literal, Optional, Dict, Any


@dataclass
class Document:
    """
    Represents a document (either synthetic with embedded fact or real document).

    For synthetic documents: fact and fact_position are required.
    For real documents (e.g., Hebrew corpus): fact and fact_position are None.
    """

    content: str
    fact: Optional[str] = None
    fact_position: Optional[Literal["start", "middle", "end"]] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}

    def __len__(self) -> int:
        """Return word count of document."""
        return len(self.content.split())


class DocumentGenerator:
    """
    Generate synthetic documents with embedded critical facts.

    This building block creates test documents with configurable parameters,
    embedding facts at specific positions for context window experiments.

    Input Data:
        - num_docs: Number of documents to generate
        - words_per_doc: Target word count per document
        - fact: Critical fact to embed
        - fact_position: Where to place the fact (start/middle/end)

    Output Data:
        - List[Document]: Generated documents with metadata

    Setup Data:
        - templates: Text generation templates
        - fact_library: Pre-defined facts for testing
        - seed: Random seed for reproducibility
    """

    def __init__(
        self,
        templates: Optional[List[str]] = None,
        fact_library: Optional[List[str]] = None,
        seed: Optional[int] = None,
    ):
        """
        Initialize DocumentGenerator.

        Args:
            templates: Text templates for filler content (optional)
            fact_library: Library of pre-defined facts (optional)
            seed: Random seed for reproducibility (optional)
        """
        self.templates = templates or self._default_templates()
        self.fact_library = fact_library or self._default_fact_library()

        if seed is not None:
            random.seed(seed)
            self._rng = random.Random(seed)
        else:
            self._rng = random.Random()

    def generate_documents(
        self,
        num_docs: int,
        words_per_doc: int,
        fact: str,
        fact_position: Literal["start", "middle", "end"],
    ) -> List[Document]:
        """
        Generate synthetic documents with embedded fact.

        Args:
            num_docs: Number of documents to generate
            words_per_doc: Target word count per document
            fact: Critical fact to embed in each document
            fact_position: Position to place fact (start/middle/end)

        Returns:
            List of Document objects with embedded facts

        Raises:
            ValueError: If parameters are invalid
        """
        self._validate_inputs(num_docs, words_per_doc, fact, fact_position)

        documents = []
        for i in range(num_docs):
            # Generate filler text
            filler_text = self._generate_filler_text(words_per_doc)

            # Embed fact at specified position
            content = self._embed_fact(filler_text, fact, fact_position)

            # Create document with metadata
            doc = Document(
                content=content,
                fact=fact,
                fact_position=fact_position,
                metadata={
                    "doc_id": i,
                    "word_count": len(content.split()),
                    "target_words": words_per_doc,
                    "generated_by": "DocumentGenerator",
                },
            )
            documents.append(doc)

        return documents

    def _generate_filler_text(self, target_words: int) -> str:
        """
        Generate filler text with approximately target_words words.

        Args:
            target_words: Target word count

        Returns:
            Generated filler text
        """
        text_parts = []
        current_words = 0

        while current_words < target_words:
            # Select random template
            template = self._rng.choice(self.templates)

            # Fill template with random content
            filled = self._fill_template(template)
            words_in_filled = len(filled.split())

            # Check if adding this would exceed target
            if current_words + words_in_filled <= target_words + 10:
                text_parts.append(filled)
                current_words += words_in_filled
            else:
                # Generate smaller chunk to reach target
                remaining = target_words - current_words
                if remaining > 0:
                    partial = " ".join(filled.split()[:remaining])
                    text_parts.append(partial)
                break

        return " ".join(text_parts)

    def _embed_fact(
        self,
        text: str,
        fact: str,
        position: Literal["start", "middle", "end"],
    ) -> str:
        """
        Embed a fact at specified position in text.

        Args:
            text: Base text to embed fact into
            fact: Fact to embed
            position: Position to place fact

        Returns:
            Text with embedded fact
        """
        words = text.split()

        if position == "start":
            # Insert at beginning (after first sentence)
            insert_idx = min(20, len(words) // 4)
        elif position == "middle":
            # Insert in the middle
            insert_idx = len(words) // 2
        else:  # end
            # Insert near the end (before last sentence)
            insert_idx = max(len(words) - 20, 3 * len(words) // 4)

        # Insert fact
        words.insert(insert_idx, fact)

        return " ".join(words)

    def _fill_template(self, template: str) -> str:
        """
        Fill a template with random content.

        Args:
            template: Template string with placeholders

        Returns:
            Filled template
        """
        # Simple template filling - replace {subject}, {verb}, {object}
        subjects = ["The company", "The team", "The project", "The system", "The data"]
        verbs = ["requires", "needs", "provides", "supports", "manages"]
        objects = [
            "careful analysis",
            "detailed planning",
            "comprehensive testing",
            "thorough review",
            "systematic approach",
        ]

        result = template
        result = result.replace("{subject}", self._rng.choice(subjects))
        result = result.replace("{verb}", self._rng.choice(verbs))
        result = result.replace("{object}", self._rng.choice(objects))

        return result

    def _validate_inputs(
        self,
        num_docs: int,
        words_per_doc: int,
        fact: str,
        fact_position: str,
    ) -> None:
        """
        Validate input parameters.

        Args:
            num_docs: Number of documents
            words_per_doc: Words per document
            fact: Fact string
            fact_position: Position for fact

        Raises:
            ValueError: If any parameter is invalid
        """
        if num_docs <= 0:
            raise ValueError(f"num_docs must be positive, got {num_docs}")

        if words_per_doc < 100:
            raise ValueError(
                f"words_per_doc must be >= 100 for meaningful documents, got {words_per_doc}"
            )

        if not fact or not fact.strip():
            raise ValueError("fact cannot be empty")

        valid_positions = ["start", "middle", "end"]
        if fact_position not in valid_positions:
            raise ValueError(
                f"fact_position must be one of {valid_positions}, got {fact_position}"
            )

    @staticmethod
    def _default_templates() -> List[str]:
        """Return default text generation templates."""
        return [
            "{subject} {verb} {object} for optimal performance and efficiency.",
            "In recent developments, {subject} has demonstrated the need for {object}.",
            "According to industry standards, {subject} {verb} {object} to ensure quality.",
            "Research indicates that {subject} {verb} {object} in most scenarios.",
            "The implementation of {subject} {verb} {object} across all departments.",
            "Historical data shows that {subject} consistently {verb} {object}.",
            "Best practices suggest that {subject} should prioritize {object}.",
            "Technical documentation confirms that {subject} {verb} {object}.",
            "Stakeholder feedback emphasizes that {subject} {verb} {object}.",
            "Performance metrics reveal that {subject} {verb} {object} effectively.",
        ]

    @staticmethod
    def _default_fact_library() -> List[str]:
        """Return default library of facts for testing."""
        return [
            "The CEO of the company is David Cohen.",
            "The project deadline is December 15th, 2025.",
            "The annual budget is $2.5 million dollars.",
            "The main office is located in Tel Aviv, Israel.",
            "The product launch date is scheduled for March 10th, 2026.",
            "The team consists of 47 employees across 3 departments.",
            "The primary color scheme is blue and white.",
            "The customer satisfaction rating is 4.8 out of 5 stars.",
            "The system supports up to 10,000 concurrent users.",
            "The encryption standard used is AES-256.",
        ]
