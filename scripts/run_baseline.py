"""CLI runner — evaluate the baseline agent across all tasks.

Usage:
    python scripts/run_baseline.py
    python scripts/run_baseline.py --tasks easy medium
    python scripts/run_baseline.py --episodes 20 --seed 7
    python scripts/run_baseline.py --output results/my_report.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Ensure project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from env.environment import EmailEnv
from agents.baseline import BaselineAgent
from grader.grader import Grader
from tasks import ALL_CONFIGS


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate the baseline email triage agent."
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=list(ALL_CONFIGS.keys()),
        choices=list(ALL_CONFIGS.keys()),
        help="Task difficulties to evaluate (default: all).",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes per task (default: 10).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/baseline_report.json",
        help="Path to save the JSON report.",
    )
    args = parser.parse_args()

    full_report: dict = {}

    for task_name in args.tasks:
        config = ALL_CONFIGS[task_name]
        env = EmailEnv(config, seed=args.seed)
        agent = BaselineAgent(seed=args.seed)
        grader = Grader(env, agent, num_episodes=args.episodes)

        print(f"\n{'='*60}")
        print(f"  Task: {task_name.upper()} | Episodes: {args.episodes} | Seed: {args.seed}")
        print(f"{'='*60}")

        report = grader.run()
        agg = report["aggregate"]
        full_report[task_name] = report

        print(f"  Mean Reward:       {agg['mean_reward']:.4f}")
        print(f"  Min / Max Reward:  {agg['min_reward']:.4f} / {agg['max_reward']:.4f}")
        print(f"  Classification:    {agg['mean_classification_accuracy']:.1%}")
        print(f"  Success Rate:      {agg['success_rate']:.1%}")

    # Save report
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(full_report, f, indent=2)
    print(f"\n[OK] Full report saved to {args.output}")


if __name__ == "__main__":
    main()
