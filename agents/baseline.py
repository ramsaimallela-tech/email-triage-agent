"""Rule-based heuristic agent for email triage."""

from __future__ import annotations
import random
from env.models import Action, Observation

class BaselineAgent:
    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)

    def select_action(self, obs: Observation) -> Action:
        email = obs.email
        content = f"{email.subject} {email.email_text}".lower()

        cat = self._classify(content, email.sender)
        prio = self._get_priority(cat, content)
        draft = self._generate_draft(cat, content)

        return Action(category=cat, priority=prio, reply=draft)

    @staticmethod
    def _classify(text: str, sender: str) -> str:
        spam_keywords = {
            "won", "lottery", "claim", "free", "click here",
            "act now", "limited time", "congratulations",
            "winner", "prize", "crypto", "investment opportunity",
            "survey", "suspended"
        }
        urgent_keywords = {
            "urgent", "asap", "critical", "deadline", "action required",
            "escalation", "security alert", "downtime", "server",
            "board meeting", "cfo", "ceo", "legal", "compliance",
            "contract", "budget", "production"
        }

        spam_hits = sum(1 for kw in spam_keywords if kw in text)
        urgent_hits = sum(1 for kw in urgent_keywords if kw in text)

        # Heuristic for suspicious senders
        if any(tld in sender.lower() for tld in [".xyz", ".net", ".info"]):
            spam_hits += 2

        if spam_hits > urgent_hits and spam_hits >= 2:
            return "spam"
        return "important" if urgent_hits >= 1 else "normal"

    @staticmethod
    def _get_priority(category: str, text: str) -> int:
        if category == "spam":
            return 5
        
        if category == "important":
            high_priority_triggers = {"urgent", "asap", "critical", "downtime", "security"}
            return 1 if any(t in text for t in high_priority_triggers) else 2
        
        return 4

    @staticmethod
    def _generate_draft(category: str, text: str) -> str:
        if category == "spam":
            return ""

        if category == "important":
            if "deadline" in text or "action required" in text:
                return (
                    "I acknowledge the deadline and am preparing the required items. "
                    "I shall investigate and provide an update shortly."
                )
            if "security" in text or "alert" in text:
                return (
                    "I am investigating this security concern immediately. "
                    "Will update with findings and secure the account as needed."
                )
            if "escalation" in text or "client" in text:
                return (
                    "I understand the urgency of this escalation and shall prioritise "
                    "a fix with the engineering team. Expect an update by EOD."
                )
            return (
                "Thank you for the heads-up. I shall review the details with the team "
                "and provide an update on next steps by end of day."
            )

        return (
            "Thanks for the email. I shall review this and get back to you shortly. "
            "Please let me know if there is anything urgent I should attend to."
        )
