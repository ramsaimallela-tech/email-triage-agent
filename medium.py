MEDIUM_CONFIG = {
    "max_steps": 8,
    "reward_weights": {"classification": 0.40, "reply": 0.30, "priority": 0.20, "efficiency": 0.10},
    "emails": [
        {"subject": "Question about last meeting", "email_text": "Could we revisit the budget discussion?", "sender": "manager@company.com", "timestamp": "2026-04-05T09:00:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "FWD: Opportunity", "email_text": "You have been selected for an exclusive offer.", "sender": "deals@offers.co", "timestamp": "2026-04-05T09:05:00Z", "true_category": "spam", "true_priority": 5},
        {"subject": "Update on project X", "email_text": "The timeline has shifted slightly.", "sender": "dev@company.com", "timestamp": "2026-04-05T09:10:00Z", "true_category": "normal", "true_priority": 3},
        {"subject": "Security alert", "email_text": "Unusual login detected on your account.", "sender": "security@company.com", "timestamp": "2026-04-05T09:15:00Z", "true_category": "important", "true_priority": 1},
        {"subject": "Re: feedback", "email_text": "Thanks for the review, I will apply the changes.", "sender": "intern@company.com", "timestamp": "2026-04-05T09:20:00Z", "true_category": "normal", "true_priority": 4},
        {"subject": "Lottery winner!", "email_text": "Claim your prize now.", "sender": "prize@scam.biz", "timestamp": "2026-04-05T09:25:00Z", "true_category": "spam", "true_priority": 5},
        {"subject": "Contract renewal", "email_text": "Please review and sign by Friday.", "sender": "legal@partner.com", "timestamp": "2026-04-05T09:30:00Z", "true_category": "important", "true_priority": 2},
        {"subject": "Office closed Monday", "email_text": "Reminder: public holiday on Monday.", "sender": "admin@company.com", "timestamp": "2026-04-05T09:35:00Z", "true_category": "normal", "true_priority": 4},
    ],
}
