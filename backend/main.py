"""
NyayaSetu — FastAPI Application
Main entry point for the backend server.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze_case import router as analyze_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("nyayasetu")

# Create FastAPI app
app = FastAPI(
    title="NyayaSetu API",
    description="AI-Powered Legal Guidance Platform — Backend API",
    version="1.0.0",
)

# CORS middleware — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(analyze_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "NyayaSetu API",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to NyayaSetu API",
        "docs": "/docs",
        "health": "/health",
    }


logger.info("NyayaSetu API initialized successfully")
