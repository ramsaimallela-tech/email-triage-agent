"""BaselineAgent — rule-based keyword heuristic agent for email triage.

This agent uses simple keyword matching to classify emails and generates
template-based replies. It serves as a reproducible lower-bound baseline.

Author: Ram Sai Mallela (@ramsaimallela-tech)
"""

from __future__ import annotations

import random
from env.models import Action, Observation


class BaselineAgent:
    """Reactive keyword-based email triage agent."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)

    def select_action(self, obs: Observation) -> Action:
        """Classify the email and draft a reply based on keyword heuristics."""
        email = obs.email
        text = (email.subject + " " + email.email_text).lower()

        # ── Classification ───────────────────────────────────────────────
        category = self._classify(text, email.sender)

        # ── Priority ─────────────────────────────────────────────────────
        priority = self._assign_priority(category, text)

        # ── Reply ────────────────────────────────────────────────────────
        reply = self._generate_reply(category, text)

        return Action(category=category, priority=priority, reply=reply)

    # ── Internal heuristics ──────────────────────────────────────────────

    @staticmethod
    def _classify(text: str, sender: str) -> str:
        """Keyword-based classification."""
        spam_signals = [
            "won", "lottery", "claim", "free", "click here",
            "act now", "limited time", "congratulations",
            "winner", "prize", "crypto", "investment opportunity",
            "survey", "suspended",
        ]
        important_signals = [
            "urgent", "asap", "critical", "deadline", "action required",
            "escalation", "security alert", "downtime", "server",
            "board meeting", "cfo", "ceo", "legal", "compliance",
            "contract", "budget", "production",
        ]

        spam_score = sum(1 for s in spam_signals if s in text)
        important_score = sum(1 for s in important_signals if s in text)

        # Suspicious sender domains boost spam score
        suspicious_tlds = [".xyz", ".net", ".info"]
        if any(tld in sender.lower() for tld in suspicious_tlds):
            spam_score += 2

        if spam_score > important_score and spam_score >= 2:
            return "spam"
        elif important_score >= 1:
            return "important"
        else:
            return "normal"

    @staticmethod
    def _assign_priority(category: str, text: str) -> int:
        """Simple priority assignment."""
        if category == "spam":
            return 5
        elif category == "important":
            if any(w in text for w in ["urgent", "asap", "critical", "downtime", "security"]):
                return 1
            return 2
        else:
            return 4

    @staticmethod
    def _generate_reply(category: str, text: str) -> str:
        """Template-based reply generation."""
        if category == "spam":
            return ""  # Don't reply to spam

        if category == "important":
            if "deadline" in text or "action required" in text:
                return (
                    "Thank you for flagging this. I acknowledge the deadline and "
                    "shall prepare the required items. I shall investigate and provide "
                    "an update shortly."
                )
            if "security" in text or "alert" in text:
                return (
                    "I shall investigate this security concern immediately and secure "
                    "the account. Will update with findings and enable 2FA as needed."
                )
            if "escalation" in text or "client" in text:
                return (
                    "I understand the urgency of this escalation. I shall prioritise "
                    "getting engineering to fix this and shall provide an update to "
                    "the client today."
                )
            return (
                "Thank you for bringing this to my attention. I shall review the "
                "details, check with the team, and provide an update on the "
                "next steps by end of day."
            )

        # Normal emails
        return (
            "Thanks for your email. I shall review this and get back to you shortly. "
            "Please let me know if there is anything urgent I should attend to."
        )
