"""
Tests for Summarizer text compression component.
"""

import pytest

from context_windows_lab.context_management.summarizer import Summarizer


class TestSummarizer:
    """Test suite for Summarizer class."""

    def test_initialization(self):
        """Test summarizer initializes with default max_words."""
        summarizer = Summarizer()
        assert summarizer.max_words == 200

    def test_initialization_custom_max_words(self):
        """Test summarizer with custom max_words."""
        summarizer = Summarizer(max_words=100)
        assert summarizer.max_words == 100

    def test_summarize_empty_text(self):
        """Test summarizing empty text returns empty string."""
        summarizer = Summarizer()
        result = summarizer.summarize("")
        assert result == ""

    def test_summarize_short_text_unchanged(self):
        """Test that text shorter than max_words is returned unchanged."""
        summarizer = Summarizer(max_words=100)
        text = "This is a short text with only ten words here."

        result = summarizer.summarize(text)
        assert result == text  # Should be unchanged

    def test_summarize_truncate_method(self):
        """Test truncate method takes first N words."""
        summarizer = Summarizer(max_words=10)
        text = "One two three four five six seven eight nine ten eleven twelve thirteen."

        result = summarizer.summarize(text, method="truncate")

        # Should have first 10 words + ellipsis
        assert result.startswith("One two three four five")
        assert result.endswith("...")
        assert len(result.split()) <= 11  # 10 words + "..."

    def test_summarize_first_last_method(self):
        """Test first_last method takes first and last portions."""
        summarizer = Summarizer(max_words=10)
        text = " ".join([f"word{i}" for i in range(1, 21)])  # 20 words

        result = summarizer.summarize(text, method="first_last")

        # Should have first 5 and last 5 words
        assert "word1" in result
        assert "word2" in result
        assert "word19" in result
        assert "word20" in result
        assert "[...]" in result  # Separator

    def test_summarize_middle_method(self):
        """Test middle method takes middle portion."""
        summarizer = Summarizer(max_words=10)
        text = " ".join([f"word{i}" for i in range(1, 31)])  # 30 words

        result = summarizer.summarize(text, method="middle")

        # Should have middle portion
        assert result.startswith("[...]")
        assert result.endswith("[...]")
        # Middle 10 words from 30 total (starting at index 10)
        assert "word11" in result or "word15" in result

    def test_summarize_unknown_method_defaults_to_truncate(self):
        """Test that unknown method defaults to truncate."""
        summarizer = Summarizer(max_words=10)
        text = " ".join([f"word{i}" for i in range(1, 21)])

        result = summarizer.summarize(text, method="unknown_method")

        # Should behave like truncate
        assert "word1" in result
        assert result.endswith("...")

    def test_summarize_exact_max_words(self):
        """Test text with exactly max_words is unchanged."""
        summarizer = Summarizer(max_words=10)
        words = [f"word{i}" for i in range(1, 11)]  # Exactly 10 words
        text = " ".join(words)

        result = summarizer.summarize(text)
        assert result == text

    def test_summarize_one_word_over_limit(self):
        """Test text with max_words + 1 gets truncated."""
        summarizer = Summarizer(max_words=10)
        words = [f"word{i}" for i in range(1, 12)]  # 11 words
        text = " ".join(words)

        result = summarizer.summarize(text, method="truncate")
        assert "word11" not in result  # Last word removed
        assert "word10" in result

    def test_summarize_large_text(self):
        """Test summarizing large text."""
        summarizer = Summarizer(max_words=50)
        text = "Lorem ipsum dolor sit amet " * 100  # 500 words

        result = summarizer.summarize(text, method="truncate")
        word_count = len(result.split())

        # Should be close to 50 words (plus ellipsis)
        assert word_count <= 52

    def test_summarize_preserves_word_boundaries(self):
        """Test that summarization doesn't split words."""
        summarizer = Summarizer(max_words=5)
        text = "The quick brown fox jumps over the lazy dog."

        result = summarizer.summarize(text, method="truncate")

        # Should have complete words - check word count
        words_in_result = [w for w in result.split() if w not in ["..."]]
        assert len(words_in_result) == 5  # Exactly 5 complete words
        assert "The quick brown fox jumps" in result

    def test_summarize_with_punctuation(self):
        """Test summarization with punctuated text."""
        summarizer = Summarizer(max_words=10)
        text = "Hello, world! This is a test. It has punctuation?"

        result = summarizer.summarize(text, method="truncate")
        # Should preserve punctuation
        assert "," in result or "!" in result

    def test_repr(self):
        """Test string representation."""
        summarizer = Summarizer(max_words=150)
        repr_str = repr(summarizer)

        assert "Summarizer" in repr_str
        assert "150" in repr_str

    def test_multiple_spaces_handling(self):
        """Test that multiple spaces are handled correctly."""
        summarizer = Summarizer(max_words=5)
        text = "Word1   word2    word3     word4      word5 word6"

        result = summarizer.summarize(text, method="truncate")
        # Should still truncate to 5 words
        assert "word6" not in result

    def test_newlines_and_tabs(self):
        """Test text with newlines and tabs."""
        summarizer = Summarizer(max_words=10)
        text = "Line1\nLine2\tWord3\nWord4 Word5 " + " ".join([f"w{i}" for i in range(20)])

        result = summarizer.summarize(text, method="truncate")
        # Should handle whitespace correctly
        assert len(result.split()) <= 11

    def test_first_last_odd_max_words(self):
        """Test first_last with odd max_words."""
        summarizer = Summarizer(max_words=11)  # Odd number
        text = " ".join([f"word{i}" for i in range(1, 31)])

        result = summarizer.summarize(text, method="first_last")

        # Should split evenly (5 and 5, since 11//2 = 5)
        assert "word1" in result
        assert "word30" in result

    def test_max_words_of_one(self):
        """Test edge case with max_words=1."""
        summarizer = Summarizer(max_words=1)
        text = "One two three four five"

        result = summarizer.summarize(text, method="truncate")
        assert result == "One..."

    def test_use_case_compress_context(self):
        """Test realistic use case: compressing long context."""
        summarizer = Summarizer(max_words=100)

        # Simulate long document context
        long_context = (
            """
        The company was founded in 1995 and has grown significantly over the years.
        Our mission is to provide excellent service to our customers worldwide.
        We have offices in New York, London, Tokyo, and Sydney.
        """
            * 20
        )  # Repeat to make it long

        # Compress using truncate
        compressed = summarizer.summarize(long_context, method="truncate")
        assert len(compressed.split()) <= 101  # max_words + ellipsis

        # Compress using first_last
        compressed_fl = summarizer.summarize(long_context, method="first_last")
        assert "[...]" in compressed_fl
        assert "founded" in compressed_fl  # From beginning
        assert "Sydney" in compressed_fl  # From end

    def test_use_case_different_max_words(self):
        """Test same text with different max_words settings."""
        text = " ".join([f"word{i}" for i in range(1, 101)])  # 100 words

        summarizer_50 = Summarizer(max_words=50)
        summarizer_25 = Summarizer(max_words=25)

        result_50 = summarizer_50.summarize(text, method="truncate")
        result_25 = summarizer_25.summarize(text, method="truncate")

        # Should produce different length results
        assert len(result_50.split()) > len(result_25.split())

    def test_default_method(self):
        """Test that default method is truncate."""
        summarizer = Summarizer(max_words=10)
        text = " ".join([f"word{i}" for i in range(1, 21)])

        # Call without specifying method
        result = summarizer.summarize(text)

        # Should use truncate by default
        assert "word1" in result
        assert result.endswith("...")
