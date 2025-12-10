"""
Accuracy Evaluator - Building Block for Response Evaluation

This module provides the AccuracyEvaluator class for measuring the accuracy
of LLM responses against expected answers.
"""

import re
from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class EvaluationResult:
    """Represents the result of evaluating a response."""

    score: float  # 0.0 to 1.0
    method: str
    response: str
    expected: str
    match_details: Optional[dict] = None


class AccuracyEvaluator:
    """
    Evaluate LLM response accuracy against expected answers.

    This building block provides multiple evaluation methods for measuring
    how accurately the LLM responded to a query.

    Input Data:
        - response: LLM response text
        - expected: Expected answer

    Output Data:
        - float: Accuracy score (0.0 to 1.0)
        - EvaluationResult: Detailed evaluation with metadata

    Setup Data:
        - method: Evaluation method (exact, contains, semantic)
        - case_sensitive: Whether to use case-sensitive matching
    """

    def __init__(
        self,
        method: Literal["exact", "contains", "partial"] = "contains",
        case_sensitive: bool = False,
    ):
        """
        Initialize AccuracyEvaluator.

        Args:
            method: Evaluation method to use
            case_sensitive: Whether to use case-sensitive matching
        """
        valid_methods = ["exact", "contains", "partial"]
        if method not in valid_methods:
            raise ValueError(f"method must be one of {valid_methods}, got {method}")

        self.method = method
        self.case_sensitive = case_sensitive

    def evaluate(self, response: str, expected: str) -> float:
        """
        Evaluate response accuracy.

        Args:
            response: LLM response text
            expected: Expected answer

        Returns:
            Accuracy score (0.0 to 1.0)
        """
        result = self.evaluate_detailed(response, expected)
        return result.score

    def evaluate_detailed(self, response: str, expected: str) -> EvaluationResult:
        """
        Evaluate response with detailed results.

        Args:
            response: LLM response text
            expected: Expected answer

        Returns:
            EvaluationResult with score and details
        """
        self._validate_inputs(response, expected)

        # Preprocess
        resp = self._preprocess(response)
        exp = self._preprocess(expected)

        # Evaluate based on method
        if self.method == "exact":
            score = self._exact_match(resp, exp)
        elif self.method == "contains":
            score = self._contains_match(resp, exp)
        else:  # partial
            score = self._partial_match(resp, exp)

        return EvaluationResult(
            score=score,
            method=self.method,
            response=response,
            expected=expected,
            match_details={"preprocessed_response": resp, "preprocessed_expected": exp},
        )

    def _exact_match(self, response: str, expected: str) -> float:
        """
        Check for exact string match.

        Args:
            response: Preprocessed response
            expected: Preprocessed expected answer

        Returns:
            1.0 if exact match, 0.0 otherwise
        """
        return 1.0 if response == expected else 0.0

    def _contains_match(self, response: str, expected: str) -> float:
        """
        Check if response contains expected answer.

        Args:
            response: Preprocessed response
            expected: Preprocessed expected answer

        Returns:
            1.0 if response contains expected, 0.0 otherwise
        """
        return 1.0 if expected in response else 0.0

    def _partial_match(self, response: str, expected: str) -> float:
        """
        Calculate partial match score based on word overlap.

        Args:
            response: Preprocessed response
            expected: Preprocessed expected answer

        Returns:
            Score between 0.0 and 1.0 based on word overlap
        """
        response_words = set(response.split())
        expected_words = set(expected.split())

        if not expected_words:
            return 0.0

        # Calculate Jaccard similarity
        intersection = response_words & expected_words
        union = response_words | expected_words

        return len(intersection) / len(union) if union else 0.0

    def _preprocess(self, text: str) -> str:
        """
        Preprocess text for comparison.

        Args:
            text: Text to preprocess

        Returns:
            Preprocessed text
        """
        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove common punctuation
        text = re.sub(r'[.,!?;:"]', "", text)

        # Case normalization
        if not self.case_sensitive:
            text = text.lower()

        return text.strip()

    def _validate_inputs(self, response: str, expected: str) -> None:
        """
        Validate evaluation inputs.

        Args:
            response: Response string
            expected: Expected string

        Raises:
            ValueError: If inputs are invalid
        """
        if not isinstance(response, str):
            raise ValueError(f"response must be string, got {type(response)}")

        if not isinstance(expected, str):
            raise ValueError(f"expected must be string, got {type(expected)}")

    def __repr__(self) -> str:
        """String representation of AccuracyEvaluator."""
        return (
            f"AccuracyEvaluator(method='{self.method}', " f"case_sensitive={self.case_sensitive})"
        )
