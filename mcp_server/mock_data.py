CARDS = {
    "user_001": {
        "customer_id": "user_001",
        "last_four": "4821",
        "status": "active",
        "replacement_status": "not_requested",
        "estimated_delivery": None,
    },
    "user_002": {
        "customer_id": "user_002",
        "last_four": "1934",
        "status": "replacement_in_transit",
        "replacement_status": "shipped",
        "estimated_delivery": "2026-10-06",
    },
    "user_003": {
        "customer_id": "user_003",
        "last_four": "7750",
        "status": "blocked",
        "replacement_status": "processing",
        "estimated_delivery": "2026-10-09",
    },
}


CARD_PROCEDURES = {
    "lost": {
        "issue": "lost",
        "title": "Lost card procedure",
        "steps": [
            "Temporarily freeze the card using the mobile banking application.",
            "Check recent transactions for anything you do not recognize.",
            "Contact banking support if you cannot find the card.",
            "Request a replacement card if necessary.",
        ],
        "emergency_contact": "+995 32 2 00 00 00",
    },
    "stolen": {
        "issue": "stolen",
        "title": "Stolen card procedure",
        "steps": [
            "Freeze the card immediately.",
            "Review recent transactions for unauthorized activity.",
            "Contact banking support immediately.",
            "Request permanent cancellation and a replacement card.",
        ],
        "emergency_contact": "+995 32 2 00 00 00",
    },
}