"""Medium task — ambiguous emails requiring reasoning."""

from env.models import Email, TaskConfig

MEDIUM_EMAILS = [
    Email(
        email_id=101,
        subject="Re: Project timeline update",
        email_text="Hi, I just wanted to follow up on the project deadline. "
                   "The client mentioned they might move it up by two weeks. "
                   "Can you check with the team and let me know if that's feasible? "
                   "It's not confirmed yet but we should be ready.",
        sender="pm@company.com",
        timestamp="2026-03-31T09:00:00Z",
        has_attachments=False,
        thread_length=3,
        true_category="important",
        true_priority=2,
        expected_reply_keywords=["check", "team", "feasible", "deadline"],
    ),
    Email(
        email_id=102,
        subject="Invitation to exclusive webinar",
        email_text="You're invited to an exclusive webinar on AI in business. "
                   "This isn't a sales pitch — we have industry leaders sharing "
                   "real case studies. Limited spots available. Register free.",
        sender="events@industry-insights.com",
        timestamp="2026-03-31T10:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=4,
        expected_reply_keywords=["interest", "schedule"],
    ),
    Email(
        email_id=103,
        subject="Your subscription is about to expire",
        email_text="Your premium plan expires in 3 days. Renew now at 20% off. "
                   "We noticed you've been an active user — don't lose your data "
                   "and saved configurations. Use code RENEW20.",
        sender="billing@saas-tool.com",
        timestamp="2026-03-31T11:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=3,
        expected_reply_keywords=["renew", "subscription"],
    ),
    Email(
        email_id=104,
        subject="Fw: Compliance audit findings",
        email_text="Please find attached the preliminary compliance audit report. "
                   "There are 3 medium-severity findings that need to be addressed "
                   "before the end of the quarter. Let's schedule a call to discuss "
                   "remediation steps.",
        sender="compliance@company.com",
        timestamp="2026-03-31T14:00:00Z",
        has_attachments=True,
        thread_length=2,
        true_category="important",
        true_priority=2,
        expected_reply_keywords=["review", "schedule", "findings", "remediation"],
    ),
    Email(
        email_id=105,
        subject="Coffee catch-up?",
        email_text="Hey! It's been a while since we caught up. Would you be free "
                   "for coffee sometime next week? I'd love to hear about what "
                   "you've been working on. No rush — let me know!",
        sender="friend@personal.com",
        timestamp="2026-03-31T16:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=4,
        expected_reply_keywords=["sure", "free", "week"],
    ),
    Email(
        email_id=106,
        subject="IMPORTANT: Update your payment method",
        email_text="We were unable to process your last payment. Please update your "
                   "payment method to avoid service interruption. If you've already "
                   "updated it, please disregard this message.",
        sender="noreply@cloud-provider.com",
        timestamp="2026-03-31T08:30:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="important",
        true_priority=2,
        expected_reply_keywords=["payment", "update", "check"],
    ),
    Email(
        email_id=107,
        subject="Congratulations! You've been pre-approved",
        email_text="Based on your profile, you've been pre-approved for our "
                   "platinum credit card with 0% APR for 12 months. No annual fee. "
                   "Apply now — this offer is personalized for you.",
        sender="offers@creditcard-deals.com",
        timestamp="2026-03-31T07:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="spam",
        true_priority=5,
        expected_reply_keywords=[],
    ),
    Email(
        email_id=108,
        subject="Re: Re: Re: Design review feedback",
        email_text="Thanks for the updated mockups. I think version 3 is much "
                   "closer to what the stakeholders want. Two small tweaks: "
                   "1) increase font size in the header, 2) swap the CTA colour "
                   "to our brand blue. Otherwise, ship it!",
        sender="designer@company.com",
        timestamp="2026-03-31T15:00:00Z",
        has_attachments=True,
        thread_length=5,
        true_category="important",
        true_priority=3,
        expected_reply_keywords=["changes", "update", "version"],
    ),
]

MEDIUM_CONFIG = TaskConfig(
    name="medium",
    description="Ambiguous emails that require reasoning to classify. "
                "Mix of promotional, personal, and professional messages.",
    max_steps=8,
    emails=MEDIUM_EMAILS,
    classification_weight=0.40,
    reply_weight=0.30,
    priority_weight=0.20,
    efficiency_weight=0.10,
)
