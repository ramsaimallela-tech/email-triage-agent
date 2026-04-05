"""Typed Pydantic models for the Email Triage Agent environment."""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


# ── Email Data ───────────────────────────────────────────────────────────────

class Email(BaseModel):
    """A single email in the triage queue."""
    email_id: int = Field(..., description="Unique identifier for this email")
    subject: str = Field(..., description="Email subject line")
    email_text: str = Field(..., description="Full body of the email")
    sender: str = Field(..., description="Sender email address")
    timestamp: str = Field(..., description="ISO-8601 arrival timestamp")
    has_attachments: bool = Field(default=False, description="Whether attachments are present")
    thread_length: int = Field(default=1, description="Number of prior emails in this thread")
    # Ground-truth labels (hidden from agent, used by grader)
    true_category: str = Field(..., description="Ground-truth category: important | spam | normal")
    true_priority: int = Field(..., description="Ground-truth priority 1-5")
    expected_reply_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords a good reply should contain",
    )


# ── Observation (what the agent sees) ────────────────────────────────────────

class Observation(BaseModel):
    """What the agent receives at each step."""
    timestep: int = Field(..., description="Current step in the episode")
    email: Email = Field(..., description="The email to triage")
    emails_remaining: int = Field(..., description="Emails left in the queue")
    accuracy_so_far: float = Field(default=0.0, description="Running classification accuracy")


# ── Action (what the agent returns) ──────────────────────────────────────────

class Action(BaseModel):
    """Agent's triage decision."""
    category: str = Field(..., description="Classification: important | spam | normal")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level 1-5")
    reply: str = Field(default="", description="Draft reply text")


# ── Step Result ──────────────────────────────────────────────────────────────

class StepResult(BaseModel):
    """Result returned by env.step()."""
    observation: Observation
    reward: float = Field(..., description="Shaped reward for this step")
    done: bool = Field(default=False, description="Whether the episode is over")
    info: dict = Field(default_factory=dict, description="Extra diagnostics")


# ── Task Configuration ───────────────────────────────────────────────────────

class TaskConfig(BaseModel):
    """Configuration for a single task difficulty."""
    name: str = Field(..., description="Task name: easy | medium | hard")
    description: str = Field(default="", description="Human-readable description")
    max_steps: int = Field(..., description="Max emails per episode")
    emails: List[Email] = Field(..., description="Email pool for this task")
    classification_weight: float = Field(default=0.40)
    reply_weight: float = Field(default=0.30)
    priority_weight: float = Field(default=0.20)
    efficiency_weight: float = Field(default=0.10)
