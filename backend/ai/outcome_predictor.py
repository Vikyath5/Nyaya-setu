from typing import List, Dict


class OutcomePredictor:
    """
    OutcomePredictor

    Predicts case outcomes using:
    • similarity-weighted precedent analysis
    • document evidence strength
    • explainable reasoning
    • probability normalization

    Output is designed for API + frontend consumption.
    """

    # --------------------------------------------------
    # Evidence multiplier based on document readiness
    # --------------------------------------------------

    def evidence_multiplier(self, readiness_score: int) -> float:

        if readiness_score >= 80:
            return 1.15
        elif readiness_score >= 50:
            return 1.05
        else:
            return 0.9

    # --------------------------------------------------
    # Document analysis + reasoning generator
    # --------------------------------------------------

    def document_analysis(
        self,
        uploaded_docs: List[str],
        required_docs: List[str]
    ) -> Dict:

        uploaded_docs = uploaded_docs or []
        required_docs = required_docs or []

        uploaded = set(uploaded_docs)
        required = set(required_docs)

        missing = list(required - uploaded)

        reasoning = []

        # Specific reasoning
        if "employment_contract" in uploaded:
            reasoning.append(
                "Employment contract confirms the legal relationship between parties."
            )

        if "salary_slips" in uploaded:
            reasoning.append(
                "Salary slips support the employee's wage claim."
            )

        if "bank_statements" not in uploaded and "bank_statements" in required:
            reasoning.append(
                "Bank statements are missing which weakens financial verification."
            )

        # Generic reasoning for uploaded documents
        for doc in uploaded:
            if doc not in ["employment_contract", "salary_slips"]:
                reasoning.append(
                    f"{doc.replace('_',' ').title()} submitted as supporting evidence."
                )

        # Generic reasoning for missing documents
        for doc in missing:
            reasoning.append(
                f"{doc.replace('_',' ').title()} not provided which may weaken supporting evidence."
            )

        readiness_score = (
            round((len(uploaded) / len(required)) * 100)
            if required else 100
        )

        if readiness_score >= 80:
            strength = "Strong"
        elif readiness_score >= 50:
            strength = "Moderate"
        else:
            strength = "Weak"

        return {
            "documents_submitted": list(uploaded),
            "documents_missing": missing,
            "document_strength_level": strength,
            "readiness_score": readiness_score,
            "document_reasoning": reasoning
        }

    # --------------------------------------------------
    # Similarity weighted outcome calculation
    # --------------------------------------------------

    def weighted_outcomes(self, similar_cases: List[Dict]):

        win_score = 0
        settlement_score = 0
        dismissal_score = 0

        for case in similar_cases:

            outcome = case.get("outcome", "").lower()
            similarity = case.get("similarity", 0.5)

            if outcome in ["employee_won", "plaintiff_won", "won"]:
                win_score += similarity

            elif outcome in ["settled", "settlement"]:
                settlement_score += similarity

            elif outcome in ["dismissed", "defendant_won"]:
                dismissal_score += similarity

        return win_score, settlement_score, dismissal_score

    # --------------------------------------------------
    # Final prediction function
    # --------------------------------------------------

    def predict(
        self,
        similar_cases: List[Dict],
        uploaded_docs: List[str],
        required_docs: List[str]
    ) -> Dict:

        similar_cases = similar_cases or []
        uploaded_docs = uploaded_docs or []
        required_docs = required_docs or []

        doc_analysis = self.document_analysis(uploaded_docs, required_docs)

        win_score, settlement_score, dismissal_score = \
            self.weighted_outcomes(similar_cases)

        total = win_score + settlement_score + dismissal_score

        # fallback when no precedent cases found
        if total == 0:
            return {
                "outcome_prediction": {
                    "win_probability_percent": 33,
                    "settlement_probability_percent": 33,
                    "dismissal_probability_percent": 34,
                    "confidence_percent": 20
                },
                "document_analysis": doc_analysis
            }

        win_prob = win_score / total
        settlement_prob = settlement_score / total
        dismissal_prob = dismissal_score / total

        multiplier = self.evidence_multiplier(doc_analysis["readiness_score"])

        win_prob *= multiplier

        normalization = win_prob + settlement_prob + dismissal_prob

        win_prob /= normalization
        settlement_prob /= normalization
        dismissal_prob /= normalization

        win_percent = round(win_prob * 100)
        settlement_percent = round(settlement_prob * 100)
        dismissal_percent = round(dismissal_prob * 100)

        confidence = min(95, 50 + len(similar_cases) * 5)

        return {

            "outcome_prediction": {
                "win_probability_percent": win_percent,
                "settlement_probability_percent": settlement_percent,
                "dismissal_probability_percent": dismissal_percent,
                "confidence_percent": confidence
            },

            "document_analysis": doc_analysis,

            "prediction_factors": {
                "similar_cases_analyzed": len(similar_cases),
                "evidence_multiplier": multiplier,
                "method": "similarity_weighted_precedent_analysis"
            }
        }