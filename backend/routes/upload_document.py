from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.ai.document_verifier import DocumentVerifier

router = APIRouter()

verifier = DocumentVerifier()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-document")

async def upload_document(expected_type: str, file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = verifier.verify_document(file_path, expected_type)

    return {
        "filename": file.filename,
        "expected_document_type": expected_type,
        "verification_result": result
    }