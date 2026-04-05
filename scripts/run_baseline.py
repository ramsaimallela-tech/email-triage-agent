"""CLI runner for evaluating the baseline agent across multiple tasks."""

from __future__ import annotations
import argparse
import json
import os
import sys

# Ensure project root is in the path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from env.environment import EmailEnv
from agents.baseline import BaselineAgent
from grader.grader import Grader
from tasks import ALL_CONFIGS

def main() -> None:
    parser = argparse.ArgumentParser(description="Email Triage Agent - Baseline Evaluator")
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=list(ALL_CONFIGS.keys()),
        choices=list(ALL_CONFIGS.keys()),
        help="Task difficulties to run (default: all)"
    )
    parser.add_argument("--episodes", type=int, default=10, help="Episodes per task")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", default="results/baseline_report.json", help="Export path")
    
    args = parser.parse_args()
    results_map: dict = {}

    for name in args.tasks:
        config = ALL_CONFIGS[name]
        env = EmailEnv(config, seed=args.seed)
        agent = BaselineAgent(seed=args.seed)
        grader = Grader(env, agent, num_episodes=args.episodes)

        print(f"\nEvaluating Task: {name.upper()} | {args.episodes} episodes")
        print("-" * 40)

        report = grader.run()
        res = report["aggregate"]
        results_map[name] = report

        print(f"  Score:    {res['avg_score']:.4f}")
        print(f"  Range:    [{res['min_score']:.4f}, {res['max_score']:.4f}]")
        print(f"  Accuracy: {res['avg_accuracy']:.1%}")
        print(f"  Success:  {res['success_rate']:.1%}")

    # Export results
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(args.output, "w") as f:
        json.dump(results_map, f, indent=2)
    
    print(f"\n[DONE] Report exported to: {args.output}")

if __name__ == "__main__":
    main()
