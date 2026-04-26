"""
Main FastAPI Application Entry Point

This module initializes the FastAPI application and includes all route handlers.
It provides REST APIs for video upload, processing, and ASL narration generation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.routes import video, asl_dataset, health, dynamic_asl, generative_asl, generated_media
from app.routes import lesson, ai_lesson
from app.models.database import engine, Base
import os
from dotenv import load_dotenv

# Import the simplified real-time ASL route
import sys
# Project root is: .../Code (two levels above backend/app)
# backend/app/main.py -> backend -> Code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from app.routes.realtime_asl_simplified import router as realtime_asl_router
    print("✅ Successfully imported simplified realtime ASL route")
except ImportError as e:
    print(f"❌ Failed to import simplified realtime ASL route: {e}")
    # Continue with dynamic route

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="ASL Video Narration Platform API",
    description="API for converting spoken video content into ASL-based narration for hearing-impaired children",
    version="1.0.0"
)

# CORS middleware configuration
# Allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route handlers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(video.router, prefix="/api/videos", tags=["Videos"])
app.include_router(asl_dataset.router, prefix="/api/asl-dataset", tags=["ASL Dataset"])
app.include_router(dynamic_asl.router, prefix="/api", tags=["Dynamic ASL"])
app.include_router(generative_asl.router, prefix="/api", tags=["Generative ASL Avatar"])
app.include_router(generated_media.router, prefix="/api", tags=["Generated Media"])
app.include_router(realtime_asl_router, prefix="/api", tags=["Real-Time ASL"])
app.include_router(lesson.router, prefix="/api", tags=["Lesson Mode"])
app.include_router(ai_lesson.router, prefix="/api", tags=["AI Lesson Generation"])

# Serve static files (storage directory) - create it if missing so mount always succeeds
storage_dir = os.path.join(project_root, "storage")
os.makedirs(os.path.join(storage_dir, "processed", "images"), exist_ok=True)
app.mount("/storage", StaticFiles(directory=storage_dir), name="storage")


@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on application startup.
    Creates all tables defined in models if they don't exist.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup tasks when application shuts down.
    """
    print("Application shutting down")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    Returns a user-friendly error message.
    """
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "error": str(exc)}
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

