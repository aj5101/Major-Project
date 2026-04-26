"""
AI Lesson Generation API Routes
Provides endpoints for AI-powered ASL lesson generation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.services.ai_lesson_service import generate_ai_lesson, is_ai_available, ai_lesson_service
from dynamic_asl_generator import create_video_for_text

router = APIRouter()

class LessonRequest(BaseModel):
    lesson_title: str
    lesson_text: str
    use_ai: bool = True

class LessonResponse(BaseModel):
    success: bool
    lesson_data: Optional[Dict] = None
    video_data: Optional[Dict] = None
    image_data: Optional[Dict] = None
    message: str
    ai_available: bool

@router.post("/generate-asl-lesson", response_model=LessonResponse)
async def generate_asl_lesson(
    request: LessonRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate ASL lesson using AI and create video
    
    This endpoint:
    1. Processes lesson text with AI to create ASL-friendly content
    2. Generates structured lesson data
    3. Creates ASL video using existing pipeline
    4. Returns complete lesson package
    """
    
    # Check if AI is available
    ai_available = is_ai_available()
    
    try:
        print("🖼️ Generating ASL lesson with images...")
        lesson_data = await ai_lesson_service.generate_ai_image_lesson(
            request.lesson_text,
            request.lesson_title
        )

        if lesson_data.get("ai_images_used") and lesson_data.get("image_data"):
            image_data = lesson_data["image_data"]
            print(f"✅ Images ready: {image_data.get('total_images')} images")
            return LessonResponse(
                success=True,
                lesson_data=lesson_data,
                image_data=image_data,
                message="ASL lesson with images generated successfully!",
                ai_available=ai_available
            )

        # Images couldn't be generated at all — return lesson structure only
        print("⚠️ No images generated, returning lesson structure only")
        return LessonResponse(
            success=True,
            lesson_data=lesson_data,
            message="Lesson generated (image generation unavailable)",
            ai_available=ai_available
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate ASL lesson: {str(e)}"
        )

@router.get("/ai-status")
async def get_ai_status():
    """Check if AI lesson generation is available"""
    return {
        "ai_available": is_ai_available(),
        "service": "Google Gemini AI",
        "message": "AI lesson generation is available" if is_ai_available() else "AI service not configured - using fallback rules"
    }

@router.post("/preview-lesson")
async def preview_lesson(request: LessonRequest):
    """
    Preview AI-processed lesson without generating video
    Faster endpoint for preview functionality
    """
    try:
        lesson_data = generate_ai_lesson(
            request.lesson_text,
            request.lesson_title
        )
        
        return {
            "success": True,
            "lesson_data": lesson_data,
            "ai_available": is_ai_available(),
            "message": "Lesson preview generated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to preview lesson: {str(e)}"
        )
