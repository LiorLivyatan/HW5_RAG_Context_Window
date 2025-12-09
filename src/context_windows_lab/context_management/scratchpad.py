"""
Scratchpad for External Memory

Provides external memory storage for the WRITE strategy in Experiment 4.
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Scratchpad:
    """
    External memory scratchpad for storing key information.

    Allows writing and retrieving important facts outside the context window.
    """

    def __init__(self):
        """Initialize empty scratchpad."""
        self.memory: Dict[str, str] = {}
        self.history: List[str] = []

    def write(self, key: str, value: str) -> None:
        """
        Write information to scratchpad.

        Args:
            key: Memory key
            value: Information to store
        """
        self.memory[key] = value
        self.history.append(f"WRITE: {key} = {value}")
        logger.debug(f"Wrote to scratchpad: {key} = {value}")

    def read(self, key: str) -> Optional[str]:
        """
        Read information from scratchpad.

        Args:
            key: Memory key

        Returns:
            Stored value or None if not found
        """
        value = self.memory.get(key)
        if value:
            self.history.append(f"READ: {key} = {value}")
            logger.debug(f"Read from scratchpad: {key} = {value}")
        return value

    def read_all(self) -> Dict[str, str]:
        """
        Read all stored information.

        Returns:
            All memory entries
        """
        return self.memory.copy()

    def clear(self) -> None:
        """Clear all stored information."""
        self.memory.clear()
        self.history.append("CLEAR: All memory cleared")
        logger.debug("Cleared scratchpad")

    def get_summary(self) -> str:
        """
        Get summary of stored information.

        Returns:
            Formatted string of all stored data
        """
        if not self.memory:
            return "Scratchpad is empty."

        lines = ["Scratchpad Memory:"]
        for key, value in self.memory.items():
            lines.append(f"  - {key}: {value}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """String representation."""
        return f"Scratchpad(entries={len(self.memory)})"

    def __len__(self) -> int:
        """Number of entries."""
        return len(self.memory)
