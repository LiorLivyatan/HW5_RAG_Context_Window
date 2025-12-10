"""
Command-Line Interface for Context Windows Lab

Provides CLI for running experiments and managing the system.
"""

import argparse
import logging
import sys
from pathlib import Path

from context_windows_lab.experiments.base_experiment import ExperimentConfig
from context_windows_lab.experiments.exp1_needle_haystack import (
    NeedleInHaystackExperiment,
)
from context_windows_lab.experiments.exp3_rag_impact import RAGImpactExperiment
from context_windows_lab.llm.ollama_interface import OllamaInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def setup_parser() -> argparse.ArgumentParser:
    """
    Set up command-line argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Context Windows Lab - LLM Context Management Experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--experiment",
        "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run specific experiment (1-4)",
    )

    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all experiments sequentially",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("./results"),
        help="Output directory for results (default: ./results)",
    )

    parser.add_argument(
        "--iterations",
        "-i",
        type=int,
        default=3,
        help="Number of iterations per experiment (default: 3)",
    )

    parser.add_argument(
        "--check-ollama",
        action="store_true",
        help="Check if Ollama is available and exit",
    )

    parser.add_argument(
        "--multiprocessing",
        "-mp",
        action="store_true",
        help="Enable multiprocessing for parallel iterations (faster)",
    )

    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=None,
        help="Number of worker processes (default: CPU count)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser


def check_ollama_availability() -> bool:
    """
    Check if Ollama is available.

    Returns:
        True if available, False otherwise
    """
    try:
        llm = OllamaInterface()
        available = llm.check_availability()

        if available:
            logger.info("✓ Ollama is available and responding")
            return True
        else:
            logger.error(
                "✗ Ollama is not responding. "
                "Please ensure Ollama is running:\n"
                "  1. Start Ollama: ollama serve\n"
                "  2. Pull model: ollama pull llama2"
            )
            return False
    except Exception as e:
        logger.error(f"✗ Error checking Ollama: {e}")
        return False


def run_experiment_1(
    output_dir: Path, iterations: int, use_multiprocessing: bool = False, max_workers: int = None
) -> bool:
    """
    Run Experiment 1: Needle in Haystack.

    Args:
        output_dir: Output directory
        iterations: Number of iterations
        use_multiprocessing: Enable multiprocessing for parallel iterations
        max_workers: Number of worker processes (default: CPU count)

    Returns:
        True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("EXPERIMENT 1: Needle in Haystack (Lost in the Middle)")
    logger.info("=" * 60)

    exp_output = output_dir / "experiment_1"

    config = ExperimentConfig(
        name="Needle in Haystack",
        output_dir=exp_output,
        iterations=iterations,
        save_results=True,
        generate_visualizations=True,
        use_multiprocessing=use_multiprocessing,
        max_workers=max_workers,
    )

    experiment = NeedleInHaystackExperiment(config=config)

    results = experiment.run()

    if results.success:
        logger.info("✓ Experiment 1 completed successfully")
        logger.info(f"  Results saved to: {exp_output}")
        logger.info(f"  Visualizations: {len(results.visualization_paths)}")
        return True
    else:
        logger.error(f"✗ Experiment 1 failed: {results.error}")
        return False


def run_experiment_2(
    output_dir: Path,
    iterations: int = 1,
    use_multiprocessing: bool = False,
    max_workers: int = None,
) -> bool:
    """
    Run Experiment 2: Context Size Impact.

    Args:
        output_dir: Output directory for results
        iterations: Number of iterations (default: 1 for quick test)

    Returns:
        True if successful, False otherwise
    """
    from context_windows_lab.experiments import ContextSizeExperiment, ExperimentConfig

    logger.info("=" * 60)
    logger.info("EXPERIMENT 2: Context Size Impact")
    logger.info("=" * 60)

    exp_output = output_dir / "experiment_2"
    exp_output.mkdir(parents=True, exist_ok=True)

    config = ExperimentConfig(
        name="Context Size Impact",
        iterations=iterations,
        output_dir=exp_output,
        save_results=True,
        generate_visualizations=True,
        use_multiprocessing=use_multiprocessing,
        max_workers=max_workers,
    )

    # Create experiment with document counts: 2, 5, 10, 20, 50
    # Tests how accuracy degrades as context window size increases
    experiment = ContextSizeExperiment(
        config=config,
        document_counts=[2, 5, 10, 20, 50],  # Test different context sizes
        words_per_document=200,
    )

    results = experiment.run()

    if results.success:
        logger.info("✓ Experiment 2 completed successfully")
        logger.info(f"  Results saved to: {exp_output}")
        logger.info(f"  Visualizations: {len(results.visualization_paths)}")
        return True
    else:
        logger.error(f"✗ Experiment 2 failed: {results.error}")
        return False


