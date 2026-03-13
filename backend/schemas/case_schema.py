from pydantic import BaseModel
from typing import List


class CaseRequest(BaseModel):
    case_description: str
    court: str
    uploaded_docs: List[str] = []
    required_docs: List[str] = []


class CaseResponse(BaseModel):
    similar_cases: list
    timeline: dict
    outcome_analysis: dict
    case_strength: dict
    resolution_advice: dict
    explanation: str