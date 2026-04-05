"""OpenEnv-compatible email triage environment."""

from __future__ import annotations
import random
from typing import Optional, Tuple, Dict, Any
from env.models import Action, Email, Observation, StepResult, TaskConfig

class EmailEnv:
    def __init__(self, config: TaskConfig, seed: int = 42) -> None:
        self.config = config
        self.seed = seed
        self._rng = random.Random(seed)

        self._step = 0
        self._done = False
        self._queue: list[Email] = []
        self._total_reward = 0.0
        self._correct_count = 0

    def reset(self) -> Observation:
        self._rng = random.Random(self.seed)
        self._step = 0
        self._done = False
        self._total_reward = 0.0
        self._correct_count = 0

        pool = list(self.config.emails)
        self._rng.shuffle(pool)
        self._queue = pool[:self.config.max_steps]

        return self._make_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self._done:
            raise RuntimeError("Episode finished. Call reset() to start a new one.")

        email = self._queue[self._step]
        reward, step_info = self._calculate_reward(email, action)

        self._total_reward += reward
        self._step += 1

        if self._step >= len(self._queue):
            self._done = True

        obs = self._make_observation() if not self._done else self._make_terminal_observation()
        return obs, reward, self._done, step_info

    def get_state(self) -> dict:
        return {
            "step": self._step,
            "done": self._done,
            "total_reward": round(self._total_reward, 4),
            "accuracy": round(self._correct_count / max(self._step, 1), 4),
            "progress": f"{self._step}/{len(self._queue)}"
        }

    def _make_observation(self) -> Observation:
        email = self._queue[min(self._step, len(self._queue) - 1)]
        return Observation(
            timestep=self._step,
            email=email,
            emails_remaining=len(self._queue) - self._step,
            accuracy_so_far=round(self._correct_count / max(self._step, 1), 4),
        )

    def _make_terminal_observation(self) -> Observation:
        return Observation(
            timestep=self._step,
            email=self._queue[-1],
            emails_remaining=0,
            accuracy_so_far=round(self._correct_count / max(self._step, 1), 4),
        )

    def _calculate_reward(self, email: Email, action: Action) -> Tuple[float, Dict[str, Any]]:
        metrics: Dict[str, Any] = {}

        # 1. Classification
        is_correct = action.category.lower() == email.true_category.lower()
        cls_score = 1.0 if is_correct else 0.0
        if is_correct:
            self._correct_count += 1
        metrics["classification_correct"] = is_correct

        # 2. Reply Relevancy (Keyword match)
        reply_txt = action.reply.lower()
        if email.expected_reply_keywords:
            hits = sum(1 for kw in email.expected_reply_keywords if kw.lower() in reply_txt)
            rel_score = hits / len(email.expected_reply_keywords)
        else:
            # Partial credit for engagement if no specific keywords are expected
            rel_score = min(len(action.reply) / 50.0, 1.0) if action.reply else 0.0
        metrics["reply_score"] = round(rel_score, 4)

        # 3. Priority Alignment
        p_dist = abs(action.priority - email.true_priority)
        p_score = max(0.0, 1.0 - p_dist * 0.25)
        metrics["priority_score"] = round(p_score, 4)

        # 4. Length Efficiency
        body_len = len(action.reply)
        if 10 <= body_len <= 200:
            eff_score = 1.0
        elif body_len > 200:
            eff_score = max(0.0, 1.0 - (body_len - 200) / 300.0)
        else:
            eff_score = body_len / 10.0
        metrics["efficiency_score"] = round(eff_score, 4)

        # Apply weights from config
        cfg = self.config
        step_reward = (
            cfg.classification_weight * cls_score +
            cfg.reply_weight * rel_score +
            cfg.priority_weight * p_score +
            cfg.efficiency_weight * eff_score
        )
        
        final_reward = round(min(max(step_reward, 0.0), 1.0), 4)
        metrics["breakdown"] = {
            "cls": round(cfg.classification_weight * cls_score, 4),
            "reply": round(cfg.reply_weight * rel_score, 4),
            "priority": round(cfg.priority_weight * p_score, 4),
            "eff": round(cfg.efficiency_weight * eff_score, 4),
        }

        return final_reward, metrics
