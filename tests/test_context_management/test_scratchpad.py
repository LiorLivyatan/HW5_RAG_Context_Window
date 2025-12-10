"""
Tests for Scratchpad external memory component.
"""

import pytest

from context_windows_lab.context_management.scratchpad import Scratchpad


class TestScratchpad:
    """Test suite for Scratchpad class."""

    def test_initialization(self):
        """Test scratchpad initializes empty."""
        scratchpad = Scratchpad()
        assert len(scratchpad) == 0
        assert scratchpad.read_all() == {}
        assert "empty" in scratchpad.get_summary().lower()

    def test_write_single_entry(self):
        """Test writing a single entry."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")

        assert len(scratchpad) == 1
        assert scratchpad.read("key1") == "value1"
        assert "key1" in scratchpad.get_summary()

    def test_write_multiple_entries(self):
        """Test writing multiple entries."""
        scratchpad = Scratchpad()
        scratchpad.write("budget", "$2.5M")
        scratchpad.write("deadline", "March 15")
        scratchpad.write("team_size", "15 engineers")

        assert len(scratchpad) == 3
        assert scratchpad.read("budget") == "$2.5M"
        assert scratchpad.read("deadline") == "March 15"
        assert scratchpad.read("team_size") == "15 engineers"

    def test_overwrite_existing_key(self):
        """Test overwriting an existing key updates the value."""
        scratchpad = Scratchpad()
        scratchpad.write("counter", "1")
        scratchpad.write("counter", "2")

        assert len(scratchpad) == 1  # Still only one entry
        assert scratchpad.read("counter") == "2"  # Updated value

    def test_read_nonexistent_key(self):
        """Test reading a key that doesn't exist returns None."""
        scratchpad = Scratchpad()
        result = scratchpad.read("nonexistent")
        assert result is None

    def test_read_all(self):
        """Test reading all entries at once."""
        scratchpad = Scratchpad()
        scratchpad.write("a", "1")
        scratchpad.write("b", "2")
        scratchpad.write("c", "3")

        all_entries = scratchpad.read_all()
        assert len(all_entries) == 3
        assert all_entries == {"a": "1", "b": "2", "c": "3"}

    def test_read_all_returns_copy(self):
        """Test that read_all returns a copy, not reference."""
        scratchpad = Scratchpad()
        scratchpad.write("key", "value")

        entries1 = scratchpad.read_all()
        entries1["key"] = "modified"

        # Original should be unchanged
        assert scratchpad.read("key") == "value"

    def test_clear(self):
        """Test clearing all entries."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")
        scratchpad.write("key2", "value2")

        assert len(scratchpad) == 2

        scratchpad.clear()

        assert len(scratchpad) == 0
        assert scratchpad.read("key1") is None
        assert scratchpad.read("key2") is None
        assert "empty" in scratchpad.get_summary().lower()

    def test_get_summary_empty(self):
        """Test summary with empty scratchpad."""
        scratchpad = Scratchpad()
        summary = scratchpad.get_summary()

        assert "empty" in summary.lower()

    def test_get_summary_with_entries(self):
        """Test summary includes all entries."""
        scratchpad = Scratchpad()
        scratchpad.write("fact1", "The budget is $2.5M")
        scratchpad.write("fact2", "The deadline is March 15")

        summary = scratchpad.get_summary()

        assert "fact1" in summary
        assert "fact2" in summary
        assert "$2.5M" in summary
        assert "March 15" in summary
        assert "Scratchpad Memory:" in summary

    def test_history_tracking_write(self):
        """Test that write operations are tracked in history."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")

        assert len(scratchpad.history) >= 1
        assert "WRITE" in scratchpad.history[0]
        assert "key1" in scratchpad.history[0]

    def test_history_tracking_read(self):
        """Test that read operations are tracked in history."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")
        initial_history_len = len(scratchpad.history)

        scratchpad.read("key1")

        assert len(scratchpad.history) > initial_history_len
        assert any("READ" in entry for entry in scratchpad.history)

    def test_history_tracking_clear(self):
        """Test that clear operations are tracked in history."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")
        scratchpad.clear()

        assert any("CLEAR" in entry for entry in scratchpad.history)

    def test_repr(self):
        """Test string representation."""
        scratchpad = Scratchpad()
        scratchpad.write("key1", "value1")
        scratchpad.write("key2", "value2")

        repr_str = repr(scratchpad)
        assert "Scratchpad" in repr_str
        assert "2" in repr_str  # Number of entries

    def test_len(self):
        """Test len() function."""
        scratchpad = Scratchpad()
        assert len(scratchpad) == 0

        scratchpad.write("key1", "value1")
        assert len(scratchpad) == 1

        scratchpad.write("key2", "value2")
        assert len(scratchpad) == 2

        scratchpad.clear()
        assert len(scratchpad) == 0

    def test_large_value_storage(self):
        """Test storing large values."""
        scratchpad = Scratchpad()
        large_text = "Lorem ipsum " * 1000  # ~12KB of text

        scratchpad.write("large_doc", large_text)

        assert scratchpad.read("large_doc") == large_text
        assert len(scratchpad) == 1

    def test_special_characters_in_values(self):
        """Test storing values with special characters."""
        scratchpad = Scratchpad()
        special_value = "Value with\nnewlines\tand\ttabs and 中文字符"

        scratchpad.write("special", special_value)

        assert scratchpad.read("special") == special_value

    def test_empty_string_value(self):
        """Test storing empty string values."""
        scratchpad = Scratchpad()
        scratchpad.write("empty", "")

        assert scratchpad.read("empty") == ""
        assert len(scratchpad) == 1  # Entry exists even if empty

    def test_numeric_keys_as_strings(self):
        """Test using numeric strings as keys."""
        scratchpad = Scratchpad()
        scratchpad.write("123", "numeric key")

        assert scratchpad.read("123") == "numeric key"

    def test_use_case_multi_step_facts(self):
        """Test realistic use case: storing facts from multiple steps."""
        scratchpad = Scratchpad()

        # Simulate multi-step agent interaction
        steps = [
            ("step_1", "The project budget is $2.5 million for Q1 2025."),
            ("step_2", "The team consists of 15 engineers and 3 designers."),
            ("step_3", "The launch date is scheduled for March 15th, 2025."),
        ]

        for key, fact in steps:
            scratchpad.write(key, fact)

        # Verify all facts are stored
        assert len(scratchpad) == 3

        # Verify retrieval
        assert "$2.5 million" in scratchpad.read("step_1")
        assert "15 engineers" in scratchpad.read("step_2")
        assert "March 15th" in scratchpad.read("step_3")

        # Verify summary includes all
        summary = scratchpad.get_summary()
        for key, fact in steps:
            assert key in summary
            assert fact in summary
