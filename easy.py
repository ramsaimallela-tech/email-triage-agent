EASY_CONFIG = {
    "max_steps": 5,
    "reward_weights": {"classification": 0.50, "reply": 0.20, "priority": 0.20, "efficiency": 0.10},
    "emails": [
        {"subject": "URGENT: Server down", "email_text": "Production is down. Fix now.", "sender": "ops@company.com", "timestamp": "2026-04-05T08:00:00Z", "true_category": "important", "true_priority": 1},
        {"subject": "Buy cheap meds now!!!", "email_text": "Click here for discounts!", "sender": "promo@spam.net", "timestamp": "2026-04-05T08:05:00Z", "true_category": "spam", "true_priority": 5},
        {"subject": "Team lunch Thursday", "email_text": "Lunch at noon. RSVP.", "sender": "hr@company.com", "timestamp": "2026-04-05T08:10:00Z", "true_category": "normal", "true_priority": 3},
        {"subject": "Invoice #1023 overdue", "email_text": "Please pay the invoice.", "sender": "billing@vendor.com", "timestamp": "2026-04-05T08:15:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "Weekly newsletter", "email_text": "Here are this week's updates.", "sender": "news@digest.com", "timestamp": "2026-04-05T08:20:00Z", "true_category": "normal", "true_priority": 4},
    ],
}
