from fastapi import FastAPI
from backend.routes.analyze_case import router as analyze_router
from backend.routes.upload_document import router as upload_router

app = FastAPI(
    title="NyayaSetu Legal AI API",
    description="AI-powered legal assistance backend",
    version="1.0"
)

app.include_router(analyze_router)
app.include_router(upload_router)

@app.get("/")
def root():
    return {"message": "NyayaSetu backend running"}