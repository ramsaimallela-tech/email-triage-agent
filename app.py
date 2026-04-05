"""Gradio-based interactive UI for Email Triage Agent evaluation."""

import gradio as gr
import json
import sys
import os

# Base directory for absolute imports
sys.path.insert(0, os.path.dirname(__file__))

from env.environment import EmailEnv
from agents.baseline import BaselineAgent
from grader.grader import Grader
from tasks import ALL_CONFIGS

def run_evaluation(difficulty: str, num_episodes: int, random_seed: int):
    """Execute a batch evaluation of the baseline agent."""
    env_config = ALL_CONFIGS[difficulty]
    env = EmailEnv(env_config, seed=int(random_seed))
    agent = BaselineAgent(seed=int(random_seed))
    
    evaluator = Grader(env, agent, num_episodes=int(num_episodes))
    report = evaluator.run()
    return json.dumps(report["aggregate"], indent=2)

def triage_manual(sub: str, body: str, from_addr: str):
    """Test the agent's logic on a single custom email."""
    from env.models import Email, Observation

    mock_email = Email(
        email_id=0,
        subject=sub,
        email_text=body,
        sender=from_addr,
        timestamp="2026-04-05T12:00:00Z",
        true_category="normal",
        true_priority=3
    )
    
    state = Observation(timestep=0, email=mock_email, emails_remaining=1)
    agent = BaselineAgent(seed=42)
    decision = agent.select_action(state)

    return (
        f"Category: {decision.category.upper()}\n"
        f"Priority: {decision.priority}/5\n"
        f"Draft Reply:\n{decision.reply if decision.reply else '(No reply drafted)'}"
    )

# For local evaluation testing (uncomment to run just Gradle UI)
# if __name__ == "__main__":
#     demo.launch()

