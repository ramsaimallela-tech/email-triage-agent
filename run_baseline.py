"""CLI runner: evaluates all tasks and saves a JSON report."""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.environment import EmailEnv
from agents.baseline import BaselineAgent
from grader.grader   import Grader
from tasks           import ALL_CONFIGS

def main():
    parser = argparse.ArgumentParser(description="Run baseline agent evaluation")
    parser.add_argument("--tasks",    nargs="+", default=["easy", "medium", "hard"])
    parser.add_argument("--episodes", type=int,  default=10)
    parser.add_argument("--seed",     type=int,  default=42)
    parser.add_argument("--output",   default="results/baseline_report.json")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    report = {}

    for task in args.tasks:
        config  = ALL_CONFIGS[task]
        env     = EmailEnv(config, seed=args.seed)
        agent   = BaselineAgent(seed=args.seed)
        grader  = Grader(env, agent, num_episodes=args.episodes)
        result  = grader.run()
        agg     = result["aggregate"]

        print("=" * 60)
        print(f"  Task: {task.upper()} | Episodes: {args.episodes} | Seed: {args.seed}")
        print("=" * 60)
        print(f"  Mean Reward:       {agg['mean_reward']:.4f}")
        print(f"  Min / Max Reward:  {agg['min_reward']:.4f} / {agg['max_reward']:.4f}")
        print(f"  Classification:    {agg['classification']}%")
        print(f"  Success Rate:      {agg['success_rate']}%")
        print()
        report[task] = result

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[OK] Full report saved to {args.output}")

if __name__ == "__main__":
    main()
