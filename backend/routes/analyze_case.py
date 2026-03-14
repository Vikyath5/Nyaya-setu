"""
NyayaSetu — Analyze Case Route
POST /analyze-case endpoint that orchestrates all AI modules.
"""

import os
import logging
from typing import Optional, List

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from ai.case_strength_analyzer import analyze_case_strength
from ai.outcome_predictor import predict_outcome
from ai.timeline_predictor import predict_timeline
from ai.similarity_engine import find_similar_cases
from ai.explanation_generator import generate_explanation
from services.document_service import suggest_documents, generate_checklist_pdf

logger = logging.getLogger("nyayasetu")

router = APIRouter()

# PDF output directory
PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_pdfs")


@router.post("/analyze-case")
async def analyze_case(
    case_description: str = Form(...),
    documents: Optional[List[UploadFile]] = File(None),
):
    """
    Analyze a legal case using all AI modules.
    Accepts case description (required) and optional file uploads.
    Returns comprehensive analysis results.
    """
    if not case_description or not case_description.strip():
        raise HTTPException(status_code=400, detail="Case description is required")

    logger.info(f"Analyzing case: {case_description[:100]}...")

    try:
        # Process uploaded documents (extract filenames)
        doc_names = []
        if documents:
            for doc in documents:
                if doc.filename:
                    doc_names.append(doc.filename)
                    logger.info(f"Document uploaded: {doc.filename}")

        # Run all AI modules
        # 1. Case Strength Analysis
        strength_result = analyze_case_strength(case_description, doc_names)
        logger.info(f"Case strength: {strength_result['score']}%")

        # 2. Outcome Prediction
        outcome_result = predict_outcome(case_description, strength_result["score"])
        logger.info(f"Dominant outcome: {outcome_result['dominant_outcome']}")

        # 3. Timeline Prediction
        timeline_result = predict_timeline(case_description)
        logger.info(f"Estimated duration: {timeline_result['estimated_duration']}")

        # 4. Similar Cases
        similarity_result = find_similar_cases(case_description, doc_names)
        logger.info(f"Found {similarity_result['matches_found']} similar cases")

        # 5. Legal Explanation
        explanation_result = generate_explanation(case_description)
        logger.info(f"Detected type: {explanation_result['detected_type']}")

        # 6. Document Suggestions
        legal_category = strength_result["legal_category"]
        required_documents = suggest_documents(legal_category)

        # 7. Generate PDF checklist
        checklist_filename = generate_checklist_pdf(
            required_documents,
            legal_category,
            case_description[:200]
        )
        logger.info(f"PDF generated: {checklist_filename}")

        # Combine results
        response = {
            "case_strength": {
                "score": strength_result["score"],
                "label": strength_result["label"],
                "strengths": strength_result["strengths"],
                "weaknesses": strength_result["weaknesses"],
                "evidence_strength": strength_result["evidence_strength"],
            },
            "predicted_outcome": {
                "outcomes": outcome_result["outcomes"],
                "dominant_outcome": outcome_result["dominant_outcome"],
                "recommendation": outcome_result["recommendation"],
                "confidence": outcome_result["confidence"],
            },
            "estimated_timeline": {
                "duration": timeline_result["estimated_duration"],
                "nodes": timeline_result["nodes"],
                "note": timeline_result["note"],
            },
            "similar_cases": similarity_result["similar_cases"],
            "legal_explanation": {
                "detected_type": explanation_result["detected_type"],
                "section_ref": explanation_result["section_ref"],
                "summary": explanation_result["summary"],
                "legal_points": explanation_result["legal_points"],
            },
            "required_documents": required_documents,
            "checklist_pdf": checklist_filename,
            "uploaded_documents": doc_names,
        }

        return response

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/download-checklist/{filename}")
async def download_checklist(filename: str):
    """Download a generated PDF checklist."""
    filepath = os.path.join(PDF_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Checklist not found")
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
