"""
Human-friendly explanation generator for NyayaSetu.

Combines outputs from different AI modules and converts them into
clear insights that non-lawyers can understand. The system does not
predict legal outcomes or exact court timelines; it only provides
guidance based on patterns from similar cases.
"""

from __future__ import annotations
from typing import Any


def _case_complexity(case_type: str, score: float) -> str:
    """Estimate general complexity level."""
    case_type_lower = case_type.lower()

    if any(word in case_type_lower for word in ("criminal", "cyber", "cheque")):
        return "High"

    if "property" in case_type_lower:
        return "Medium"

    if score >= 0.6:
        return "Low"

    return "Medium"


def _confidence_level(score: float) -> str:
    """Convert evidence score into a readable confidence label."""
    if score >= 0.75:
        return "High"
    if score >= 0.45:
        return "Medium"
    return "Low"


def _historical_pattern_statement(confidence: float) -> str:
    """Explain patterns from similar cases without claiming prediction."""
    pct = round(confidence * 100)
    low = max(0, pct - 10)
    high = min(100, pct + 10)

    return (
        "Based on patterns observed in similar cases within the dataset, "
        f"cases with comparable evidence and circumstances often see favourable "
        f"results in roughly {low}–{high}% of situations. "
        "However, court outcomes depend on many factors and cannot be guaranteed."
    )


def _legal_path(case_type: str) -> str:
    """Provide practical legal guidance steps."""
    case_type_lower = case_type.lower()

    if "labour" in case_type_lower or "wage" in case_type_lower:
        return (
            "Step 1: File a complaint with the Labour Commissioner.\n"
            "Step 2: Attempt mediation or conciliation with the employer.\n"
            "Step 3: If unresolved, consider filing a case in the Labour Court.\n"
            "Step 4: Preserve salary slips, bank records, and employment documents."
        )

    if "property" in case_type_lower:
        return (
            "Step 1: Gather property ownership documents.\n"
            "Step 2: Send a legal notice to the opposing party.\n"
            "Step 3: If the issue persists, file a civil case in the appropriate court.\n"
            "Step 4: Maintain records of agreements and transactions."
        )

    if "cheque" in case_type_lower:
        return (
            "Step 1: Send a legal demand notice within 30 days of cheque dishonour.\n"
            "Step 2: If payment is not made, file a complaint under Section 138.\n"
            "Step 3: Present bank documents and cheque records in court."
        )

    if "cyber" in case_type_lower or "fraud" in case_type_lower:
        return (
            "Step 1: File a complaint on the National Cyber Crime Portal.\n"
            "Step 2: Report the matter to the nearest Cyber Crime Cell.\n"
            "Step 3: Preserve screenshots, transaction records, and communication logs."
        )

    return (
        "Step 1: Consult a qualified lawyer regarding your situation.\n"
        "Step 2: Consider sending a legal notice to the opposing party.\n"
        "Step 3: If required, file a case in the appropriate court.\n"
        "Step 4: Preserve all relevant documents and evidence."
    )


def generate_explanation(
    case_strength: dict[str, Any],
    outcome_analysis: dict[str, Any],
    timeline_insight: dict[str, Any],
) -> dict[str, str]:
    """
    Combine AI outputs into a clear explanation.

    The system provides insights based on patterns from similar cases
    and does not guarantee legal outcomes or timelines.
    """

    case_type = case_strength.get("case_type", "General Civil Dispute")
    strength_label = case_strength.get("case_strength", "Moderate")
    score = float(case_strength.get("score", 0.5))

    evidence_found = case_strength.get("key_evidence_detected", [])
    missing = case_strength.get("missing_evidence", [])
    risk_factors = case_strength.get("risk_factors", [])

    confidence = float(outcome_analysis.get("confidence", 0.5))

    timeline_text = (
        timeline_insight.get("estimated_first_hearing_window")
        or timeline_insight.get("estimated_resolution_time")
        or "Court timelines can vary significantly depending on workload and case complexity."
    )

    # Summary
    summary = (
        f"This case appears to be a {case_type}. "
        f"Based on the information available, the case currently looks {strength_label.lower()}. "
        "The following insights are derived from patterns observed in similar disputes."
    )

    # Reasoning
    if strength_label == "Strong":
        reason_core = (
            "The available evidence appears strong and supports your claim."
        )
    elif strength_label == "Moderate":
        reason_core = (
            "Some evidence supports your case, but strengthening documentation may help."
        )
    else:
        reason_core = (
            "The available evidence is currently limited, which may make the case harder to establish."
        )

    risk_note = ""
    if risk_factors:
        risk_note = " Potential challenges include: " + "; ".join(risk_factors) + "."

    reasoning = reason_core + risk_note

    # Evidence analysis
    if evidence_found:
        evidence_analysis = (
            "The system identified the following evidence in your case: "
            f"{', '.join(evidence_found)}."
        )
    else:
        evidence_analysis = (
            "No clear supporting evidence was detected in the case description."
        )

    # Missing evidence explanation
    if missing:
        missing_explanation = (
            f"The following evidence could strengthen your case: {', '.join(missing)}."
        )
    else:
        missing_explanation = (
            "Key evidence categories appear to be present based on the available information."
        )

    return {
        "summary": summary,
        "reasoning": reasoning,
        "evidence_analysis": evidence_analysis,
        "missing_evidence_explanation": missing_explanation,
        "historical_pattern_insight": _historical_pattern_statement(confidence),
        "case_complexity": _case_complexity(case_type, score),
        "recommended_legal_path": _legal_path(case_type),
        "timeline_note": timeline_text,
        "confidence_level": _confidence_level(score),
    }