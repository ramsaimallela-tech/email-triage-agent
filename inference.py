"""Formal inference script for the Email Triage Agent."""

import os
import sys
import json

# Ensure project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from env.environment import EmailEnv
from agents.llm_agent import LLMAgent
from tasks import ALL_CONFIGS

# Try importing OpenAI; fall back gracefully if unavailable
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Configuration from Environment
API_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL   = os.getenv("MODEL_NAME",   "gpt-4-turbo")
TOKEN   = os.getenv("HF_TOKEN")

TASKS = ["easy", "medium", "hard"]


def run_task(task_name: str, client, model: str) -> dict:
    """Run one full episode for a given task and return aggregate metrics."""
    config = ALL_CONFIGS[task_name]
    env    = EmailEnv(config, seed=42)
    agent  = LLMAgent(client, model)

    observation  = env.reset()
    is_finished  = False
    step_index   = 0
    total_reward = 0.0

    # ── [START] block ────────────────────────────────────────────────────────
    print(f"[START] task={task_name}", flush=True)

    while not is_finished:
        agent_action = agent.select_action(observation)
        observation, step_reward, is_finished, step_metadata = env.step(agent_action)

        total_reward += step_reward
        step_index   += 1

        # ── [STEP] block ─────────────────────────────────────────────────────
        print(
            f"[STEP] step={step_index} reward={step_reward:.4f} "
            f"category={agent_action.category} priority={agent_action.priority}",
            flush=True,
        )

    score = total_reward / max(step_index, 1)

    # ── [END] block ──────────────────────────────────────────────────────────
    print(
        f"[END] task={task_name} score={score:.4f} steps={step_index}",
        flush=True,
    )

    return {
        "task":         task_name,
        "steps":        step_index,
        "total_reward": round(total_reward, 4),
        "score":        round(score,        4),
    }


def main():
    # ── Build a client (real or stub) ────────────────────────────────────────
    if OPENAI_AVAILABLE and TOKEN:
        client = OpenAI(api_key=TOKEN, base_url=API_URL)
    elif OPENAI_AVAILABLE:
        client = OpenAI(api_key="no-token", base_url=API_URL)
    else:
        client = None   # LLMAgent must handle None gracefully

    results = []
    for task_name in TASKS:
        try:
            result = run_task(task_name, client, MODEL)
            results.append(result)
        except Exception as exc:          # never crash the whole run
            print(f"[ERROR] task={task_name} error={exc}", flush=True)
            print(f"[END] task={task_name} score=0.0 steps=0",  flush=True)

    # Final JSON summary (useful for LLM Criteria Check)
    print(json.dumps({"results": results}, indent=2), flush=True)


if __name__ == "__main__":
    main()
