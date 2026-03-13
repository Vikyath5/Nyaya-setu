from typing import Dict


class ResolutionAdvisor:
    """
    ResolutionAdvisor

    Determines whether a dispute should proceed to court
    or can be resolved through alternative mechanisms.

    Uses:
    • case type
    • case strength
    • win probability
    • estimated timeline
    """

    # --------------------------------------
    # Main recommendation function
    # --------------------------------------

    def recommend(
        self,
        case_type: str,
        case_strength: str,
        win_probability: int,
        estimated_resolution_months: int
    ) -> Dict:

        case_type = (case_type or "").lower()
        case_strength = (case_strength or "").lower()

        reasoning = []
        court_required = True
        recommendation = "Court Litigation"

        # --------------------------------------
        # Labour disputes
        # --------------------------------------

        if case_type in ["labour_dispute", "employment_dispute"]:

            recommendation = "Labour Commissioner"
            court_required = False

            reasoning.append(
                "Labour disputes are commonly resolved through labour authorities before approaching courts."
            )

        # --------------------------------------
        # Consumer disputes
        # --------------------------------------

        elif case_type in ["consumer_complaint", "consumer_dispute"]:

            recommendation = "Consumer Forum"
            court_required = False

            reasoning.append(
                "Consumer protection forums provide a faster resolution mechanism for consumer disputes."
            )

        # --------------------------------------
        # Property / tenant disputes
        # --------------------------------------

        elif case_type in ["tenant_dispute", "property_dispute"]:

            recommendation = "Mediation"
            court_required = False

            reasoning.append(
                "Property and tenancy disputes are often suitable for mediation before litigation."
            )

        # --------------------------------------
        # Default case → Court
        # --------------------------------------

        else:

            recommendation = "Court Litigation"
            court_required = True

            reasoning.append(
                "The dispute may require formal judicial proceedings."
            )

        # --------------------------------------
        # Timeline consideration
        # --------------------------------------

        if estimated_resolution_months and estimated_resolution_months >= 24:

            reasoning.append(
                "Estimated timeline suggests court proceedings may take a long time due to backlog."
            )

            if not court_required:
                reasoning.append(
                    "Alternative resolution methods may lead to faster settlement."
                )

        # --------------------------------------
        # Outcome probability factor
        # --------------------------------------

        if win_probability:

            if win_probability < 40:

                reasoning.append(
                    "Low predicted probability of success suggests exploring settlement or mediation."
                )

            elif win_probability > 65:

                reasoning.append(
                    "High probability of success supports pursuing legal action if necessary."
                )

        return {

            "recommended_resolution": recommendation,

            "resolution_type": self._resolution_type(recommendation),

            "court_required": court_required,

            "resolution_reasoning": reasoning
        }

    # --------------------------------------
    # Resolution type mapping
    # --------------------------------------

    def _resolution_type(self, recommendation: str) -> str:

        mapping = {

            "Labour Commissioner": "Administrative Resolution",
            "Consumer Forum": "Consumer Protection Mechanism",
            "Mediation": "Alternative Dispute Resolution",
            "Court Litigation": "Judicial Process"
        }

        return mapping.get(recommendation, "Legal Process")