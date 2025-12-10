#!/usr/bin/env python3
"""
Test Experiment 1 with distractors to make it harder for the model.

This script compares accuracy with and without distractors.
"""

from pathlib import Path
from context_windows_lab.experiments import NeedleInHaystackExperiment, ExperimentConfig
from context_windows_lab.llm import OllamaInterface

def test_with_distractors():
    """Test Experiment 1 WITH distractors (harder)."""
    print("\n" + "="*70)
    print("EXPERIMENT 1 WITH DISTRACTORS (HARDER)")
    print("="*70 + "\n")

    config = ExperimentConfig(
        name="Needle in Haystack (With Distractors)",
        iterations=1,
        output_dir=Path("./results/experiment_1_distractors"),
        generate_visualizations=True,
    )

    # Create experiment WITH distractors
    experiment = NeedleInHaystackExperiment(
        config=config,
        num_documents=5,
        words_per_document=200,
        add_distractors=True,  # ENABLE DISTRACTORS
    )

    # Run experiment
    print("Running experiment with distractors...")
    experiment.run()

    # Show results
    analysis = experiment.analyze()
    print("\nRESULTS WITH DISTRACTORS:")
    for position in ["start", "middle", "end"]:
        acc = analysis[position]["accuracy"]["mean"]
        std = analysis[position]["accuracy"]["std"]
        print(f"  {position:>6}: Accuracy = {acc:.2%} ± {std:.2%}")


def test_without_distractors():
    """Test Experiment 1 WITHOUT distractors (baseline)."""
    print("\n" + "="*70)
    print("EXPERIMENT 1 WITHOUT DISTRACTORS (BASELINE)")
    print("="*70 + "\n")

    config = ExperimentConfig(
        name="Needle in Haystack (Baseline)",
        iterations=1,
        output_dir=Path("./results/experiment_1_baseline"),
        generate_visualizations=True,
    )

    # Create experiment WITHOUT distractors
    experiment = NeedleInHaystackExperiment(
        config=config,
        num_documents=5,
        words_per_document=200,
        add_distractors=False,  # NO DISTRACTORS
    )

    # Run experiment
    print("Running baseline experiment...")
    experiment.run()

    # Show results
    analysis = experiment.analyze()
    print("\nRESULTS WITHOUT DISTRACTORS:")
    for position in ["start", "middle", "end"]:
        acc = analysis[position]["accuracy"]["mean"]
        std = analysis[position]["accuracy"]["std"]
        print(f"  {position:>6}: Accuracy = {acc:.2%} ± {std:.2%}")


def test_with_weaker_model(model_name="tinyllama"):
    """Test Experiment 1 with a weaker model."""
    print("\n" + "="*70)
    print(f"EXPERIMENT 1 WITH WEAKER MODEL ({model_name})")
    print("="*70 + "\n")

    # Check if model exists
    import subprocess
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if model_name not in result.stdout:
        print(f"Model '{model_name}' not found. Pulling...")
        print(f"Run: ollama pull {model_name}")
        print("Then re-run this script.\n")
        return

    config = ExperimentConfig(
        name=f"Needle in Haystack ({model_name})",
        iterations=1,
        output_dir=Path(f"./results/experiment_1_{model_name}"),
        generate_visualizations=True,
    )

    # Create LLM interface with weaker model
    llm = OllamaInterface(model=model_name)

    # Create experiment with distractors AND weaker model
    experiment = NeedleInHaystackExperiment(
        config=config,
        num_documents=5,
        words_per_document=200,
        add_distractors=True,  # ENABLE DISTRACTORS
        llm_interface=llm,  # USE WEAKER MODEL
    )

    # Run experiment
    print(f"Running experiment with {model_name}...")
    experiment.run()

    # Show results
    analysis = experiment.analyze()
    print(f"\nRESULTS WITH {model_name.upper()}:")
    for position in ["start", "middle", "end"]:
        acc = analysis[position]["accuracy"]["mean"]
        std = analysis[position]["accuracy"]["std"]
        print(f"  {position:>6}: Accuracy = {acc:.2%} ± {std:.2%}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING EXPERIMENT 1 - MAKING IT HARDER FOR THE MODEL")
    print("="*70)

    # Test 1: Baseline (no distractors)
    test_without_distractors()

    # Test 2: With distractors
    test_with_distractors()

    # Test 3: With weaker model (if available)
    test_with_weaker_model("tinyllama")

    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70 + "\n")
