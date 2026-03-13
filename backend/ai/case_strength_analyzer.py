"""
Rule-based case strength analyzer for NyayaSetu backend.

This module evaluates the strength of a legal case based on evidence
described in the user's input. It provides insights and guidance rather
than predicting outcomes or exact court timelines.
"""

from __future__ import annotations


def _detect_case_type(text: str) -> str:
    """Infer case type using simple keyword patterns."""
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
    """Estimate complexity from case type and evidence strength."""
    lower = case_type.lower()

    if any(label in lower for label in ("cyber", "criminal", "cheque")):
        return "High"

    if "property" in lower:
        return "Medium"

    if "labour" in lower:
        return "Low" if score >= 0.6 else "Medium"

    if "family" in lower:
        return "Medium"

    return "Medium"


def _recommended_actions(case_type: str, missing_evidence: list[str]) -> list[str]:
    """Provide practical legal next steps based on case category."""
    lower = case_type.lower()

    if "labour" in lower:
        actions = [
            "Send a written demand notice to the employer regarding unpaid dues.",
            "File a complaint with the Labour Commissioner.",
            "Proceed to Labour Court if conciliation fails.",
        ]

    elif "property" in lower:
        actions = [
            "Collect title and ownership documents.",
            "Send a legal notice to the opposing party.",
            "File a civil case and request injunction if required.",
        ]

    elif "cheque" in lower:
        actions = [
            "Send statutory legal notice after cheque dishonour.",
            "File complaint under the Negotiable Instruments Act if payment is not made.",
            "Preserve bank memo and transaction records.",
        ]

    elif "cyber" in lower:
        actions = [
            "File complaint on the National Cyber Crime Portal.",
            "Report incident to local Cyber Crime Cell.",
            "Preserve screenshots, messages, and transaction records.",
        ]

    elif "family" in lower:
        actions = [
            "Consult a family lawyer for legal options.",
            "Attempt mediation if possible.",
            "File petition in Family Court if resolution fails.",
        ]

    elif "criminal" in lower:
        actions = [
            "File or follow up on FIR with detailed information.",
            "Collect witness information and supporting evidence.",
            "Consult a criminal lawyer regarding court procedures.",
        ]

    else:
        actions = [
            "Consult a lawyer to determine the appropriate legal forum.",
            "Prepare a detailed timeline of events.",
            "Consider issuing a legal notice before filing a case.",
        ]

    if missing_evidence:
        actions.append(
            "Gather missing evidence before proceeding: " + ", ".join(missing_evidence) + "."
        )

    return actions


def analyze_case_strength(case_text: str) -> dict:
    """
    Analyze case strength based on evidence described in the case text.

    The analysis is rule-based and provides insights rather than predictions.
    """

    if not isinstance(case_text, str):
        raise TypeError("case_text must be a string")

    normalized_text = case_text.strip().lower()

    if not normalized_text:
        raise ValueError("case_text must be a non-empty string")

    case_type = _detect_case_type(normalized_text)

    evidence_keywords = {
        "contract": ["contract", "employment contract", "signed contract"],
        "agreement": ["agreement", "written agreement", "signed agreement"],
        "witness": ["witness", "witnesses"],
        "email": ["email", "mail thread", "email proof"],
        "payment proof": ["payment proof", "bank statement", "bank records", "salary slip", "receipt"],
        "message": ["message", "sms", "whatsapp", "chat"],
        "recording": ["recording", "audio recording", "call recording", "video recording"],
    }

    detected_evidence = []

    for evidence_name, terms in evidence_keywords.items():
        if any(term in normalized_text for term in terms):
            detected_evidence.append(evidence_name)

    all_evidence_keys = list(evidence_keywords.keys())
    missing_evidence = [key for key in all_evidence_keys if key not in detected_evidence]

    # Base score
    score = 0.35

    strong_evidence_weights = {
        "contract": 0.15,
        "agreement": 0.10,
        "witness": 0.10,
        "email": 0.08,
        "payment proof": 0.20,
        "message": 0.07,
        "recording": 0.10,
    }

    for item in detected_evidence:
        score += strong_evidence_weights[item]

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
        outcome_insight = (
            "The available documentation appears strong and supports your claim."
        )

    elif score >= 0.4:
        case_strength = "Moderate"
        outcome_insight = (
            "Some supporting evidence is present, but strengthening documentation could improve the case."
        )

    else:
        case_strength = "Weak"
        outcome_insight = (
            "Limited evidence is currently available, which may make the case difficult to establish."
        )

    legal_complexity = _estimate_complexity(case_type, score)

    timeline_note = (
        "Court timelines in India can vary widely depending on court workload, "
        "procedural steps, and case complexity. Cases with clear evidence and "
        "fewer disputes may progress faster."
    )

    complexity_risk_adjustment = {"Low": 0.0, "Medium": 0.05, "High": 0.10}
    risk_probability = 1.0 - score + complexity_risk_adjustment[legal_complexity]
    risk_probability = round(max(0.0, min(1.0, risk_probability)), 2)

    recommended_actions = _recommended_actions(case_type, missing_evidence)

    return {
        "case_type": case_type,
        "case_strength": case_strength,
        "score": score,
        "outcome_insight": outcome_insight,
        "legal_complexity": legal_complexity,
        "timeline_note": timeline_note,
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