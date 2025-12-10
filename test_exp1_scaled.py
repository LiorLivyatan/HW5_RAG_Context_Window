#!/usr/bin/env python3
"""
Experiment 1 - Scaled Version: Demonstrate "Lost in the Middle" Phenomenon

This script runs Experiment 1 with MUCH larger scale:
- 50 documents per position (vs original 5)
- 500 words per document (vs original 200)
- Distractors enabled
- Weaker model (tinyllama)

Expected: Finally see accuracy drop in middle position!
"""

from pathlib import Path
from context_windows_lab.experiments import NeedleInHaystackExperiment, ExperimentConfig
from context_windows_lab.llm import OllamaInterface

def run_scaled_experiment():
    """Run Experiment 1 with massive scale to demonstrate Lost in the Middle."""

    print("\n" + "="*80)
    print("EXPERIMENT 1 - SCALED VERSION")
    print("Demonstrating 'Lost in the Middle' Phenomenon")
    print("="*80)

    print("\nConfiguration:")
    print("  - Documents per position: 50 (vs original 5)")
    print("  - Words per document: 500 (vs original 200)")
    print("  - Total context size: ~25,000 words per position")
    print("  - Distractors: ENABLED (confusing CEO names, roles)")
    print("  - Model: tinyllama (1.1B parameters - much weaker than llama2)")
    print("  - Iterations: 1 (50 docs × 3 positions = 150 queries)")
    print()

    # Create configuration
    config = ExperimentConfig(
        name="Needle in Haystack (Scaled - 50 docs)",
        iterations=1,  # 1 iteration = 150 queries total
        output_dir=Path("./results/experiment_1_scaled"),
        generate_visualizations=True,
    )

    # Create LLM interface with tinyllama
    print("Initializing tinyllama (1.1B)...")
    llm = OllamaInterface(model="tinyllama")

    # Create experiment with MASSIVE SCALE
    print("Creating scaled experiment...")
    experiment = NeedleInHaystackExperiment(
        config=config,
        num_documents=50,  # 10x larger!
        words_per_document=500,  # 2.5x larger!
        add_distractors=True,  # Confusing information
        llm_interface=llm,
    )

    print("\n" + "-"*80)
    print("RUNNING EXPERIMENT...")
    print("This will take ~10-15 minutes (150 queries with tinyllama)")
    print("-"*80 + "\n")

    # Run experiment
    experiment.run()

    # Show results
    analysis = experiment.analyze()

    print("\n" + "="*80)
    print("RESULTS - SCALED EXPERIMENT")
    print("="*80 + "\n")

    for position in ["start", "middle", "end"]:
        acc = analysis[position]["accuracy"]["mean"]
        std = analysis[position]["accuracy"]["std"]
        count = analysis[position]["accuracy"]["count"]
        lat = analysis[position]["latency_ms"]["mean"]

        print(f"{position.upper():>8} Position:")
        print(f"  Accuracy: {acc:.2%} ± {std:.2%} ({count} documents)")
        print(f"  Latency:  {lat/1000:.2f}s average")
        print()

    # Calculate and display the "Lost in the Middle" effect
    start_acc = analysis["start"]["accuracy"]["mean"]
    middle_acc = analysis["middle"]["accuracy"]["mean"]
    end_acc = analysis["end"]["accuracy"]["mean"]

    middle_drop = ((start_acc + end_acc) / 2) - middle_acc

    print("="*80)
    print("LOST IN THE MIDDLE EFFECT")
    print("="*80)
    print(f"Average of Start & End: {(start_acc + end_acc) / 2:.2%}")
    print(f"Middle Position:        {middle_acc:.2%}")
    print(f"Drop in Middle:         {middle_drop:.2%}")

    if middle_drop > 0.05:  # More than 5% drop
        print("\n✅ SUCCESS! 'Lost in the Middle' phenomenon DEMONSTRATED!")
        print("   Middle position shows significantly lower accuracy.")
    elif middle_drop > 0.02:  # 2-5% drop
        print("\n⚠️  PARTIAL: Some accuracy drop in middle, but not dramatic.")
        print("   May need even more documents or harder distractors.")
    else:
        print("\n❌ NOT OBSERVED: Middle accuracy is not significantly lower.")
        print("   Task may still be too easy for tinyllama.")

    print("\n" + "="*80)
    print(f"Results saved to: {config.output_dir}")
    print(f"Visualization: {config.output_dir / 'accuracy_by_position.png'}")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("CONTEXT WINDOWS LAB - SCALED EXPERIMENT 1")
    print("Testing 'Lost in the Middle' with 50 documents + distractors + tinyllama")
    print("="*80)

    run_scaled_experiment()

    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE")
    print("="*80 + "\n")
