"""EmailEnv — OpenEnv-compatible email triage environment.

Implements reset / step / get_state with shaped reward.
"""

from __future__ import annotations

import random
from typing import Optional, Tuple, Dict, Any

from env.models import Action, Email, Observation, StepResult, TaskConfig


class EmailEnv:
    """Simulates an email triage queue that an agent must classify and reply to."""

    def __init__(self, config: TaskConfig, seed: int = 42) -> None:
        self.config = config
        self.seed = seed
        self._rng = random.Random(seed)

        # Episode state
        self._step: int = 0
        self._done: bool = False
        self._queue: list[Email] = []
        self._total_reward: float = 0.0
        self._correct_classifications: int = 0

    # ── Public API ───────────────────────────────────────────────────────

    def reset(self) -> Observation:
        """Reset environment, return first observation."""
        self._rng = random.Random(self.seed)
        self._step = 0
        self._done = False
        self._total_reward = 0.0
        self._correct_classifications = 0

        # Shuffle and pick emails for this episode
        pool = list(self.config.emails)
        self._rng.shuffle(pool)
        self._queue = pool[: self.config.max_steps]

        return self._make_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """Process the agent's triage decision and advance to the next email."""
        if self._done:
            raise RuntimeError("Episode is done — call reset() first.")

        current_email = self._queue[self._step]
        reward, info = self._compute_reward(current_email, action)

        self._total_reward += reward
        self._step += 1

        if self._step >= len(self._queue):
            self._done = True

        obs = self._make_observation() if not self._done else self._make_terminal_observation()
        return obs, reward, self._done, info

    def get_state(self) -> dict:
        """Return serialisable snapshot of the environment state."""
        return {
            "step": self._step,
            "done": self._done,
            "total_reward": round(self._total_reward, 4),
            "accuracy": round(
                self._correct_classifications / max(self._step, 1), 4
            ),
            "emails_processed": self._step,
            "emails_total": len(self._queue),
        }

    # ── Internal helpers ─────────────────────────────────────────────────

    def _make_observation(self) -> Observation:
        email = self._queue[min(self._step, len(self._queue) - 1)]
        return Observation(
            timestep=self._step,
            email=email,
            emails_remaining=len(self._queue) - self._step,
            accuracy_so_far=round(
                self._correct_classifications / max(self._step, 1), 4
            ),
        )

    def _make_terminal_observation(self) -> Observation:
        """Return a terminal observation reusing the last email."""
        return Observation(
            timestep=self._step,
            email=self._queue[-1],
            emails_remaining=0,
            accuracy_so_far=round(
                self._correct_classifications / max(self._step, 1), 4
            ),
        )

    def _compute_reward(
        self, email: Email, action: Action
    ) -> Tuple[float, Dict[str, Any]]:
        """Compute shaped reward for a single step.

        Reward components
        -----------------
        1. Classification accuracy  (weight from config, default 0.40)
        2. Reply quality            (weight from config, default 0.30)
        3. Priority accuracy        (weight from config, default 0.20)
        4. Efficiency bonus         (weight from config, default 0.10)
        """
        info: Dict[str, Any] = {}

        # 1. Classification ───────────────────────────────────────────────
        cat_correct = action.category.lower() == email.true_category.lower()
        classification_score = 1.0 if cat_correct else 0.0
        if cat_correct:
            self._correct_classifications += 1
        info["classification_correct"] = cat_correct

        # 2. Reply quality ────────────────────────────────────────────────
        reply_lower = action.reply.lower()
        if email.expected_reply_keywords:
            keyword_hits = sum(
                1 for kw in email.expected_reply_keywords if kw.lower() in reply_lower
            )
            reply_score = keyword_hits / len(email.expected_reply_keywords)
        else:
            # No expected keywords — give partial credit for non-empty reply
            reply_score = min(len(action.reply) / 50.0, 1.0) if action.reply else 0.0
        info["reply_score"] = round(reply_score, 4)

        # 3. Priority accuracy ────────────────────────────────────────────
        priority_diff = abs(action.priority - email.true_priority)
        priority_score = max(0.0, 1.0 - priority_diff * 0.25)
        info["priority_score"] = round(priority_score, 4)

        # 4. Efficiency bonus ─────────────────────────────────────────────
        reply_len = len(action.reply)
        if 10 <= reply_len <= 200:
            efficiency_score = 1.0
        elif reply_len > 200:
            efficiency_score = max(0.0, 1.0 - (reply_len - 200) / 300.0)
        else:
            efficiency_score = reply_len / 10.0
        info["efficiency_score"] = round(efficiency_score, 4)

        # Weighted sum
        w = self.config
        reward = (
            w.classification_weight * classification_score
            + w.reply_weight * reply_score
            + w.priority_weight * priority_score
            + w.efficiency_weight * efficiency_score
        )
        reward = round(min(max(reward, 0.0), 1.0), 4)
        info["reward_breakdown"] = {
            "classification": round(w.classification_weight * classification_score, 4),
            "reply": round(w.reply_weight * reply_score, 4),
            "priority": round(w.priority_weight * priority_score, 4),
            "efficiency": round(w.efficiency_weight * efficiency_score, 4),
        }

        return reward, info
