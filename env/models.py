"""Data models for the email triage environment."""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class Email(BaseModel):
    """Represents a single email in the processing queue."""
    email_id: int
    subject: str
    email_text: str
    sender: str
    timestamp: str # ISO-8601
    has_attachments: bool = False
    thread_length: int = 1
    
    # Ground-truth (hidden from the agent)
    true_category: str
    true_priority: int
    expected_reply_keywords: List[str] = Field(default_factory=list)

class Observation(BaseModel):
    """State snapshot provided to the agent at each step."""
    timestep: int
    email: Email
    emails_remaining: int
    accuracy_so_far: float = 0.0

class Action(BaseModel):
    """The agent's decision for a given email."""
    category: str # important | spam | normal
    priority: int = Field(default=3, ge=1, le=5)
    reply: str = ""

class StepResult(BaseModel):
    """Container for the results of an environment step."""
    observation: Observation
    reward: float
    done: bool = False
    info: dict = Field(default_factory=dict)

class TaskConfig(BaseModel):
    """Configuration defining a specific task's difficulty and scoring."""
    name: str # easy | medium | hard
    description: str = ""
    max_steps: int
    emails: List[Email]
    
    # Scoring weights
    classification_weight: float = 0.40
    reply_weight: float = 0.30
    priority_weight: float = 0.20
    efficiency_weight: float = 0.10
