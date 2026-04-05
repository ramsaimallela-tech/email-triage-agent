"""LLMAgent — an LLM-powered agent for email triage.

This agent uses the OpenAI client to classify emails and generate replies.
"""

from __future__ import annotations
import json
from openai import OpenAI
from env.models import Action, Observation

class LLMAgent:
    """LLM-based email triage agent."""

    def __init__(self, client: OpenAI, model_name: str) -> None:
        self.client = client
        self.model_name = model_name

    def select_action(self, obs: Observation) -> Action:
        """Use an LLM to decide on the triage action."""
        email = obs.email
        
        prompt = f"""
You are an expert email triage assistant. Your task is to classify an incoming email and draft a professional reply.

Email Details:
- Subject: {email.subject}
- Sender: {email.sender}
- Body: {email.email_text}
- Has Attachments: {email.has_attachments}
- Thread Length: {email.thread_length}

Tasks:
1. Classify the email as 'important', 'spam', or 'normal'.
2. Assign a priority level from 1 (highest) to 5 (lowest).
3. Draft a professional reply (keep it concise). If the email is spam, the reply should be an empty string.

Return your response in strict JSON format:
{{
  "category": "important|spam|normal",
  "priority": 1-5,
  "reply": "your draft reply"
}}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {{"role": "system", "content": "You are a professional email triage assistant."}},
                    {{"role": "user", "content": prompt}}
                ],
                response_format={{ "type": "json_object" }}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            return Action(
                category=data.get("category", "normal"),
                priority=data.get("priority", 3),
                reply=data.get("reply", "")
            )
        except Exception as e:
            # Fallback to a safe default in case of LLM error
            return Action(category="normal", priority=3, reply="Acknowledgment received.")
