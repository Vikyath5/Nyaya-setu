from fastapi import APIRouter, HTTPException
from backend.schemas.case_schema import CaseRequest
from backend.services.case_pipeline import CasePipeline

router = APIRouter()

pipeline = CasePipeline()


@router.post("/analyze-case")
def analyze_case(data: CaseRequest):

    try:

        result = pipeline.analyze(
            data.case_description,
            data.court,
            data.uploaded_docs,
            data.required_docs
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Case analysis failed: {str(e)}"
        )