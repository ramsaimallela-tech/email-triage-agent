"""LLM-powered agent for email triage."""

from __future__ import annotations
import json
from openai import OpenAI
from env.models import Action, Observation

class LLMAgent:
    def __init__(self, client: OpenAI, model_name: str) -> None:
        self.client = client
        self.model_name = model_name

    def select_action(self, obs: Observation) -> Action:
        email = obs.email
        
        prompt = f"""
Analyze this email and provide a triage decision in JSON.

Subject: {email.subject}
Sender: {email.sender}
Body: {email.email_text}
Attachments: {email.has_attachments}
Thread Size: {email.thread_length}

Output Schema:
{{
  "category": "important | spam | normal",
  "priority": 1-5,
  "reply": "concise professional reply (leave empty if spam)"
}}
"""
        try:
            api_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a professional email triage system."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            raw_content = api_response.choices[0].message.content
            parsed = json.loads(raw_content)
            
            return Action(
                category=parsed.get("category", "normal"),
                priority=parsed.get("priority", 3),
                reply=parsed.get("reply", "")
            )
        except Exception:
            # Fallback for API failures
            return Action(category="normal", priority=3, reply="Acknowledgment received.")
