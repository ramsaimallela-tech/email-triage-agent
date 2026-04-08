from pydantic import BaseModel
from typing import Optional

class Email(BaseModel):
    email_id: int
    subject: str
    email_text: str
    sender: str
    timestamp: str
    true_category: str
    true_priority: int
    has_attachments: bool = False
    thread_length: int = 1

class Action(BaseModel):
    category: str   # important | spam | normal
    priority: int   # 1-5
    reply: str = ""

class Observation(BaseModel):
    timestep: int
    email: Email
    emails_remaining: int
    accuracy_so_far: float = 0.0
