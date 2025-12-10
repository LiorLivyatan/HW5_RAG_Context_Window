"""
Unit tests for AccuracyEvaluator.

Tests cover:
- Exact match evaluation
- Contains match evaluation
- Partial match evaluation (Jaccard similarity)
- Case sensitivity handling
- Edge cases
"""

import pytest

from context_windows_lab.evaluation.accuracy_evaluator import (
    AccuracyEvaluator,
    EvaluationResult,
)


class TestAccuracyEvaluator:
    """Test suite for AccuracyEvaluator class."""

    def test_exact_match_success(self):
        """Test exact match when response equals expected."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=True)

        response = "David Cohen"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_exact_match_failure(self):
        """Test exact match when response doesn't equal expected."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=True)

        response = "David Cohen is the CEO"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_exact_match_case_insensitive(self):
        """Test exact match with case insensitivity."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=False)

        response = "david cohen"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_contains_match_success(self):
        """Test contains match when expected is in response."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)

        response = "The CEO of the company is David Cohen."
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_contains_match_failure(self):
        """Test contains match when expected is not in response."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)

        response = "The CEO is unknown."
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_contains_match_case_sensitive(self):
        """Test contains match with case sensitivity."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=True)

        response = "The CEO is david cohen"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_partial_match_full_overlap(self):
        """Test partial match with 100% word overlap."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "David Cohen"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_partial_match_no_overlap(self):
        """Test partial match with no word overlap."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "John Smith"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_partial_match_some_overlap(self):
        """Test partial match with partial word overlap."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "David Smith"
        expected = "David Cohen"

        # Intersection: {David} = 1
        # Union: {David, Smith, Cohen} = 3
        # Score: 1/3 ≈ 0.333
        score = evaluator.evaluate(response, expected)
        assert 0.3 < score < 0.4

    def test_evaluate_detailed_exact(self):
        """Test detailed evaluation for exact match."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=False)

        response = "David Cohen"
        expected = "David Cohen"

        result = evaluator.evaluate_detailed(response, expected)

        assert isinstance(result, EvaluationResult)
        assert result.score == 1.0
        assert result.method == "exact"
        assert result.response == response  # Original, not normalized
        assert result.expected == expected  # Original, not normalized
        # Check that preprocessing happened in match_details
        assert "preprocessed_response" in result.match_details
        assert result.match_details["preprocessed_response"] == "david cohen"

    def test_evaluate_detailed_contains(self):
        """Test detailed evaluation for contains match."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)

        response = "The answer is David Cohen"
        expected = "David Cohen"

        result = evaluator.evaluate_detailed(response, expected)

        assert result.score == 1.0
        assert result.method == "contains"

    def test_evaluate_detailed_partial(self):
        """Test detailed evaluation for partial match."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "David Smith"
        expected = "David Cohen"

        result = evaluator.evaluate_detailed(response, expected)

        assert 0.0 < result.score < 1.0
        assert result.method == "partial"
        assert result.match_details is not None

    def test_default_method_is_contains(self):
        """Test that default evaluation method is 'contains'."""
        evaluator = AccuracyEvaluator()

        response = "The CEO is David Cohen"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_default_case_insensitive(self):
        """Test that default is case insensitive."""
        evaluator = AccuracyEvaluator()

        response = "DAVID COHEN"
        expected = "david cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_empty_response(self):
        """Test handling of empty response."""
        evaluator = AccuracyEvaluator(method="contains")

        response = ""
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_empty_expected(self):
        """Test handling of empty expected answer."""
        evaluator = AccuracyEvaluator(method="partial")

        response = "Some response"
        expected = ""

        score = evaluator.evaluate(response, expected)
        assert score == 0.0

    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=False)

        response = "  David Cohen  "
        expected = "David Cohen"

        # Should normalize whitespace
        result = evaluator.evaluate_detailed(response, expected)
        assert result.score == 1.0

    def test_invalid_method_raises_error(self):
        """Test that invalid method raises ValueError."""
        with pytest.raises(ValueError, match="method must be one of"):
            AccuracyEvaluator(method="invalid")

    def test_multiword_contains(self):
        """Test contains match with multi-word expected answer."""
        evaluator = AccuracyEvaluator(method="contains")

        response = (
            "Based on the passage, the CEO of the company is David Cohen, who founded it in 2010."
        )
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_partial_match_calculates_jaccard(self):
        """Test that partial match calculates Jaccard similarity correctly."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "apple banana cherry"
        expected = "banana cherry date"

        # Intersection: {banana, cherry} = 2
        # Union: {apple, banana, cherry, date} = 4
        # Jaccard: 2/4 = 0.5
        score = evaluator.evaluate(response, expected)
        assert score == 0.5

    def test_evaluation_result_dataclass(self):
        """Test EvaluationResult dataclass fields."""
        result = EvaluationResult(
            score=0.85,
            method="contains",
            response="test response",
            expected="test expected",
            match_details={"detail": "value"},
        )

        assert result.score == 0.85
        assert result.method == "contains"
        assert result.response == "test response"
        assert result.expected == "test expected"
        assert result.match_details == {"detail": "value"}

    def test_case_sensitive_exact_match(self):
        """Test case-sensitive exact matching."""
        evaluator = AccuracyEvaluator(method="exact", case_sensitive=True)

        # Should fail
        assert evaluator.evaluate("David Cohen", "david cohen") == 0.0

        # Should succeed
        assert evaluator.evaluate("David Cohen", "David Cohen") == 1.0

    def test_case_sensitive_contains_match(self):
        """Test case-sensitive contains matching."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=True)

        response = "The CEO is David Cohen"

        # Should succeed
        assert evaluator.evaluate(response, "David Cohen") == 1.0

        # Should fail (case mismatch)
        assert evaluator.evaluate(response, "david cohen") == 0.0

    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)

        response = 'המנכ"ל הוא David Cohen'
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_special_characters(self):
        """Test handling of special characters."""
        evaluator = AccuracyEvaluator(method="contains", case_sensitive=False)

        response = "The answer is: David Cohen (CEO)"
        expected = "David Cohen"

        score = evaluator.evaluate(response, expected)
        assert score == 1.0

    def test_partial_match_with_punctuation(self):
        """Test partial match strips punctuation correctly."""
        evaluator = AccuracyEvaluator(method="partial", case_sensitive=False)

        response = "David, Cohen."
        expected = "David Cohen"

        # After normalization, should have high overlap
        score = evaluator.evaluate(response, expected)
        assert score > 0.5
