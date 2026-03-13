"""Rule-based case strength analyzer for NyayaSetu backend.

This module is designed to be imported by API routes and services:
    from ai.case_strength_analyzer import analyze_case_strength

The output is JSON-serializable so it can be returned directly from FastAPI.
"""

from __future__ import annotations


def _detect_case_type(text: str) -> str:
    """Infer case type from simple keyword patterns."""
    case_type_rules = [
        ("Labour Dispute", ["salary", "wage", "employer", "termination", "workplace"]),
        ("Property Dispute", ["property", "land", "ownership", "title", "possession"]),
        ("Cheque Dispute", ["cheque", "bounced", "dishonour", "dishonored"]),
        ("Cyber Dispute", ["cyber", "hacking", "online scam", "phishing", "otp fraud"]),
        ("Family Dispute", ["divorce", "marriage", "custody", "maintenance", "alimony"]),
        ("Criminal Dispute", ["assault", "theft", "extortion", "criminal", "fir", "arrest"]),
    ]

    for case_type, keywords in case_type_rules:
        if any(keyword in text for keyword in keywords):
            return case_type
    return "General Dispute"


def _estimate_complexity(case_type: str, score: float) -> str:
    """Estimate complexity from case type and evidence quality."""
    lower = case_type.lower()

    if any(label in lower for label in ("cyber", "criminal", "cheque")):
        return "High"
    if "property" in lower:
        return "Medium"
    if "labour" in lower:
        # Labour disputes are generally lower complexity when evidence is strong.
        return "Low" if score >= 0.6 else "Medium"
    if "family" in lower:
        return "Medium"
    return "Medium"


def _recommended_actions(case_type: str, missing_evidence: list[str]) -> list[str]:
    """Return practical next steps tailored to the case category."""
    lower = case_type.lower()

    if "labour" in lower:
        actions = [
            "Send a written demand notice to the employer for unpaid dues.",
            "File a complaint with the Labour Commissioner.",
            "Proceed to Labour Court if conciliation fails.",
        ]
    elif "property" in lower:
        actions = [
            "Collect title and ownership documents.",
            "Send a legal notice to the opposite party.",
            "File a civil suit and seek injunction if needed.",
        ]
    elif "cheque" in lower:
        actions = [
            "Send statutory legal notice after cheque bounce.",
            "File a complaint under the Negotiable Instruments Act timeline.",
            "Preserve bank memo and payment records.",
        ]
    elif "cyber" in lower:
        actions = [
            "File complaint on the National Cyber Crime Portal.",
            "Report to local Cyber Crime Cell and register FIR if needed.",
            "Preserve screenshots, transaction IDs, and communication logs.",
        ]
    elif "family" in lower:
        actions = [
            "Consult a family lawyer for rights and remedies.",
            "Try mediation where appropriate.",
            "File petition in Family Court if settlement fails.",
        ]
    elif "criminal" in lower:
        actions = [
            "File or follow up on FIR with full incident details.",
            "Collect witness details and any digital/physical proof.",
            "Coordinate with a criminal lawyer for court steps.",
        ]
    else:
        actions = [
            "Consult a lawyer to identify the correct legal forum.",
            "Prepare a documented timeline of events.",
            "Issue legal notice before formal filing where applicable.",
        ]

    if missing_evidence:
        actions.append(
            "Gather missing evidence before filing: " + ", ".join(missing_evidence) + "."
        )

    return actions


def analyze_case_strength(case_text: str) -> dict:
    """Analyze case strength using evidence- and keyword-based rules.

    How scoring works:
    - Evidence presence increases score because proof supports legal claims.
    - Missing key evidence decreases score because unsupported claims carry risk.
    - Final score is bounded to [0.0, 1.0] for consistent downstream usage.
    """
    if not isinstance(case_text, str):
        raise TypeError("case_text must be a string")

    normalized_text = case_text.strip().lower()
    if not normalized_text:
        raise ValueError("case_text must be a non-empty string")

    case_type = _detect_case_type(normalized_text)

    evidence_keywords: dict[str, list[str]] = {
        "contract": ["contract", "employment contract", "signed contract"],
        "agreement": ["agreement", "written agreement", "signed agreement"],
        "witness": ["witness", "witnesses"],
        "email": ["email", "mail thread", "email proof"],
        "payment proof": ["payment proof", "bank statement", "bank records", "salary slip", "receipt"],
        "message": ["message", "sms", "whatsapp", "chat"],
        "recording": ["recording", "audio recording", "call recording", "video recording"],
    }

    detected_evidence: list[str] = []
    for evidence_name, terms in evidence_keywords.items():
        if any(term in normalized_text for term in terms):
            detected_evidence.append(evidence_name)

    all_evidence_keys = list(evidence_keywords.keys())
    missing_evidence = [key for key in all_evidence_keys if key not in detected_evidence]

    # Rule-based score: start from neutral baseline, add evidence boosts,
    # then subtract penalties for missing support documents.
    score = 0.35

    strong_evidence_weights = {
        "contract": 0.15,
        "agreement": 0.1,
        "witness": 0.1,
        "email": 0.08,
        "payment proof": 0.2,
        "message": 0.07,
        "recording": 0.1,
    }

    for item in detected_evidence:
        score += strong_evidence_weights[item]

    # Penalize absent evidence with slightly smaller weight than positive signal
    # to avoid overly punishing users who describe cases briefly.
    missing_penalty_weights = {
        "contract": 0.06,
        "agreement": 0.04,
        "witness": 0.04,
        "email": 0.03,
        "payment proof": 0.08,
        "message": 0.03,
        "recording": 0.03,
    }

    for item in missing_evidence:
        score -= missing_penalty_weights[item]

    score = round(max(0.0, min(1.0, score)), 2)

    if score >= 0.7:
        case_strength = "Strong"
        success_rate = "70-90%"
    elif score >= 0.4:
        case_strength = "Moderate"
        success_rate = "40-70%"
    else:
        case_strength = "Weak"
        success_rate = "10-40%"

    legal_complexity = _estimate_complexity(case_type, score)

    if case_strength == "Strong":
        estimated_resolution_time = "6-12 months"
    elif case_strength == "Moderate":
        estimated_resolution_time = "12-24 months"
    else:
        estimated_resolution_time = "18-36 months"

    # Risk probability is the inverse of strength score, adjusted slightly by
    # complexity since high-complexity cases often have procedural uncertainty.
    complexity_risk_adjustment = {"Low": 0.0, "Medium": 0.05, "High": 0.1}
    risk_probability = 1.0 - score + complexity_risk_adjustment[legal_complexity]
    risk_probability = round(max(0.0, min(1.0, risk_probability)), 2)

    recommended_actions = _recommended_actions(case_type, missing_evidence)

    return {
        "case_type": case_type,
        "case_strength": case_strength,
        "score": score,
        "success_rate": success_rate,
        "legal_complexity": legal_complexity,
        "estimated_resolution_time": estimated_resolution_time,
        "risk_probability": risk_probability,
        "key_evidence_detected": detected_evidence,
        "missing_evidence": missing_evidence,
        "recommended_actions": recommended_actions,
    }


if __name__ == "__main__":
    case = (
        "My employer has not paid my salary for three months. "
        "I have salary slips, email messages, and bank records as payment proof."
    )

    result = analyze_case_strength(case)

    print("Case Strength Analysis:")
    print(result)
