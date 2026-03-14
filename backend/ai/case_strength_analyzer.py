"""
NyayaSetu — Case Strength Analyzer
Analyzes case description and returns strength score with strengths/weaknesses.
"""

from .embedding_model import detect_legal_category, assess_evidence_strength, normalize_text


def analyze_case_strength(case_description: str, documents: list = None) -> dict:
    """
    Analyze the strength of a legal case based on description and documents.
    Returns a score (0-100) with strengths and weaknesses.
    """
    text = normalize_text(case_description)
    category_info = detect_legal_category(case_description)
    evidence = assess_evidence_strength(case_description)

    # Base score from category match strength
    category_score = min(category_info["primary_score"] * 12, 40)

    # Evidence score
    evidence_score = int(evidence["score"] * 0.35)

    # Document bonus
    doc_score = 0
    if documents and len(documents) > 0:
        doc_score = min(len(documents) * 5, 15)

    # Description length/detail bonus
    word_count = len(text.split())
    detail_score = min(word_count // 10, 10)

    total_score = min(category_score + evidence_score + doc_score + detail_score, 95)
    total_score = max(total_score, 25)  # minimum 25%

    # Generate strengths based on analysis
    strengths = []
    weaknesses = []

    if category_info["primary_score"] >= 3:
        strengths.append(f"Clear {category_info['primary_category'].title()} dispute identified")
    if category_info["primary_score"] >= 2:
        strengths.append(f"Multiple legal keywords detected ({', '.join(category_info['matched_keywords'][:3])})")

    if evidence["strength"] == "strong":
        strengths.append("Strong documentary evidence mentioned")
    elif evidence["strength"] == "moderate":
        strengths.append("Moderate evidence indicators present")

    if word_count >= 50:
        strengths.append("Detailed case description provided")

    if documents and len(documents) > 0:
        strengths.append(f"{len(documents)} supporting document(s) uploaded")

    # Check for specific strong indicators
    if any(w in text for w in ["written", "email", "letter", "documented"]):
        strengths.append("Written communication records on file")
    if any(w in text for w in ["contract", "agreement"]):
        strengths.append("Formal agreement/contract exists")
    if any(w in text for w in ["witness", "witnesses"]):
        strengths.append("Witness testimony available")

    # Generate weaknesses
    if evidence["strength"] == "weak":
        weaknesses.append("Evidence appears primarily verbal/circumstantial")
    if evidence["strength"] == "unknown":
        weaknesses.append("No clear evidence indicators in description")
    if word_count < 30:
        weaknesses.append("Case description lacks sufficient detail")
    if not documents or len(documents) == 0:
        weaknesses.append("No supporting documents uploaded")

    if "notice" not in text and "legal notice" not in text:
        weaknesses.append("No formal legal notice sent yet")
    if "police" not in text and "fir" not in text and category_info["primary_category"] == "criminal":
        weaknesses.append("No FIR/police complaint mentioned")

    # Ensure we have at least some feedback
    if not strengths:
        strengths.append("Case filed for legal analysis")
    if not weaknesses:
        weaknesses.append("Further documentation strengthens the case")

    return {
        "score": total_score,
        "label": _score_label(total_score),
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:4],
        "evidence_strength": evidence["strength"],
        "legal_category": category_info["primary_category"]
    }


def _score_label(score: int) -> str:
    if score >= 75:
        return "Strong"
    elif score >= 55:
        return "Moderate"
    elif score >= 35:
        return "Fair"
    else:
        return "Needs Strengthening"
