"""Gradio app for Hugging Face Spaces deployment.

Provides an interactive UI to evaluate the baseline agent on different
task difficulties.

Author: Ram Sai Mallela (@ramsaimallela-tech)
Space:  https://huggingface.co/spaces/Ram2k7/email-triage-agent
"""

import gradio as gr
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from env.environment import EmailEnv
from agents.baseline import BaselineAgent
from grader.grader import Grader
from tasks import ALL_CONFIGS


def evaluate(task: str, episodes: int, seed: int):
    """Run the baseline agent and return the grading report."""
    config = ALL_CONFIGS[task]
    env = EmailEnv(config, seed=int(seed))
    agent = BaselineAgent(seed=int(seed))
    grader = Grader(env, agent, num_episodes=int(episodes))
    report = grader.run()
    return json.dumps(report["aggregate"], indent=2)


def triage_single(email_subject: str, email_body: str, sender: str):
    """Demonstrate the baseline agent on a single custom email."""
    from env.models import Email, Observation

    email = Email(
        email_id=0,
        subject=email_subject,
        email_text=email_body,
        sender=sender,
        timestamp="2026-04-05T00:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=3,
        expected_reply_keywords=[],
    )
    obs = Observation(timestep=0, email=email, emails_remaining=1)
    agent = BaselineAgent(seed=42)
    action = agent.select_action(obs)

    return (
        f"Category: {action.category.upper()}\n"
        f"Priority: {action.priority}/5\n"
        f"Reply:\n{action.reply if action.reply else '(no reply — spam detected)'}"
    )


# -- Gradio Interface --------------------------------------------------------

with gr.Blocks(
    title="Email Triage Agent Grader",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown(
        "# Email Triage Agent — OpenEnv Grader\n"
        "by [Ram Sai Mallela](https://github.com/ramsaimallela-tech)\n\n"
        "Evaluate the baseline agent on the email triage environment, "
        "or try it on a custom email."
    )

    with gr.Tab("Batch Evaluation"):
        gr.Markdown("Run the baseline agent over multiple episodes and view aggregate scores.")
        with gr.Row():
            task_input = gr.Dropdown(
                ["easy", "medium", "hard"], value="easy", label="Task Difficulty"
            )
            episode_input = gr.Slider(1, 20, value=5, step=1, label="Episodes")
            seed_input = gr.Number(value=42, label="Random Seed")
        eval_btn = gr.Button("Evaluate", variant="primary")
        eval_output = gr.Textbox(label="Grading Report (JSON)", lines=12)
        eval_btn.click(evaluate, [task_input, episode_input, seed_input], eval_output)

    with gr.Tab("Try Single Email"):
        gr.Markdown("Paste a custom email and observe how the baseline agent triages it.")
        subject_input = gr.Textbox(label="Subject", value="Urgent: Server issue")
        body_input = gr.Textbox(
            label="Email Body",
            lines=5,
            value="Our production server is down. Clients are affected. Need immediate action.",
        )
        sender_input = gr.Textbox(label="Sender", value="ops@company.com")
        triage_btn = gr.Button("Triage Email", variant="primary")
        triage_output = gr.Textbox(label="Agent Decision", lines=6)
        triage_btn.click(
            triage_single, [subject_input, body_input, sender_input], triage_output
        )

if __name__ == "__main__":
    demo.launch()
