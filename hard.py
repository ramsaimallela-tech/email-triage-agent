HARD_CONFIG = {
    "max_steps": 12,
    "reward_weights": {"classification": 0.35, "reply": 0.35, "priority": 0.20, "efficiency": 0.10},
    "emails": [
        {"subject": "Re: Re: Re: Project Alpha", "email_text": "Following up on last week's thread — please confirm the deliverable dates.", "sender": "cto@bigclient.com", "timestamp": "2026-04-05T10:00:00Z", "true_category": "important", "true_priority": 1},
        {"subject": "You may have won", "email_text": "Exclusive member offer inside.", "sender": "offers@prize-hub.net", "timestamp": "2026-04-05T10:05:00Z", "true_category": "spam", "true_priority": 5},
        {"subject": "Thoughts on the proposal?", "email_text": "Wanted your informal take before the board meeting.", "sender": "ceo@company.com", "timestamp": "2026-04-05T10:10:00Z", "true_category": "important", "true_priority": 1},
        {"subject": "Updated roadmap v3", "email_text": "Attached is the latest product roadmap for Q3.", "sender": "pm@company.com", "timestamp": "2026-04-05T10:15:00Z", "true_category": "normal", "true_priority": 3, "has_attachments": True},
        {"subject": "Payment failed", "email_text": "Your subscription payment could not be processed.", "sender": "billing@saas.io", "timestamp": "2026-04-05T10:20:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "Unsubscribe confirmation", "email_text": "You have been removed from our list.", "sender": "no-reply@newsletter.com", "timestamp": "2026-04-05T10:25:00Z", "true_category": "normal", "true_priority": 5},
        {"subject": "Incident report", "email_text": "Full post-mortem attached after last night's outage.", "sender": "sre@company.com", "timestamp": "2026-04-05T10:30:00Z", "true_category": "important", "true_priority": 1, "has_attachments": True},
        {"subject": "Cheap software licences", "email_text": "Get MS Office for $5. Limited time.", "sender": "deals@softwarepirate.ru", "timestamp": "2026-04-05T10:35:00Z", "true_category": "spam", "true_priority": 5},
        {"subject": "Team building event", "email_text": "Join us for go-karting next Friday!", "sender": "culture@company.com", "timestamp": "2026-04-05T10:40:00Z", "true_category": "normal", "true_priority": 4},
        {"subject": "NDA required before call", "email_text": "Please sign before our Wednesday discussion.", "sender": "legal@enterprise.com", "timestamp": "2026-04-05T10:45:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "Phishing test results", "email_text": "30% of staff clicked the simulated phishing link.", "sender": "security@company.com", "timestamp": "2026-04-05T10:50:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "Daily standup notes", "email_text": "Notes from today's 10-minute standup attached.", "sender": "scrum@company.com", "timestamp": "2026-04-05T10:55:00Z", "true_category": "normal", "true_priority": 4},
    ],
}
