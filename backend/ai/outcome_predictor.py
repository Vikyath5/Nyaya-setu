"""
NyayaSetu — Outcome Predictor
Predicts likely legal outcomes based on case analysis.
"""

from .embedding_model import detect_legal_category, assess_evidence_strength, normalize_text


# Base outcome distributions by legal category
OUTCOME_BASELINES = {
    "labour": {"settlement": 55, "court_win": 25, "dismissed": 12, "court_loss": 8},
    "property": {"settlement": 35, "court_win": 30, "dismissed": 20, "court_loss": 15},
    "criminal": {"settlement": 15, "court_win": 35, "dismissed": 30, "court_loss": 20},
    "family": {"settlement": 50, "court_win": 20, "dismissed": 15, "court_loss": 15},
    "consumer": {"settlement": 45, "court_win": 30, "dismissed": 15, "court_loss": 10},
    "constitutional": {"settlement": 10, "court_win": 40, "dismissed": 35, "court_loss": 15},
    "cyber": {"settlement": 25, "court_win": 30, "dismissed": 30, "court_loss": 15},
}

DEFAULT_BASELINE = {"settlement": 40, "court_win": 25, "dismissed": 20, "court_loss": 15}

# Recommendations by dominant outcome
RECOMMENDATIONS = {
    "settlement": "High viability for Pre-Litigation Mediation. Settlement probability is significantly higher than court verdict outcomes.",
    "court_win": "Strong case for litigation. Evidence and legal provisions favor a positive court verdict.",
    "dismissed": "Case may face challenges. Consider strengthening evidence and documentation before proceeding.",
    "court_loss": "Case requires significant strengthening. Consult a specialized lawyer for detailed advice.",
}


def predict_outcome(case_description: str, case_strength_score: int = 50) -> dict:
    """
    Predict legal outcome probabilities based on case description and strength.
    Returns outcome percentages and recommendation.
    """
    category_info = detect_legal_category(case_description)
    evidence = assess_evidence_strength(case_description)
    category = category_info["primary_category"]

    # Get baseline for the detected category
    baseline = OUTCOME_BASELINES.get(category, DEFAULT_BASELINE).copy()

    # Adjust based on case strength
    strength_modifier = (case_strength_score - 50) / 100

    if strength_modifier > 0:
        # Stronger case: increase settlement and court_win
        baseline["settlement"] += int(strength_modifier * 20)
        baseline["court_win"] += int(strength_modifier * 10)
        baseline["dismissed"] -= int(strength_modifier * 15)
        baseline["court_loss"] -= int(strength_modifier * 15)
    else:
        # Weaker case: increase dismissed and court_loss
        baseline["dismissed"] += int(abs(strength_modifier) * 15)
        baseline["court_loss"] += int(abs(strength_modifier) * 10)
        baseline["settlement"] -= int(abs(strength_modifier) * 15)
        baseline["court_win"] -= int(abs(strength_modifier) * 10)

    # Evidence-based adjustments
    if evidence["strength"] == "strong":
        baseline["court_win"] += 5
        baseline["dismissed"] -= 5
    elif evidence["strength"] == "weak":
        baseline["dismissed"] += 5
        baseline["court_win"] -= 5

    # Clamp values
    for key in baseline:
        baseline[key] = max(baseline[key], 2)

    # Normalize to 100%
    total = sum(baseline.values())
    for key in baseline:
        baseline[key] = round(baseline[key] / total * 100)

    # Adjust rounding error
    diff = 100 - sum(baseline.values())
    dominant = max(baseline, key=baseline.get)
    baseline[dominant] += diff

    # Determine dominant outcome
    dominant_outcome = max(baseline, key=baseline.get)
    recommendation = RECOMMENDATIONS.get(dominant_outcome, RECOMMENDATIONS["settlement"])

    return {
        "outcomes": [
            {"label": "Settlement", "percentage": baseline["settlement"], "color": "var(--semantic-positive)"},
            {"label": "Court Win", "percentage": baseline["court_win"], "color": "var(--accent-primary)"},
            {"label": "Dismissed", "percentage": baseline["dismissed"], "color": "var(--text-tertiary)"},
            {"label": "Court Loss", "percentage": baseline["court_loss"], "color": "var(--semantic-warning)"},
        ],
        "dominant_outcome": dominant_outcome,
        "recommendation": recommendation,
        "confidence": "moderate" if case_strength_score >= 45 else "low"
    }
