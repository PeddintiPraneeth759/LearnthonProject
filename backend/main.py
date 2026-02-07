"""
Fake News Verification API
FastAPI backend for verifying news claims using AI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from models.schemas import VerificationRequest, VerificationResponse, ErrorResponse
from agents.verifier import news_verifier
from config import APP_NAME, DEBUG


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    print(f"🚀 {APP_NAME} is starting...")
    yield
    print(f"👋 {APP_NAME} is shutting down...")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="AI-powered Fake News Verification API using LangChain and LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": APP_NAME,
        "message": "Welcome to the Fake News Verification API"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/verify", response_model=VerificationResponse)
async def verify_news(request: VerificationRequest):
    """
    Verify a news claim
    
    This endpoint accepts a news headline, paragraph, or claim and returns
    a verification result with verdict, confidence score, and trusted sources.
    """
    try:
        # Run verification workflow
        result = await news_verifier.verify(request.claim)
        
        return VerificationResponse(**result)
    except Exception as e:
        if DEBUG:
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(
            status_code=500,
            detail="An error occurred during verification. Please try again."
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
