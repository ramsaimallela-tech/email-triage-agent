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

# -- UI Definition --

with gr.Blocks(title="Email Triage Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Email Triage Agent — OpenEnv Dashboard")
    
    with gr.Tab("Evaluation Runner"):
        gr.Markdown("Measure baseline agent performance across multiple episodes.")
        with gr.Row():
            task_select = gr.Dropdown(["easy", "medium", "hard"], value="easy", label="Difficulty")
            ep_count = gr.Slider(1, 20, value=5, step=1, label="Episodes")
            seed_val = gr.Number(value=42, label="Seed")
        
        run_btn = gr.Button("Start Evaluation", variant="primary")
        results_out = gr.Textbox(label="Metrics (JSON)", lines=10)
        run_btn.click(run_evaluation, [task_select, ep_count, seed_val], results_out)

    with gr.Tab("Manual Sandbox"):
        gr.Markdown("Test agent classification and drafting on custom input.")
        with gr.Column():
            in_sub = gr.Textbox(label="Subject", value="Project Update")
            in_sender = gr.Textbox(label="From", value="colleague@company.com")
            in_body = gr.Textbox(label="Message Body", lines=5, value="The report is ready for review.")
        
        test_btn = gr.Button("Triage Now", variant="primary")
        test_out = gr.Textbox(label="Agent Decision", lines=6)
        test_btn.click(triage_manual, [in_sub, in_body, in_sender], test_out)

# For local evaluation testing (uncomment to run just Gradle UI)
# if __name__ == "__main__":
#     demo.launch()
