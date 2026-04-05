"""Grader — N-episode evaluation producing a JSON report.

Usage:
    grader = Grader(env, agent, num_episodes=10)
    report = grader.run()
"""

from __future__ import annotations

from typing import Any, Dict, List

from env.environment import EmailEnv
from env.models import TaskConfig


class Grader:
    """Evaluate an agent over multiple episodes and produce a grading report."""

    def __init__(self, env: EmailEnv, agent: Any, num_episodes: int = 10) -> None:
        self.env = env
        self.agent = agent
        self.num_episodes = num_episodes

    def run(self) -> Dict[str, Any]:
        """Run N episodes and return aggregate + per-episode report."""
        episode_results: List[Dict[str, Any]] = []

        for ep in range(self.num_episodes):
            # Vary seed per episode for diversity
            self.env.seed = self.env.seed + ep
            result = self._run_episode(ep)
            episode_results.append(result)

        return self._build_report(episode_results)

    # ── Internal ─────────────────────────────────────────────────────────

    def _run_episode(self, episode_id: int) -> Dict[str, Any]:
        """Run a single episode and return metrics."""
        obs = self.env.reset()
        total_reward = 0.0
        steps = 0
        classifications_correct = 0

        while True:
            action = self.agent.select_action(obs)
            obs, reward, done, info = self.env.step(action)
            total_reward += reward
            steps += 1

            if info.get("classification_correct"):
                classifications_correct += 1

            if done:
                break

        mean_reward = total_reward / max(steps, 1)
        accuracy = classifications_correct / max(steps, 1)

        return {
            "episode": episode_id,
            "steps": steps,
            "total_reward": round(total_reward, 4),
            "mean_reward": round(mean_reward, 4),
            "classification_accuracy": round(accuracy, 4),
            "success": mean_reward >= 0.5,
        }

    @staticmethod
    def _build_report(episodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate per-episode results into a summary report."""
        n = len(episodes)
        if n == 0:
            return {"aggregate": {}, "episodes": []}

        total_rewards = [e["mean_reward"] for e in episodes]
        accuracies = [e["classification_accuracy"] for e in episodes]
        successes = [e["success"] for e in episodes]

        aggregate = {
            "num_episodes": n,
            "mean_reward": round(sum(total_rewards) / n, 4),
            "min_reward": round(min(total_rewards), 4),
            "max_reward": round(max(total_rewards), 4),
            "mean_classification_accuracy": round(sum(accuracies) / n, 4),
            "success_rate": round(sum(successes) / n, 4),
        }

        return {
            "aggregate": aggregate,
            "episodes": episodes,
        }
