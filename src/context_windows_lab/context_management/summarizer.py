"""
Summarizer for Context Compression

Provides simple text summarization for the COMPRESS strategy in Experiment 4.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Summarizer:
    """
    Simple text summarizer for context compression.

    Uses basic extractive summarization (selecting key sentences)
    or truncation strategies.
    """

    def __init__(self, max_words: int = 200):
        """
        Initialize summarizer.

        Args:
            max_words: Maximum words in summary
        """
        self.max_words = max_words

    def summarize(self, text: str, method: str = "truncate") -> str:
        """
        Summarize text using specified method.

        Args:
            text: Text to summarize
            method: Summarization method ("truncate", "first_last", "middle")

        Returns:
            Summarized text
        """
        if not text:
            return ""

        words = text.split()

        # If already short enough, return as-is
        if len(words) <= self.max_words:
            return text

        if method == "truncate":
            # Simple truncation: take first max_words
            summary_words = words[:self.max_words]
            return " ".join(summary_words) + "..."

        elif method == "first_last":
            # Take first and last portions
            half = self.max_words // 2
            first_part = words[:half]
            last_part = words[-half:]
            return " ".join(first_part) + " [...] " + " ".join(last_part)

        elif method == "middle":
            # Keep middle portion (useful for some cases)
            start_idx = (len(words) - self.max_words) // 2
            end_idx = start_idx + self.max_words
            summary_words = words[start_idx:end_idx]
            return "[...] " + " ".join(summary_words) + " [...]"

        else:
            # Default to truncation
            summary_words = words[:self.max_words]
            return " ".join(summary_words) + "..."

    def __repr__(self) -> str:
        """String representation."""
        return f"Summarizer(max_words={self.max_words})"
