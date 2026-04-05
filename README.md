---
title: Email Triage Agent
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.25.0
python_version: "3.10"
app_file: app.py
pinned: false
---

# Email Triage Agent — OpenEnv Agent Project

[![OpenEnv Compatible](https://img.shields.io/badge/OpenEnv-1.0-blue)](openenv.yaml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-brightgreen)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

An **OpenEnv-compatible AI agent environment** that simulates real-world email triage. An agent must classify incoming emails (important, spam, normal), assign priority levels, and draft appropriate replies — balancing classification accuracy, reply quality, and response efficiency.

---

## Real-World Motivation

Email triage is a universal challenge: professionals spend **28% of their workday** on email. Misclassification causes:

- **Missed deadlines** — important emails buried under noise
- **Security breaches** — phishing or spam emails acted upon
- **Productivity loss** — normal emails treated as urgent

This environment simulates those triage decisions at a realistic level, making it an ideal testbed for AI agents in knowledge-worker automation.

---

## Project Structure

```
email-triage-agent/
├── openenv.yaml              # OpenEnv spec (observation, action, reward)
├── env/
│   ├── environment.py        # EmailEnv: reset / step / get_state
│   └── models.py             # Pydantic models (Email, Action, Observation)
├── tasks/
│   ├── easy.py               # 5-step, clear-cut emails
│   ├── medium.py             # 8-step, ambiguous emails
│   └── hard.py               # 12-step, complex multi-context emails
├── agents/
│   └── baseline.py           # BaselineAgent: keyword-based heuristics
├── grader/
│   └── grader.py             # Grader: N-episode evaluation, JSON report
├── scripts/
│   └── run_baseline.py       # CLI runner: evaluates all tasks, saves report
├── results/                   # Auto-created; stores baseline_report.json
├── app.py                     # Gradio UI for Hugging Face Spaces
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Observation Space

Each timestep the agent receives an `Observation`:

| Field              | Type     | Description                               |
|--------------------|----------|-------------------------------------------|
| `timestep`         | `int`    | Current step within the episode           |
| `email.email_text` | `string` | Full body of the incoming email           |
| `email.subject`    | `string` | Email subject line                        |
| `email.sender`     | `string` | Sender email address                      |
| `email.timestamp`  | `string` | ISO-8601 arrival timestamp                |
| `email.has_attachments` | `bool` | Whether attachments are present        |
| `email.thread_length`  | `int`  | Number of prior emails in thread         |
| `emails_remaining` | `int`    | Emails left in the queue                  |
| `accuracy_so_far`  | `float`  | Running classification accuracy           |

---

## Action Space

The agent returns an `Action`:

| Field      | Type     | Description                                   |
|------------|----------|-----------------------------------------------|
| `category` | `enum`   | Classification: `important`, `spam`, `normal` |
| `priority` | `int`    | Priority level `1-5` (1 = highest)            |
| `reply`    | `string` | Draft reply text (empty for spam)             |

---

## Reward Design

Reward is a **continuous shaped float [0.0, 1.0]** — never binary. Each step:

| Component                | Weight    | Description                                    |
|--------------------------|-----------|------------------------------------------------|
| Classification accuracy  | 0.35-0.50 | Correct category assignment                    |
| Reply quality            | 0.20-0.35 | Keyword relevance of the reply                 |
| Priority accuracy        | 0.20      | Closeness to ground-truth priority             |
| Efficiency bonus         | 0.10      | Concise, actionable replies (10-200 chars ideal)|

Weights vary by task difficulty (easy tasks weight classification more heavily).

---

## Baseline Agent Scores

The `BaselineAgent` uses keyword heuristics with seed `42`. Scores are averages over 10 episodes:

| Task   | Max Steps | Mean Reward | Classification | Success Rate |
|--------|-----------|-------------|----------------|--------------|
| Easy   | 5         | ~0.65-0.80  | ~80-100%       | ~80-100%     |
| Medium | 8         | ~0.40-0.55  | ~60-80%        | ~40-60%      |
| Hard   | 12        | ~0.20-0.40  | ~50-70%        | ~20-40%      |

---

## Setup

### Option 1 — pip

```bash
git clone https://github.com/ramsaimallela-tech/email-triage-agent.git
cd email-triage-agent
pip install -r requirements.txt
```

### Option 2 — Docker

```bash
docker build -t email-triage-agent .
docker run email-triage-agent
```

---

## Running the Baseline Agent

```bash
# Evaluate all three task difficulties
python scripts/run_baseline.py

# Evaluate only easy and medium
python scripts/run_baseline.py --tasks easy medium

# Run 20 episodes per task with a custom seed
python scripts/run_baseline.py --episodes 20 --seed 7

# Save report to a custom path
python scripts/run_baseline.py --output results/my_report.json
```

### Expected Output

```
============================================================
  Task: EASY | Episodes: 10 | Seed: 42
============================================================
  Mean Reward:       0.6800
  Min / Max Reward:  0.6200 / 0.7400
  Classification:    85.0%
  Success Rate:      90.0%

[OK] Full report saved to results/baseline_report.json
```

---

## Building a Custom Agent

Implement any class with a `select_action` method:

```python
from env.models import Action, Observation

class MyAgent:
    def select_action(self, obs: Observation) -> Action:
        # Your logic here
        return Action(
            category="important",
            priority=2,
            reply="I shall look into this straightaway.",
        )
```

Then evaluate with the Grader:

```python
from env.environment import EmailEnv
from grader.grader import Grader
from tasks import ALL_CONFIGS

config = ALL_CONFIGS["hard"]
env    = EmailEnv(config, seed=42)
agent  = MyAgent()

grader = Grader(env, agent, num_episodes=10)
report = grader.run()
print(report["aggregate"])
```

---

## Hugging Face Spaces Deployment

### 1. Create the Space

Navigate to [huggingface.co/spaces](https://huggingface.co/spaces), select **New Space**, choose SDK **Gradio**, and set Python version to 3.11.

Your Space URL will be: `https://huggingface.co/spaces/Ram2k7/email-triage-agent`

### 2. Upload files

Push the full project (all files except `results/`) to the Space repository:

```bash
git clone https://huggingface.co/spaces/Ram2k7/email-triage-agent
# Copy all project files into the cloned repository
cd email-triage-agent
git add .
git commit -m "Initial deployment"
git push
```

### 3. Launch

Hugging Face will automatically install dependencies from `requirements.txt` and launch `app.py`, which provides:
- **Batch Evaluation** tab — run the grader with configurable episodes and seed
- **Try Single Email** tab — paste a custom email and observe the agent's decision

---

## Author

**Ram Sai Mallela** — [@ramsaimallela-tech](https://github.com/ramsaimallela-tech)

---

## Licence

MIT — free to use, modify, and distribute.
