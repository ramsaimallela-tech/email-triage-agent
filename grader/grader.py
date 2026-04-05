"""Evaluation utility for running multiple agent episodes."""

from __future__ import annotations
from typing import Any, Dict, List
from env.environment import EmailEnv

class Grader:
    def __init__(self, env: EmailEnv, agent: Any, num_episodes: int = 10) -> None:
        self.env = env
        self.agent = agent
        self.num_episodes = num_episodes

    def run(self) -> Dict[str, Any]:
        """Run requested episodes and return a summary report."""
        results: List[Dict[str, Any]] = []

        for i in range(self.num_episodes):
            # Vary seed per episode
            self.env.seed += i
            results.append(self._run_episode(i))

        return self._build_report(results)

    def _run_episode(self, episode_index: int) -> Dict[str, Any]:
        obs = self.env.reset()
        total_reward = 0.0
        step_count = 0
        hits = 0

        while True:
            action = self.agent.select_action(obs)
            obs, reward, done, info = self.env.step(action)
            
            total_reward += reward
            step_count += 1
            if info.get("classification_correct"):
                hits += 1

            if done:
                break

        score = total_reward / max(step_count, 1)
        acc = hits / max(step_count, 1)

        return {
            "episode": episode_index,
            "steps": step_count,
            "reward": round(total_reward, 4),
            "mean_score": round(score, 4),
            "accuracy": round(acc, 4),
            "success": score >= 0.5,
        }

    @staticmethod
    def _build_report(episodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        n = len(episodes)
        if n == 0:
            return {"aggregate": {}, "episodes": []}

        scores = [e["mean_score"] for e in episodes]
        accs = [e["accuracy"] for e in episodes]
        wins = [e["success"] for e in episodes]

        summary = {
            "num_episodes": n,
            "avg_score": round(sum(scores) / n, 4),
            "min_score": round(min(scores), 4),
            "max_score": round(max(scores), 4),
            "avg_accuracy": round(sum(accs) / n, 4),
            "success_rate": round(sum(wins) / n, 4),
        }

        return {
            "aggregate": summary,
            "episodes": episodes,
        }
