"""Keyword-based heuristic baseline agent."""
import random
from env.models import Action, Observation

SPAM_KEYWORDS      = ["lottery", "winner", "cheap", "discount", "click here", "prize", "offer", "buy now", "exclusive", "unsubscribe", "pirate", "scam"]
IMPORTANT_KEYWORDS = ["urgent", "invoice", "security", "server down", "contract", "nda", "incident", "payment", "overdue", "alert", "critical", "sign"]

class BaselineAgent:
    def __init__(self, seed: int = 42):
        self._rng = random.Random(seed)

    def select_action(self, obs: Observation) -> Action:
        text  = (obs.email.subject + " " + obs.email.email_text).lower()
        cat   = "normal"
        prio  = 3

        if any(k in text for k in SPAM_KEYWORDS):
            cat, prio, reply = "spam", 5, ""
        elif any(k in text for k in IMPORTANT_KEYWORDS):
            cat, prio = "important", 1
            reply = "Thank you for flagging this. I will address it immediately."
        else:
            reply = "Thank you for your email. I will review and respond shortly."

        return Action(category=cat, priority=prio, reply=reply if cat != "spam" else "")