def run_experiment_3(
    output_dir: Path,
    iterations: int = 1,
    use_multiprocessing: bool = False,
    max_workers: int = None,
) -> bool:
    """
    Run Experiment 3: RAG Impact.

    Args:
        output_dir: Output directory for results
        iterations: Number of iterations (default: 1)
        use_multiprocessing: Enable multiprocessing for parallel iterations
        max_workers: Number of worker processes (default: CPU count)

    Returns:
        True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("EXPERIMENT 3: RAG Impact - Full Context vs RAG")
    logger.info("=" * 60)

    exp_output = output_dir / "experiment_3"
    exp_output.mkdir(parents=True, exist_ok=True)

    config = ExperimentConfig(
        name="RAG Impact",
        iterations=iterations,
        output_dir=exp_output,
        save_results=True,
        generate_visualizations=True,
        use_multiprocessing=use_multiprocessing,
        max_workers=max_workers,
    )

    # Create experiment with Hebrew documents, top-3 retrieval
    # Uses default path: data/raw/hebrew_documents/
    # Question in English (llama2 cannot handle Hebrew questions properly)
    # Note: Assignment specified Hebrew, but llama2 limitation requires English question
    experiment = RAGImpactExperiment(
        config=config,
        domain="medicine",  # Focus on medicine domain for medicine-related question
        question="What are the main benefits or applications of the technology described?",  # English question
        expected_answer="benefits",  # Expected keyword in response
        top_k=3,
    )

    results = experiment.run()

    if results.success:
        logger.info("✓ Experiment 3 completed successfully")
        logger.info(f"  Results saved to: {exp_output}")
        logger.info(f"  Visualizations: {len(results.visualization_paths)}")
        return True
    else:
        logger.error(f"✗ Experiment 3 failed: {results.error}")
        return False


def run_experiment_4(
    output_dir: Path,
    iterations: int = 1,
    use_multiprocessing: bool = False,
    max_workers: int = None,
) -> bool:
    """
    Run Experiment 4: Context Engineering Strategies.

    Args:
        output_dir: Output directory for results
        iterations: Number of iterations (default: 1)
        use_multiprocessing: Enable multiprocessing for parallel iterations
        max_workers: Number of worker processes (default: CPU count)

    Returns:
        True if successful, False otherwise
    """
    from context_windows_lab.experiments import ContextStrategiesExperiment

    logger.info("=" * 60)
    logger.info("EXPERIMENT 4: Context Engineering Strategies")
    logger.info("=" * 60)

    exp_output = output_dir / "experiment_4"
    exp_output.mkdir(parents=True, exist_ok=True)

    config = ExperimentConfig(
        name="Context Strategies",
        iterations=iterations,
        output_dir=exp_output,
        save_results=True,
        generate_visualizations=True,
        use_multiprocessing=use_multiprocessing,
        max_workers=max_workers,
    )

    # Create experiment with 20 documents, 10 steps
    # Tests SELECT (RAG), COMPRESS (summarization), WRITE (scratchpad)
    # Uses k=5 for SELECT strategy (matches assignment pseudocode)
    experiment = ContextStrategiesExperiment(
        config=config,
        num_documents=20,
        words_per_document=200,
        num_steps=10,  # Multi-step agent simulation
        top_k=5,  # Assignment requires k=5 for SELECT strategy
        max_summary_words=200,
    )

    results = experiment.run()

    if results.success:
        logger.info("✓ Experiment 4 completed successfully")
        logger.info(f"  Results saved to: {exp_output}")
        logger.info(f"  Visualizations: {len(results.visualization_paths)}")
        return True
    else:
        logger.error(f"✗ Experiment 4 failed: {results.error}")
        return False


def main():
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Context Windows Lab - Starting...")

    # Check Ollama availability
    if args.check_ollama:
        sys.exit(0 if check_ollama_availability() else 1)

    # Verify Ollama is available before running experiments
    if not check_ollama_availability():
        logger.error("Cannot proceed without Ollama. Exiting.")
        sys.exit(1)

    # Run experiments
    success = True

    if args.experiment == 1 or args.run_all:
        success = (
            run_experiment_1(args.output_dir, args.iterations, args.multiprocessing, args.workers)
            and success
        )

    if args.experiment == 2 or args.run_all:
        success = (
            run_experiment_2(args.output_dir, args.iterations, args.multiprocessing, args.workers)
            and success
        )

    if args.experiment == 3 or args.run_all:
        success = (
            run_experiment_3(args.output_dir, args.iterations, args.multiprocessing, args.workers)
            and success
        )

    if args.experiment == 4 or args.run_all:
        success = (
            run_experiment_4(args.output_dir, args.iterations, args.multiprocessing, args.workers)
            and success
        )

    if not args.experiment and not args.run_all:
        parser.print_help()
        logger.info("\nUse --experiment N or --run-all to run experiments")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
