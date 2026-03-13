"""Human-friendly explanation generator for NyayaSetu.

Combines outputs from case_strength_analyzer, outcome_predictor, and
timeline_predictor into a plain-English summary that non-lawyers can act on.
"""

from __future__ import annotations

from typing import Any


def _case_complexity(case_type: str, score: float) -> str:
    """Determine complexity level from case type and evidence score."""
    case_type_lower = case_type.lower()
    if any(word in case_type_lower for word in ("criminal", "cyber", "cheque")):
        return "High"
    if "property" in case_type_lower:
        return "Medium"
    # Labour disputes: let evidence score guide Low vs Medium.
    if score >= 0.6:
        return "Low"
    return "Medium"


def _confidence_level(score: float) -> str:
    """Map a 0-1 strength score to a human confidence label."""
    if score >= 0.75:
        return "High"
    if score >= 0.45:
        return "Medium"
    return "Low"


def _success_rate_statement(confidence: float) -> str:
    """Turn a model confidence value into a readable probability range."""
    pct = round(confidence * 100)
    low = max(0, pct - 10)
    high = min(100, pct + 10)
    return (
        f"Based on similar cases in the dataset, success probability is "
        f"around {low}–{high}%."
    )


def _legal_path(case_type: str) -> str:
    """Return step-by-step legal guidance based on case category."""
    case_type_lower = case_type.lower()
    if "labour" in case_type_lower or "wage" in case_type_lower:
        return (
            "Step 1: File a complaint with the Labour Commissioner.\n"
            "Step 2: Attempt mediation or conciliation with your employer.\n"
            "Step 3: If unresolved, file a case in the Labour Court.\n"
            "Step 4: Keep all salary slips, bank records, and communications safe."
        )
    if "property" in case_type_lower:
        return (
            "Step 1: Gather all property documents (title deed, sale agreement).\n"
            "Step 2: Send a legal notice to the opposing party.\n"
            "Step 3: File a civil suit in the Civil Court.\n"
            "Step 4: Seek interim relief (injunction) if possession is at risk."
        )
    if "cheque" in case_type_lower:
        return (
            "Step 1: Send a legal demand notice within 30 days of dishonour.\n"
            "Step 2: File a complaint under Section 138 of the Negotiable Instruments Act.\n"
            "Step 3: Appear before the Magistrate Court with bank evidence."
        )
    if "family" in case_type_lower:
        return (
            "Step 1: Consult a family lawyer for mediation options.\n"
            "Step 2: File a petition in the Family Court.\n"
            "Step 3: Pursue counselling sessions if ordered by court."
        )
    if "cyber" in case_type_lower or "fraud" in case_type_lower:
        return (
            "Step 1: File a complaint on the National Cyber Crime Portal (cybercrime.gov.in).\n"
            "Step 2: Approach the local Cyber Crime Cell.\n"
            "Step 3: File an FIR at the nearest police station.\n"
            "Step 4: Preserve all digital evidence (screenshots, emails, transactions)."
        )
    return (
        "Step 1: Consult a qualified lawyer about your specific situation.\n"
        "Step 2: Send a formal legal notice to the opposing party.\n"
        "Step 3: File a case in the appropriate Civil Court.\n"
        "Step 4: Gather and preserve all available evidence."
    )


def generate_explanation(
    case_strength: dict[str, Any],
    outcome_prediction: dict[str, Any],
    timeline_prediction: dict[str, Any],
) -> dict[str, str]:
    """Combine AI module outputs into a plain-English explanation.

    Parameters
    ----------
    case_strength:
        Output dictionary from case_strength_analyzer.analyze_case_strength().
    outcome_prediction:
        Output dictionary from the outcome predictor module.
    timeline_prediction:
        Output dictionary from the timeline predictor module.

    Returns
    -------
    dict
        Nine structured insight fields written in simple English.
    """
    case_type = case_strength.get("case_type", "General Civil Dispute")
    strength_label = case_strength.get("case_strength", "Moderate")
    score = float(case_strength.get("score", 0.5))
    evidence_found = case_strength.get("key_evidence_detected", [])
    missing = case_strength.get("missing_evidence", [])
    risk_factors = case_strength.get("risk_factors", [])

    predicted_outcome = outcome_prediction.get("predicted_outcome", "Outcome uncertain")
    confidence = float(outcome_prediction.get("confidence", 0.5))

    resolution_time = timeline_prediction.get("estimated_resolution_time", "Not available")

    # 1. Summary
    summary = (
        f"Your case is classified as a {case_type}. "
        f"Based on the information provided, your case appears to be {strength_label.lower()}. "
        f"The AI analysis predicts: {predicted_outcome}."
    )

    # 2. Reasoning
    if strength_label == "Strong":
        reason_core = (
            "You have provided solid evidence that supports your claim. "
            "The documentation available significantly improves your chances in court."
        )
    elif strength_label == "Moderate":
        reason_core = (
            "You have some supporting evidence, but gaps remain. "
            "Strengthening your documentation before filing will improve your position."
        )
    else:
        reason_core = (
            "The evidence currently available is limited. "
            "This weakens your case and makes the outcome harder to predict. "
            "Collecting more proof before proceeding is strongly advised."
        )

    risk_note = ""
    if risk_factors:
        risk_note = " Potential challenges include: " + "; ".join(risk_factors) + "."
    reasoning = reason_core + risk_note

    # 3. Evidence analysis
    if evidence_found:
        evidence_analysis = (
            f"The following evidence was detected in your case: "
            f"{', '.join(evidence_found)}. "
            "Each piece of evidence helps establish the facts of your case and "
            "makes it more credible in the eyes of the court."
        )
    else:
        evidence_analysis = (
            "No clear evidence was detected in the details you provided. "
            "Without supporting documents or witnesses, your case will be hard to prove."
        )

    # 4. Missing evidence explanation
    if missing:
        missing_explanation = (
            f"The following evidence is missing: {', '.join(missing)}. "
            "Courts rely heavily on documented proof. Missing evidence can lead to "
            "delays, weaken your arguments, or even result in the case being dismissed. "
            "Try to collect these before filing."
        )
    else:
        missing_explanation = (
            "All key evidence types appear to be covered. "
            "Make sure physical copies of all documents are organised and ready."
        )

    # 5-9. Derived fields
    success_rate_estimate = _success_rate_statement(confidence)
    case_complexity = _case_complexity(case_type, score)
    recommended_legal_path = _legal_path(case_type)
    confidence_level = _confidence_level(score)

    return {
        "summary": summary,
        "reasoning": reasoning,
        "evidence_analysis": evidence_analysis,
        "missing_evidence_explanation": missing_explanation,
        "success_rate_estimate": success_rate_estimate,
        "case_complexity": case_complexity,
        "recommended_legal_path": recommended_legal_path,
        "estimated_timeline": resolution_time,
        "confidence_level": confidence_level,
    }


if __name__ == "__main__":
    sample_case_strength = {
        "case_type": "Labour Wage Dispute",
        "case_strength": "Strong",
        "score": 0.82,
        "key_evidence_detected": ["salary slips", "bank records"],
        "missing_evidence": ["employment contract"],
        "risk_factors": ["employer may deny employment"],
    }

    sample_outcome_prediction = {
        "predicted_outcome": "Employee likely to win",
        "confidence": 0.74,
    }

    sample_timeline_prediction = {
        "estimated_resolution_time": "3-6 months",
    }

    explanation = generate_explanation(
        sample_case_strength,
        sample_outcome_prediction,
        sample_timeline_prediction,
    )

    print("Case Explanation:")
    for key, value in explanation.items():
        print(f"\n[{key.upper()}]\n{value}")
