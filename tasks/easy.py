"""Easy task — clear-cut emails with obvious labels."""

from env.models import Email, TaskConfig

EASY_EMAILS = [
    Email(
        email_id=1,
        subject="URGENT: Server downtime affecting production",
        email_text="Hi team, our main production server went down at 3:00 AM. "
                   "Multiple clients are affected. We need immediate action to "
                   "restore services. Please respond ASAP.",
        sender="ops-lead@company.com",
        timestamp="2026-03-31T03:15:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["acknowledge", "investigating", "restore", "update"],
    ),
    Email(
        email_id=2,
        subject="You've WON $1,000,000 — Claim NOW!!!",
        email_text="Dear Lucky Winner, you have been selected for our grand prize "
                   "of ONE MILLION DOLLARS. Click the link below to claim your "
                   "winnings immediately. Act now before it expires!",
        sender="prize-notification@free-lottery.xyz",
        timestamp="2026-03-31T08:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="spam",
        true_priority=5,
        expected_reply_keywords=[],
    ),
    Email(
        email_id=3,
        subject="Team lunch this Friday",
        email_text="Hey everyone, just a reminder that we have our monthly team "
                   "lunch this Friday at 12:30 PM at the usual place. RSVP if "
                   "you haven't already. Looking forward to seeing you all!",
        sender="hr@company.com",
        timestamp="2026-03-31T09:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=4,
        expected_reply_keywords=["thanks", "attend"],
    ),
    Email(
        email_id=4,
        subject="FINAL WARNING: Account suspended",
        email_text="Your account has been suspended due to suspicious activity. "
                   "Click here to verify your identity or your account will be "
                   "permanently deleted within 24 hours.",
        sender="security-alert@bank-verify.net",
        timestamp="2026-03-31T10:30:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="spam",
        true_priority=5,
        expected_reply_keywords=[],
    ),
    Email(
        email_id=5,
        subject="Q1 Budget Review Meeting — Action Required",
        email_text="Hi, the CFO has requested all department heads submit their "
                   "Q1 budget summaries before the review meeting on Monday. "
                   "Please prepare your reports and send them to finance@company.com.",
        sender="cfo@company.com",
        timestamp="2026-03-31T11:00:00Z",
        has_attachments=True,
        thread_length=2,
        true_category="important",
        true_priority=2,
        expected_reply_keywords=["budget", "submit", "monday", "prepare"],
    ),
    Email(
        email_id=6,
        subject="Weekly newsletter — Top tech stories",
        email_text="Here are this week's top tech stories: 1) AI breakthrough in "
                   "protein folding, 2) New smartphone launches, 3) Open-source "
                   "framework update. Read more on our website.",
        sender="newsletter@technews.com",
        timestamp="2026-03-31T07:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=5,
        expected_reply_keywords=[],
    ),
]

EASY_CONFIG = TaskConfig(
    name="easy",
    description="Clear-cut emails with obvious spam/important labels. "
                "Reward is primarily from classification accuracy.",
    max_steps=5,
    emails=EASY_EMAILS,
    classification_weight=0.50,
    reply_weight=0.20,
    priority_weight=0.20,
    efficiency_weight=0.10,
)
