"""Hard task — complex multi-context emails with nuanced replies."""

from env.models import Email, TaskConfig

HARD_EMAILS = [
    Email(
        email_id=201,
        subject="Re: Partnership proposal — legal review needed",
        email_text="Hi, following our call last week, the partnership terms have "
                   "changed. Their legal team wants a non-compete clause (Section 4.2) "
                   "and a revised revenue-sharing model (60-40 instead of 50-50). "
                   "We need our legal counsel to review before the Thursday deadline. "
                   "Also, the CEO wants a briefing doc by Wednesday EOD.",
        sender="bizdev@company.com",
        timestamp="2026-03-31T09:00:00Z",
        has_attachments=True,
        thread_length=7,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["legal", "review", "deadline", "thursday", "brief", "revenue"],
    ),
    Email(
        email_id=202,
        subject="Urgent: API rate limits exceeded",
        email_text="Our monitoring detected that API rate limits have been exceeded "
                   "by 300% since 2 AM. Investigation shows a retry loop in the "
                   "payment service (commit abc123). The vendor may throttle us "
                   "permanently if not resolved. Infra team is on standby.",
        sender="sre@company.com",
        timestamp="2026-03-31T06:00:00Z",
        has_attachments=False,
        thread_length=4,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["investigate", "fix", "retry", "payment", "throttle"],
    ),
    Email(
        email_id=203,
        subject="Job opportunity — Senior AI Engineer at TechCorp",
        email_text="Hi, I came across your profile and was impressed by your work. "
                   "We have an opening for a Senior AI Engineer. The role offers "
                   "competitive compensation, fully remote, and a chance to lead "
                   "our LLM research team. Would you be open to a brief chat?",
        sender="recruiter@techcorp.com",
        timestamp="2026-03-31T10:30:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=3,
        expected_reply_keywords=["interest", "opportunity", "discuss"],
    ),
    Email(
        email_id=204,
        subject="Re: Customer escalation — Enterprise client threatening churn",
        email_text="The enterprise client (Acme Corp, $2M ARR) has escalated again. "
                   "Their CTO says the integration bugs we promised to fix 3 sprints "
                   "ago are still present. They've given us until end of month or "
                   "they're switching to a competitor. Support ticket: #ESC-4492. "
                   "Can we get engineering priority on this?",
        sender="cs-lead@company.com",
        timestamp="2026-03-31T11:00:00Z",
        has_attachments=True,
        thread_length=9,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["priority", "engineering", "fix", "client", "escalation"],
    ),
    Email(
        email_id=205,
        subject="Your cloud storage is 95% full",
        email_text="You're running low on storage. Current usage: 95% of 2TB. "
                   "Upgrade to our business plan for 10TB at a special rate, or "
                   "manage your files to free up space. Files older than 1 year "
                   "can be archived automatically.",
        sender="noreply@cloud-storage.com",
        timestamp="2026-03-31T07:30:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=3,
        expected_reply_keywords=["storage", "archive", "manage"],
    ),
    Email(
        email_id=206,
        subject="Act now — Limited time crypto investment opportunity",
        email_text="Don't miss out! Our AI-powered crypto trading bot has generated "
                   "500% returns in 30 days. Join 10,000+ investors making passive "
                   "income. Minimum investment just $100. Sign up with your wallet "
                   "address and start earning today. No experience needed.",
        sender="invest@crypto-gains-pro.xyz",
        timestamp="2026-03-31T05:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="spam",
        true_priority=5,
        expected_reply_keywords=[],
    ),
    Email(
        email_id=207,
        subject="Board meeting prep — confidential",
        email_text="Attached are the board deck slides for next Tuesday. Please "
                   "review slides 12-18 (financial projections) and slides 22-25 "
                   "(headcount plan). The CFO flagged two numbers that don't match "
                   "— see highlighted cells in the spreadsheet. We need corrected "
                   "figures by Monday morning.",
        sender="ea-to-ceo@company.com",
        timestamp="2026-03-31T17:00:00Z",
        has_attachments=True,
        thread_length=3,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["review", "slides", "figures", "monday", "correct"],
    ),
    Email(
        email_id=208,
        subject="Re: Open-source contribution — PR feedback",
        email_text="Thanks for your PR! A few comments: 1) The test coverage dropped "
                   "by 2%, please add tests for the edge cases. 2) The function naming "
                   "doesn't follow our conventions (snake_case). 3) Great improvement "
                   "on the algorithm — the benchmarks look solid. Please address #1 "
                   "and #2 and I'll merge.",
        sender="maintainer@oss-project.org",
        timestamp="2026-03-31T14:00:00Z",
        has_attachments=False,
        thread_length=4,
        true_category="normal",
        true_priority=3,
        expected_reply_keywords=["tests", "naming", "update", "address"],
    ),
    Email(
        email_id=209,
        subject="Security alert: Unusual login attempt",
        email_text="We detected a login attempt from an unrecognised device in a "
                   "new location (Lagos, Nigeria). If this was you, no action needed. "
                   "If not, please secure your account immediately by changing your "
                   "password and enabling 2FA. Incident ID: SEC-20260331-001.",
        sender="security@company.com",
        timestamp="2026-03-31T04:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="important",
        true_priority=1,
        expected_reply_keywords=["secure", "password", "2fa", "investigate"],
    ),
    Email(
        email_id=210,
        subject="Win a free vacation! Complete our survey",
        email_text="Complete this 2-minute survey and get a chance to win an "
                   "all-expenses-paid vacation to the Maldives! Over 50,000 "
                   "participants. Don't wait — survey closes in 48 hours. "
                   "Click the link below to start.",
        sender="survey@reward-surveys.net",
        timestamp="2026-03-31T12:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="spam",
        true_priority=5,
        expected_reply_keywords=[],
    ),
    Email(
        email_id=211,
        subject="Re: Vendor contract renewal — negotiation update",
        email_text="The vendor came back with a 15% price increase for next year. "
                   "I've pushed back and proposed capping it at 5%. They're willing "
                   "to meet at 8% if we commit to a 2-year term. The current "
                   "contract expires in 6 weeks. We need Finance and Legal sign-off "
                   "before I can respond. Thoughts?",
        sender="procurement@company.com",
        timestamp="2026-03-31T13:00:00Z",
        has_attachments=True,
        thread_length=6,
        true_category="important",
        true_priority=2,
        expected_reply_keywords=["negotiate", "price", "contract", "finance", "legal"],
    ),
    Email(
        email_id=212,
        subject="Reminder: Health insurance enrollment ends Friday",
        email_text="This is a reminder that open enrollment for health insurance "
                   "closes this Friday at 5 PM. If you haven't made your selection, "
                   "please log in to the benefits portal. Changes made after the "
                   "deadline will not take effect until the next enrollment period.",
        sender="benefits@company.com",
        timestamp="2026-03-31T08:00:00Z",
        has_attachments=False,
        thread_length=1,
        true_category="normal",
        true_priority=2,
        expected_reply_keywords=["enrollment", "benefits"],
    ),
]

HARD_CONFIG = TaskConfig(
    name="hard",
    description="Complex multi-context emails requiring nuanced classification, "
                "accurate prioritisation, and high-quality replies. Strict scoring.",
    max_steps=12,
    emails=HARD_EMAILS,
    classification_weight=0.35,
    reply_weight=0.35,
    priority_weight=0.20,
    efficiency_weight=0.10,
)
