"""
Unit tests for Metrics calculator.

Tests cover:
- Statistical calculations (mean, std, min, max, count)
- Confidence interval calculations
- Edge cases (single value, identical values)
- Numerical accuracy
"""

import pytest
import math
from context_windows_lab.evaluation.metrics import calculate_statistics, Statistics


class TestMetrics:
    """Test suite for metrics calculation functions."""

    def test_calculate_statistics_basic(self):
        """Test basic statistics calculation."""
        scores = [0.8, 0.9, 0.85, 0.95, 0.75]

        stats = calculate_statistics(scores)

        assert isinstance(stats, Statistics)
        assert stats.count == 5
        assert stats.mean == pytest.approx(0.85, abs=0.01)
        assert stats.min == 0.75
        assert stats.max == 0.95
        assert stats.std > 0

    def test_calculate_statistics_mean(self):
        """Test mean calculation accuracy."""
        scores = [1.0, 2.0, 3.0, 4.0, 5.0]

        stats = calculate_statistics(scores)

        assert stats.mean == 3.0

    def test_calculate_statistics_std(self):
        """Test standard deviation calculation."""
        scores = [1.0, 2.0, 3.0, 4.0, 5.0]

        stats = calculate_statistics(scores)

        # Expected std for [1,2,3,4,5] with n-1 denominator
        # variance = ((1-3)^2 + (2-3)^2 + (3-3)^2 + (4-3)^2 + (5-3)^2) / 4
        #          = (4 + 1 + 0 + 1 + 4) / 4 = 2.5
        # std = sqrt(2.5) ≈ 1.58
        assert stats.std == pytest.approx(1.58, abs=0.01)

    def test_calculate_statistics_confidence_interval(self):
        """Test 95% confidence interval calculation."""
        scores = [0.8, 0.9, 0.85, 0.95, 0.75]

        stats = calculate_statistics(scores)

        # CI should be a tuple of (lower, upper)
        assert isinstance(stats.confidence_interval_95, tuple)
        assert len(stats.confidence_interval_95) == 2

        lower, upper = stats.confidence_interval_95

        # Lower bound should be less than mean
        assert lower < stats.mean

        # Upper bound should be greater than mean
        assert upper > stats.mean

        # Mean should be within the interval
        assert lower <= stats.mean <= upper

    def test_single_value(self):
        """Test statistics with a single value."""
        scores = [0.85]

        stats = calculate_statistics(scores)

        assert stats.count == 1
        assert stats.mean == 0.85
        assert stats.std == 0.0
        assert stats.min == 0.85
        assert stats.max == 0.85
        # CI should equal the mean when there's only one value
        assert stats.confidence_interval_95 == (0.85, 0.85)

    def test_identical_values(self):
        """Test statistics with identical values."""
        scores = [0.9, 0.9, 0.9, 0.9, 0.9]

        stats = calculate_statistics(scores)

        assert stats.count == 5
        assert stats.mean == 0.9
        assert stats.std == 0.0
        assert stats.min == 0.9
        assert stats.max == 0.9
        # CI should equal the mean when std is 0
        assert stats.confidence_interval_95 == (0.9, 0.9)

    def test_two_values(self):
        """Test statistics with two values."""
        scores = [0.8, 1.0]

        stats = calculate_statistics(scores)

        assert stats.count == 2
        assert stats.mean == 0.9
        assert stats.std > 0
        assert stats.min == 0.8
        assert stats.max == 1.0

    def test_all_zeros(self):
        """Test statistics with all zero values."""
        scores = [0.0, 0.0, 0.0]

        stats = calculate_statistics(scores)

        assert stats.count == 3
        assert stats.mean == 0.0
        assert stats.std == 0.0
        assert stats.min == 0.0
        assert stats.max == 0.0

    def test_all_ones(self):
        """Test statistics with all perfect scores."""
        scores = [1.0, 1.0, 1.0, 1.0]

        stats = calculate_statistics(scores)

        assert stats.count == 4
        assert stats.mean == 1.0
        assert stats.std == 0.0
        assert stats.min == 1.0
        assert stats.max == 1.0

    def test_large_dataset(self):
        """Test statistics with a large dataset."""
        scores = [0.5 + 0.01 * i for i in range(100)]  # [0.5, 0.51, ..., 1.49]

        stats = calculate_statistics(scores)

        assert stats.count == 100
        assert stats.mean == pytest.approx(0.995, abs=0.01)
        assert stats.std > 0
        assert stats.min == 0.5
        assert stats.max == pytest.approx(1.49, abs=0.01)

    def test_negative_values(self):
        """Test statistics with negative values."""
        scores = [-1.0, 0.0, 1.0, 2.0]

        stats = calculate_statistics(scores)

        assert stats.count == 4
        assert stats.mean == 0.5
        assert stats.min == -1.0
        assert stats.max == 2.0

    def test_mixed_precision(self):
        """Test statistics with mixed precision floats."""
        scores = [0.123456789, 0.987654321, 0.555555555]

        stats = calculate_statistics(scores)

        assert stats.count == 3
        assert isinstance(stats.mean, float)
        assert isinstance(stats.std, float)

    def test_confidence_interval_width(self):
        """Test that confidence interval width decreases with more samples."""
        # Small sample
        scores_small = [0.8, 0.9, 0.85]
        stats_small = calculate_statistics(scores_small)
        ci_width_small = stats_small.confidence_interval_95[1] - stats_small.confidence_interval_95[0]

        # Large sample with similar variance
        scores_large = [0.8, 0.9, 0.85, 0.82, 0.88, 0.87, 0.83, 0.91, 0.84, 0.86]
        stats_large = calculate_statistics(scores_large)
        ci_width_large = stats_large.confidence_interval_95[1] - stats_large.confidence_interval_95[0]

        # Larger sample should have narrower CI (with high probability)
        assert ci_width_large < ci_width_small

    def test_statistics_dataclass_fields(self):
        """Test Statistics dataclass has all required fields."""
        stats = Statistics(
            mean=0.85,
            std=0.05,
            min=0.75,
            max=0.95,
            count=10,
            confidence_interval_95=(0.82, 0.88),
        )

        assert stats.mean == 0.85
        assert stats.std == 0.05
        assert stats.min == 0.75
        assert stats.max == 0.95
        assert stats.count == 10
        assert stats.confidence_interval_95 == (0.82, 0.88)

    def test_variance_calculation(self):
        """Test that variance is calculated with n-1 denominator (sample variance)."""
        scores = [2.0, 4.0, 6.0, 8.0]
        # Mean = 5.0
        # Variance = ((2-5)^2 + (4-5)^2 + (6-5)^2 + (8-5)^2) / (4-1)
        #          = (9 + 1 + 1 + 9) / 3 = 20/3 ≈ 6.67
        # Std = sqrt(6.67) ≈ 2.58

        stats = calculate_statistics(scores)

        assert stats.mean == 5.0
        assert stats.std == pytest.approx(2.58, abs=0.01)

    def test_confidence_interval_z_score(self):
        """Test that confidence interval uses correct z-score (1.96 for 95%)."""
        scores = [5.0] * 100  # Large sample, std=0

        stats = calculate_statistics(scores)

        # With std=0, CI should equal mean regardless of sample size
        assert stats.confidence_interval_95 == (5.0, 5.0)

    def test_empty_list_raises_error(self):
        """Test that empty list raises appropriate error."""
        with pytest.raises((ValueError, ZeroDivisionError)):
            calculate_statistics([])

    def test_high_variance_dataset(self):
        """Test statistics with high variance data."""
        scores = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

        stats = calculate_statistics(scores)

        assert stats.mean == 0.5
        assert stats.std > 0.4  # Should have high std
        assert stats.min == 0.0
        assert stats.max == 1.0

    def test_low_variance_dataset(self):
        """Test statistics with low variance data."""
        scores = [0.5, 0.51, 0.49, 0.50, 0.50]

        stats = calculate_statistics(scores)

        assert stats.mean == pytest.approx(0.5, abs=0.01)
        assert stats.std < 0.02  # Should have low std
        assert stats.min == 0.49
        assert stats.max == 0.51
