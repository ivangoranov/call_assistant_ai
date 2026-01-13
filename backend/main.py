"""
AI Call Summarizer Backend - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, calls

app = FastAPI(
    title="AI Call Summarizer API",
    description="Backend API for AI Call Summarizer MVP",
    version="0.1.0",
)

# CORS middleware for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(calls.router, prefix="/calls", tags=["Calls"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
