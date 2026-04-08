"""EmailEnv: OpenEnv-compatible email triage environment."""

import random
from typing import Tuple, Dict, Any

from env.models import Email, Action, Observation


class EmailEnv:
    def __init__(self, config: dict, seed: int = 42):
        self.config = config
        self.seed   = seed
        self._rng   = random.Random(seed)
        self._emails = config.get("emails", [])
        self._index  = 0
        self._correct = 0
        self._step    = 0

    # ── internal helpers ──────────────────────────────────────────────────────
    def _build_email(self, raw: dict, email_id: int) -> Email:
        return Email(
            email_id=email_id,
            subject=raw.get("subject", ""),
            email_text=raw.get("email_text", ""),
            sender=raw.get("sender", "user@example.com"),
            timestamp=raw.get("timestamp", "2026-04-05T12:00:00Z"),
            true_category=raw.get("true_category", "normal"),
            true_priority=raw.get("true_priority", 3),
            has_attachments=raw.get("has_attachments", False),
            thread_length=raw.get("thread_length", 1),
        )

    def _compute_reward(self, email: Email, action: Action) -> float:
        weights = self.config.get("reward_weights", {
            "classification": 0.40,
            "reply":          0.30,
            "priority":       0.20,
            "efficiency":     0.10,
        })

        # Classification accuracy
        cls_score = 1.0 if action.category == email.true_category else 0.0

        # Priority accuracy (closer = better)
        pri_diff  = abs(action.priority - email.true_priority)
        pri_score = max(0.0, 1.0 - pri_diff / 4.0)

        # Reply quality (keyword presence)
        reply_len  = len(action.reply.strip())
        if email.true_category == "spam":
            rep_score = 1.0 if reply_len == 0 else 0.5
        else:
            rep_score = min(1.0, reply_len / 100.0) if reply_len > 0 else 0.0

        # Efficiency bonus
        eff_score = 1.0 if 10 <= reply_len <= 200 else 0.5

        reward = (
            weights["classification"] * cls_score
            + weights["priority"]       * pri_score
            + weights["reply"]          * rep_score
            + weights["efficiency"]     * eff_score
        )
        return round(min(max(reward, 0.0), 1.0), 4)

    # ── public API ────────────────────────────────────────────────────────────
    def reset(self) -> Observation:
        self._rng     = random.Random(self.seed)
        self._index   = 0
        self._correct = 0
        self._step    = 0
        self._shuffled = list(self._emails)
        self._rng.shuffle(self._shuffled)
        email = self._build_email(self._shuffled[0], 0)
        return Observation(
            timestep=0,
            email=email,
            emails_remaining=len(self._shuffled) - 1,
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        current_email = self._build_email(self._shuffled[self._index], self._index)
        reward        = self._compute_reward(current_email, action)

        if action.category == current_email.true_category:
            self._correct += 1
        self._step  += 1
        self._index += 1

        done = self._index >= len(self._shuffled)

        if not done:
            next_email = self._build_email(self._shuffled[self._index], self._index)
            obs = Observation(
                timestep=self._step,
                email=next_email,
                emails_remaining=len(self._shuffled) - self._index - 1,
                accuracy_so_far=round(self._correct / self._step, 4),
            )
        else:
            obs = Observation(
                timestep=self._step,
                email=current_email,
                emails_remaining=0,
                accuracy_so_far=round(self._correct / self._step, 4),
            )

        info = {
            "true_category": current_email.true_category,
            "true_priority":  current_email.true_priority,
            "correct":        action.category == current_email.true_category,
        }
        return obs, reward, done, info
