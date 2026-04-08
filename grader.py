"""Grader: N-episode batch evaluator."""
import json
from typing import Dict, Any

class Grader:
    def __init__(self, env, agent, num_episodes: int = 10):
        self.env          = env
        self.agent        = agent
        self.num_episodes = num_episodes

    def run(self) -> Dict[str, Any]:
        all_rewards   = []
        all_correct   = []
        episode_data  = []

        for ep in range(self.num_episodes):
            obs     = self.env.reset()
            done    = False
            rewards = []
            correct = 0
            steps   = 0

            while not done:
                action = self.agent.select_action(obs)
                obs, reward, done, info = self.env.step(action)
                rewards.append(reward)
                if info.get("correct"):
                    correct += 1
                steps += 1

            ep_mean = sum(rewards) / max(len(rewards), 1)
            ep_acc  = correct / max(steps, 1)
            all_rewards.append(ep_mean)
            all_correct.append(ep_acc)
            episode_data.append({"episode": ep + 1, "mean_reward": round(ep_mean, 4), "accuracy": round(ep_acc, 4)})

        aggregate = {
            "mean_reward":    round(sum(all_rewards) / len(all_rewards), 4),
            "min_reward":     round(min(all_rewards), 4),
            "max_reward":     round(max(all_rewards), 4),
            "classification": round(sum(all_correct) / len(all_correct) * 100, 2),
            "success_rate":   round(sum(1 for r in all_rewards if r >= 0.5) / len(all_rewards) * 100, 2),
        }
        return {"aggregate": aggregate, "episodes": episode_data}
