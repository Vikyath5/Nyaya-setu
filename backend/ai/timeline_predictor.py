import json
import os
from typing import Dict, List


class HearingScheduleAnalyzer:
    """
    HearingScheduleAnalyzer

    Provides administrative insights on when a case may
    receive its first hearing listing based on court backlog
    and filing readiness.

    This module does NOT predict case outcomes or final timelines.
    """

    def __init__(self, court_dataset_path: str = None):

        if court_dataset_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            court_dataset_path = os.path.join(base_dir, "dataset", "court_load.json")

        try:
            with open(court_dataset_path, "r", encoding="utf-8") as f:
                self.court_data = json.load(f)
        except Exception:
            self.court_data = {}

    # ----------------------------------
    # Document readiness analysis
    # ----------------------------------

    def document_status(
        self,
        uploaded_docs: List[str],
        required_docs: List[str]
    ) -> Dict:

        uploaded = set(uploaded_docs or [])
        required = set(required_docs or [])

        missing = list(required - uploaded)

        readiness_score = (
            round((len(uploaded) / len(required)) * 100)
            if required else 100
        )

        if readiness_score >= 80:
            status = "Complete"
        elif readiness_score >= 50:
            status = "Partial"
        else:
            status = "Incomplete"

        return {
            "document_status": status,
            "documents_missing": missing,
            "readiness_score": readiness_score
        }

    # ----------------------------------
    # Court backlog analysis
    # ----------------------------------

    def court_backlog(self, court_name: str) -> Dict:

        court = self.court_data.get(court_name, {})

        return {
            "court_name": court_name,
            "pending_cases": court.get("pending_cases", "Unknown"),
            "backlog_delay_months": court.get("backlog_delay_months", 2),
            "load_level": court.get("load_level", "Moderate")
        }

    # ----------------------------------
    # Hearing window estimation
    # ----------------------------------

    def hearing_window(self, backlog_delay: int, readiness_score: int):

        base_months = backlog_delay

        if readiness_score < 50:
            base_months += 1

        lower = max(1, base_months)
        upper = base_months + 2

        return f"{lower}-{upper} months"

    # ----------------------------------
    # Final analysis
    # ----------------------------------

    def analyze(
        self,
        court_name: str,
        case_type: str,
        uploaded_docs: List[str],
        required_docs: List[str]
    ) -> Dict:

        document_info = self.document_status(uploaded_docs, required_docs)
        court_info = self.court_backlog(court_name)

        hearing_range = self.hearing_window(
            court_info["backlog_delay_months"],
            document_info["readiness_score"]
        )

        explanation = []

        if court_info["load_level"] == "High":
            explanation.append(
                f"High backlog in {court_name} may delay hearing allocation."
            )

        if document_info["document_status"] != "Complete":
            explanation.append(
                "Incomplete documentation may delay administrative listing."
            )

        explanation.append(
            "Court listings depend on registry processing and judicial availability."
        )

        return {

            "hearing_schedule_insight": {
                "estimated_first_hearing_window": hearing_range,
                "court": court_name,
                "filing_readiness": document_info["document_status"]
            },

            "administrative_factors": {
                "court_backlog_level": court_info["load_level"],
                "document_status": document_info["document_status"],
                "documents_missing": document_info["documents_missing"]
            },

            "explanation": explanation
        }