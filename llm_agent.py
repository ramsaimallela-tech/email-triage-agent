"""LLM-powered agent with graceful fallback to baseline heuristics."""
import json
from env.models import Action, Observation
from agents.baseline import BaselineAgent

_FALLBACK = BaselineAgent(seed=42)

SYSTEM_PROMPT = """You are an expert email triage assistant.
Given an email, respond ONLY with valid JSON (no markdown) in this exact format:
{"category": "<important|spam|normal>", "priority": <1-5>, "reply": "<draft reply or empty string for spam>"}"""

class LLMAgent:
    def __init__(self, client, model: str):
        self._client  = client
        self._model   = model

    def _call_llm(self, obs: Observation) -> Action:
        user_msg = (
            f"Subject: {obs.email.subject}\n"
            f"From: {obs.email.sender}\n"
            f"Body: {obs.email.email_text}"
        )
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": user_msg},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        raw  = resp.choices[0].message.content.strip()
        data = json.loads(raw)
        return Action(
            category=data.get("category", "normal"),
            priority=int(data.get("priority", 3)),
            reply=data.get("reply", ""),
        )

    def select_action(self, obs: Observation) -> Action:
        if self._client is None:
            return _FALLBACK.select_action(obs)
        try:
            return self._call_llm(obs)
        except Exception:
            return _FALLBACK.select_action(obs)
