from backend.ai.similarity_engine import SimilarityEngine
from backend.ai.timeline_predictor import HearingScheduleAnalyzer
from backend.ai.outcome_predictor import OutcomePredictor
from backend.ai.case_strength_analyzer import analyze_case_strength
from backend.ai.explanation_generator import generate_explanation


class CasePipeline:

    def __init__(self):

        self.similarity_engine = SimilarityEngine()
        self.timeline_analyzer = HearingScheduleAnalyzer()
        self.outcome_predictor = OutcomePredictor()

    def analyze_case(self, case_description, court, uploaded_documents):

        # ---------------------------------------------------
        # 1️⃣ Find similar cases
        # ---------------------------------------------------
        similar_cases = self.similarity_engine.find_similar_cases(
            case_description
        )

        # ---------------------------------------------------
        # 2️⃣ Extract required docs from most similar case
        # ---------------------------------------------------
        required_documents = []

        if similar_cases:
            top_case = similar_cases[0]

            required_documents = top_case.get("documents_required", [])

        # ---------------------------------------------------
        # 3️⃣ Detect missing documents
        # ---------------------------------------------------
        missing_documents = []

        for doc in required_documents:
            if doc.lower() not in [d.lower() for d in uploaded_documents]:
                missing_documents.append(doc)

        # ---------------------------------------------------
        # 4️⃣ Timeline insight (no prediction)
        # ---------------------------------------------------
        timeline_result = self.timeline_analyzer.analyze(
            court,
            similar_cases
        )

        # ---------------------------------------------------
        # 5️⃣ Outcome analysis
        # ---------------------------------------------------
        outcome_result = self.outcome_predictor.predict(similar_cases)

        # ---------------------------------------------------
        # 6️⃣ Case strength
        # ---------------------------------------------------
        strength_result = analyze_case_strength(case_description)

        # ---------------------------------------------------
        # 7️⃣ Generate explanation
        # ---------------------------------------------------
        explanation = generate_explanation(
            strength_result,
            outcome_result,
            timeline_result
        )

        # ---------------------------------------------------
        # 8️⃣ Resolution suggestion
        # ---------------------------------------------------
        recommended_resolution = None

        if similar_cases:
            recommended_resolution = similar_cases[0].get(
                "resolution_method"
            )

        # ---------------------------------------------------
        # FINAL RESPONSE
        # ---------------------------------------------------
        return {

            "similar_cases_found": similar_cases,

            "document_analysis": {
                "required_documents": required_documents,
                "uploaded_documents": uploaded_documents,
                "missing_documents": missing_documents
            },

            "recommended_resolution_method": recommended_resolution,

            "timeline_insight": timeline_result,

            "outcome_analysis": outcome_result,

            "case_strength": strength_result,

            "legal_explanation": explanation
        }