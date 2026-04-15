"""
test_scenarios.py — 10 unique (Intent, Key Facts, Tone) scenarios
with human-written reference emails.
"""

SCENARIOS = [
    # ── Scenario 1 ───────────────────────────────────────────────────
    {
        "id": 1,
        "intent": "Follow up after a sales meeting",
        "key_facts": (
            "Met on June 5 at the client's Chicago office; "
            "discussed the Enterprise Analytics platform; "
            "client requested a custom demo by June 20; "
            "primary contact is VP of Data, Priya Sharma"
        ),
        "tone": "Professional and friendly",
        "reference_email": (
            "Subject: Great Meeting on June 5 — Next Steps\n\n"
            "Hi Priya,\n\n"
            "Thank you for taking the time to meet with us at your Chicago "
            "office on June 5. It was a pleasure discussing how our Enterprise "
            "Analytics platform can support your team's goals.\n\n"
            "As promised, we are preparing a custom demo tailored to your "
            "requirements and will have it ready for you by June 20. I will "
            "send over a calendar invite shortly so we can walk through it "
            "together.\n\n"
            "Please don't hesitate to reach out if any questions come up in "
            "the meantime.\n\n"
            "Best regards,\n[Your Name]"
        ),
    },
    # ── Scenario 2 ───────────────────────────────────────────────────
    {
        "id": 2,
        "intent": "Request for proposal details from a vendor",
        "key_facts": (
            "Project is a new warehouse management system; "
            "budget cap is \$500K; "
            "proposal deadline is August 1; "
            "vendor must include SLA terms and implementation timeline"
        ),
        "tone": "Formal",
        "reference_email": (
            "Subject: Request for Proposal — Warehouse Management System\n\n"
            "Dear Vendor Team,\n\n"
            "We are currently evaluating solutions for a new warehouse "
            "management system and would like to invite you to submit a "
            "proposal. Our budget for this project is capped at \$500,000.\n\n"
            "Please ensure your proposal includes detailed SLA terms and a "
            "comprehensive implementation timeline. All submissions must be "
            "received no later than August 1.\n\n"
            "Should you require additional information about our "
            "requirements, please do not hesitate to contact us.\n\n"
            "Sincerely,\n[Your Name]"
        ),
    },
    # ── Scenario 3 ───────────────────────────────────────────────────
    {
        "id": 3,
        "intent": "Apologize for a delayed shipment",
        "key_facts": (
            "Order #88421 was due on May 28; "
            "delay caused by supplier shortage; "
            "new estimated delivery is June 8; "
            "offering a 15% discount on next order as compensation"
        ),
        "tone": "Empathetic and apologetic",
        "reference_email": (
            "Subject: Sincere Apologies for the Delay on Order #88421\n\n"
            "Dear Customer,\n\n"
            "I sincerely apologize for the delay in delivering your order "
            "#88421, which was originally due on May 28. Unfortunately, an "
            "unexpected supplier shortage impacted our fulfillment "
            "schedule.\n\n"
            "We have expedited processing and your updated delivery estimate "
            "is June 8. To express our regret, we would like to offer you a "
            "15% discount on your next order.\n\n"
            "We truly value your patience and your business. Please reach "
            "out if there is anything else we can do.\n\n"
            "With sincere apologies,\n[Your Name]"
        ),
    },
    # ── Scenario 4 ───────────────────────────────────────────────────
    {
        "id": 4,
        "intent": "Announce an internal policy change",
        "key_facts": (
            "New remote-work policy effective July 1; "
            "employees may work from home up to 3 days per week; "
            "manager approval required for fully remote arrangements; "
            "updated policy document available on the HR portal"
        ),
        "tone": "Informative and neutral",
        "reference_email": (
            "Subject: Updated Remote-Work Policy — Effective July 1\n\n"
            "Dear Team,\n\n"
            "I am writing to inform you of an update to our remote-work "
            "policy, effective July 1. Under the new guidelines, employees "
            "may work from home up to three days per week.\n\n"
            "Fully remote arrangements will require prior manager approval. "
            "The complete policy document is now available on the HR "
            "portal for your review.\n\n"
            "If you have questions, please reach out to your manager or the "
            "HR team.\n\n"
            "Thank you,\n[Your Name]"
        ),
    },
    # ── Scenario 5 ───────────────────────────────────────────────────
    {
        "id": 5,
        "intent": "Invite a speaker to a company conference",
        "key_facts": (
            "Conference name: Innovate 2025; "
            "date is October 14–15 in Austin, TX; "
            "keynote slot is 45 minutes; "
            "honorarium of \$5,000 plus travel covered"
        ),
        "tone": "Warm and persuasive",
        "reference_email": (
            "Subject: Speaking Invitation — Innovate 2025\n\n"
            "Dear Dr. [Last Name],\n\n"
            "We would be honored to have you deliver a keynote address at "
            "Innovate 2025, our flagship conference taking place October "
            "14–15 in Austin, TX.\n\n"
            "The keynote slot is 45 minutes, and we are offering an "
            "honorarium of \$5,000, with all travel expenses covered. Your "
            "insights would be an incredible addition to the event.\n\n"
            "We truly hope you will consider this invitation and would be "
            "happy to discuss any details. Looking forward to hearing from "
            "you!\n\n"
            "Warmly,\n[Your Name]"
        ),
    },
    # ── Scenario 6 ───────────────────────────────────────────────────
    {
        "id": 6,
        "intent": "Urgent request to reschedule a board meeting",
        "key_facts": (
            "Original date was July 22; "
            "CEO is unavailable due to emergency travel; "
            "proposed new date is July 29; "
            "agenda remains unchanged"
        ),
        "tone": "Urgent and respectful",
        "reference_email": (
            "Subject: URGENT — Board Meeting Rescheduled to July 29\n\n"
            "Dear Board Members,\n\n"
            "I am writing to inform you that the board meeting originally "
            "scheduled for July 22 must be rescheduled. Due to emergency "
            "travel obligations, our CEO will be unavailable on that "
            "date.\n\n"
            "We propose moving the meeting to July 29. The agenda will "
            "remain unchanged. Please confirm your availability at your "
            "earliest convenience so we can finalize logistics.\n\n"
            "Thank you for your understanding and flexibility.\n\n"
            "Regards,\n[Your Name]"
        ),
    },
    # ── Scenario 7 ───────────────────────────────────────────────────
    {
        "id": 7,
        "intent": "Welcome a new team member",
        "key_facts": (
            "New hire is Alex Kim, Senior Software Engineer; "
            "starting on Monday, August 12; "
            "will be on the Platform Infrastructure team; "
            "buddy/mentor is Jessica Tran"
        ),
        "tone": "Casual and enthusiastic",
        "reference_email": (
            "Subject: Welcome to the Team, Alex!\n\n"
            "Hey everyone,\n\n"
            "I'm excited to let you know that Alex Kim will be joining us "
            "as a Senior Software Engineer on the Platform Infrastructure "
            "team starting Monday, August 12!\n\n"
            "Jessica Tran will be Alex's buddy and mentor, so please help "
            "make the first few weeks awesome. Feel free to swing by and "
            "say hello.\n\n"
            "Let's give Alex a warm welcome!\n\n"
            "Cheers,\n[Your Name]"
        ),
    },
    # ── Scenario 8 ───────────────────────────────────────────────────
    {
        "id": 8,
        "intent": "Decline a partnership proposal politely",
        "key_facts": (
            "Proposal was for co-branded marketing campaign; "
            "does not align with current brand strategy; "
            "open to revisiting in Q1 next year; "
            "appreciate the detailed proposal they sent"
        ),
        "tone": "Polite and diplomatic",
        "reference_email": (
            "Subject: Re: Co-Branded Marketing Campaign Proposal\n\n"
            "Dear [Name],\n\n"
            "Thank you for taking the time to put together such a detailed "
            "proposal for a co-branded marketing campaign. We genuinely "
            "appreciate the thought and effort behind it.\n\n"
            "After careful review, we have determined that the initiative "
            "does not align with our current brand strategy. That said, we "
            "would be very open to revisiting this conversation in Q1 of "
            "next year as our priorities evolve.\n\n"
            "We value the relationship and look forward to potential "
            "collaboration in the future.\n\n"
            "Kind regards,\n[Your Name]"
        ),
    },
    # ── Scenario 9 ───────────────────────────────────────────────────
    {
        "id": 9,
        "intent": "Notify customers of scheduled system maintenance",
        "key_facts": (
            "Maintenance window: Saturday, September 6, 2:00–6:00 AM EST; "
            "services affected: payment processing and order tracking; "
            "expected downtime is up to 2 hours; "
            "no action required from customers"
        ),
        "tone": "Clear and reassuring",
        "reference_email": (
            "Subject: Scheduled Maintenance — September 6\n\n"
            "Dear Valued Customer,\n\n"
            "We want to let you know about a scheduled maintenance window "
            "on Saturday, September 6, from 2:00 AM to 6:00 AM EST. During "
            "this period, payment processing and order tracking may be "
            "temporarily unavailable for up to 2 hours.\n\n"
            "No action is required on your part. Our team will be working "
            "to complete the maintenance as quickly as possible to minimize "
            "any disruption.\n\n"
            "Thank you for your understanding.\n\n"
            "Best,\n[Your Name]"
        ),
    },
    # ── Scenario 10 ──────────────────────────────────────────────────
    {
        "id": 10,
        "intent": "Request feedback on a draft report from a colleague",
        "key_facts": (
            "Report title: 2024 Sustainability Impact Assessment; "
            "deadline for feedback is Friday, June 14; "
            "focus areas: data accuracy in Section 3 and clarity of "
            "executive summary; "
            "report is attached as a PDF"
        ),
        "tone": "Collegial and concise",
        "reference_email": (
            "Subject: Feedback Request — 2024 Sustainability Impact "
            "Assessment\n\n"
            "Hi [Name],\n\n"
            "I have attached the draft of our 2024 Sustainability Impact "
            "Assessment and would greatly appreciate your feedback. In "
            "particular, I'd love your thoughts on the data accuracy in "
            "Section 3 and the clarity of the executive summary.\n\n"
            "Could you share your comments by Friday, June 14? The report "
            "is attached as a PDF for your convenience.\n\n"
            "Thanks in advance!\n\n"
            "Best,\n[Your Name]"
        ),
    },
]
