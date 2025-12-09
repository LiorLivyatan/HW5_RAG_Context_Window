"""
Ollama Interface - Building Block for LLM Queries

This module provides the OllamaInterface class for querying local Ollama LLM
with context and questions, measuring performance metrics.
"""

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import logging

try:
    import ollama
except ImportError:
    ollama = None

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Represents a response from the LLM."""

    text: str
    latency_ms: float
    tokens_used: Optional[int]
    model: str
    timestamp: datetime
    success: bool
    error: Optional[str] = None


class OllamaInterface:
    """
    Interface for querying Ollama LLM with performance monitoring.

    This building block provides a clean interface to query local Ollama,
    with automatic retry, latency tracking, and token counting.

    Input Data:
        - context: Context to provide to the LLM
        - question: Question to ask

    Output Data:
        - LLMResponse: Response with text, latency, tokens, metadata

    Setup Data:
        - base_url: Ollama API endpoint
        - model: Model name (e.g., "llama2")
        - temperature: Sampling temperature (0.0 = deterministic)
        - max_tokens: Maximum tokens to generate
        - timeout: Request timeout in seconds
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2",
        temperature: float = 0.0,
        max_tokens: int = 500,
        timeout: int = 60,
        max_retries: int = 3,
    ):
        """
        Initialize Ollama interface.

        Args:
            base_url: Ollama API endpoint URL
            model: Model name to use
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts on failure
        """
        if ollama is None:
            raise ImportError(
                "ollama package not installed. Install with: pip install ollama"
            )

        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

        # Validate connection at initialization
        if not self.check_availability():
            logger.warning(
                f"Ollama is not available at {base_url}. "
                "Please ensure Ollama is running: ollama serve"
            )

    def query(self, context: str, question: str) -> LLMResponse:
        """
        Query the LLM with context and question.

        Args:
            context: Context to provide
            question: Question to ask

        Returns:
            LLMResponse with text, latency, and metadata

        Raises:
            RuntimeError: If query fails after all retries
        """
        self._validate_inputs(context, question)

        # Build prompt
        prompt = self._build_prompt(context, question)

        # Query with retries
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                # Query Ollama
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    options={
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                )

                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000

                # Extract response text
                text = response.get("response", "").strip()

                # Count tokens (approximation if not provided)
                tokens_used = self._count_tokens(text)

                logger.info(
                    f"Query successful: {latency_ms:.2f}ms, {tokens_used} tokens"
                )

                return LLMResponse(
                    text=text,
                    latency_ms=latency_ms,
                    tokens_used=tokens_used,
                    model=self.model,
                    timestamp=datetime.now(),
                    success=True,
                )

            except Exception as e:
                logger.warning(f"Query attempt {attempt + 1} failed: {e}")

                if attempt == self.max_retries - 1:
                    # Final attempt failed
                    return LLMResponse(
                        text="",
                        latency_ms=0.0,
                        tokens_used=0,
                        model=self.model,
                        timestamp=datetime.now(),
                        success=False,
                        error=str(e),
                    )

                # Wait before retry (exponential backoff)
                time.sleep(2**attempt)

        # Should not reach here, but return error response
        return LLMResponse(
            text="",
            latency_ms=0.0,
            tokens_used=0,
            model=self.model,
            timestamp=datetime.now(),
            success=False,
            error="Max retries exceeded",
        )

    def check_availability(self) -> bool:
        """
        Check if Ollama is available and responding.

        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            # Try to list models as a health check
            ollama.list()
            return True
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False

    def _build_prompt(self, context: str, question: str) -> str:
        """
        Build prompt from context and question.

        Args:
            context: Context to provide
            question: Question to ask

        Returns:
            Formatted prompt
        """
        return f"""Context:
{context}

Question: {question}

Answer: """

    def _count_tokens(self, text: str) -> int:
        """
        Approximate token count for text.

        Uses simple heuristic: ~4 characters per token.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Simple approximation: 4 characters per token
        return len(text) // 4

    def _validate_inputs(self, context: str, question: str) -> None:
        """
        Validate query inputs.

        Args:
            context: Context string
            question: Question string

        Raises:
            ValueError: If inputs are invalid
        """
        if not isinstance(context, str):
            raise ValueError(f"context must be string, got {type(context)}")

        if not isinstance(question, str):
            raise ValueError(f"question must be string, got {type(question)}")

        if not question.strip():
            raise ValueError("question cannot be empty")

        # Context can be empty for some queries, so we don't validate it strictly

    def __repr__(self) -> str:
        """String representation of OllamaInterface."""
        return (
            f"OllamaInterface(base_url='{self.base_url}', "
            f"model='{self.model}', temperature={self.temperature})"
        )
