"""
NyayaSetu — Timeline Predictor
Estimates case duration and milestones based on case type.
"""

from .embedding_model import detect_legal_category


# Timeline templates by legal category
TIMELINE_TEMPLATES = {
    "labour": {
        "duration": "4-6 months",
        "nodes": [
            {"label": "Pre-Litigation", "time": "Month 1-2", "active": True, "done": True},
            {"label": "Legal Notice", "time": "Month 2-3", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 4-6", "active": False, "done": False},
        ]
    },
    "property": {
        "duration": "6-10 months",
        "nodes": [
            {"label": "Title Verification", "time": "Month 1-2", "active": True, "done": True},
            {"label": "Legal Notice", "time": "Month 2-4", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 6-10", "active": False, "done": False},
        ]
    },
    "criminal": {
        "duration": "3-6 months",
        "nodes": [
            {"label": "FIR/Complaint", "time": "Day 1-7", "active": True, "done": True},
            {"label": "Investigation", "time": "Month 1-3", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 3-6", "active": False, "done": False},
        ]
    },
    "family": {
        "duration": "3-6 months",
        "nodes": [
            {"label": "Counseling", "time": "Month 1-2", "active": True, "done": True},
            {"label": "Petition Filing", "time": "Month 2-3", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 3-6", "active": False, "done": False},
        ]
    },
    "consumer": {
        "duration": "3-6 months",
        "nodes": [
            {"label": "Complaint Draft", "time": "Week 1-2", "active": True, "done": True},
            {"label": "Forum Filing", "time": "Month 1", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 3-6", "active": False, "done": False},
        ]
    },
    "constitutional": {
        "duration": "2-4 months",
        "nodes": [
            {"label": "Petition Drafting", "time": "Week 1-4", "active": True, "done": True},
            {"label": "Filing", "time": "Month 1-2", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 2-4", "active": False, "done": False},
        ]
    },
    "cyber": {
        "duration": "3-6 months",
        "nodes": [
            {"label": "Cyber Cell Complaint", "time": "Day 1-7", "active": True, "done": True},
            {"label": "Investigation", "time": "Month 1-3", "active": True, "done": False},
            {"label": "First Hearing", "time": "Month 3-6", "active": False, "done": False},
        ]
    },
}

DEFAULT_TIMELINE = {
    "duration": "4-8 months",
    "nodes": [
        {"label": "Consultation", "time": "Week 1-2", "active": True, "done": True},
        {"label": "Legal Notice", "time": "Month 1-2", "active": True, "done": False},
        {"label": "First Hearing", "time": "Month 4-8", "active": False, "done": False},
    ]
}


def predict_timeline(case_description: str) -> dict:
    """
    Predict estimated timeline for a legal case.
    Returns timeline nodes with duration estimate.
    """
    category_info = detect_legal_category(case_description)
    category = category_info["primary_category"]

    template = TIMELINE_TEMPLATES.get(category, DEFAULT_TIMELINE)

    return {
        "estimated_duration": template["duration"],
        "nodes": template["nodes"],
        "category": category,
        "note": f"Timeline based on typical {category.title()} cases in Indian courts. Actual duration may vary based on court workload and case complexity."
    }
