"""
Dynamic ASL Generation API Route
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.models.database import get_db
import sys
import os

# Add the project root to path to import the generator
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from dynamic_asl_generator import create_video_for_text
except ImportError as e:
    print(f"Failed to import dynamic_asl_generator: {e}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    raise

router = APIRouter()

class ASLGenerationRequest(BaseModel):
    text: str
    video_id: str = None

class ASLGenerationResponse(BaseModel):
    video_file: str
    signs: list
    duration: float
    text: str
    video_url: str

@router.post("/generate-asl", response_model=ASLGenerationResponse)
async def generate_asl_video(
    request: ASLGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a custom ASL video based on input text.
    
    Args:
        request: Text and optional video ID for generation
        
    Returns:
        Information about the generated ASL video
    """
    try:
        # Generate the video
        result = create_video_for_text(request.text, request.video_id)
        
        # Return response with video URL
        return ASLGenerationResponse(
            video_file=result['video_file'],
            signs=result['signs'],
            duration=result['duration'],
            text=result['text'],
            video_url=f"/storage/processed/dynamic/{result['video_file']}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ASL video: {str(e)}")

@router.get("/available-signs")
async def get_available_signs():
    """
    Get list of available ASL signs.
    
    Returns:
        List of available ASL signs
    """
    try:
        from dynamic_asl_generator import get_available_signs
        signs = get_available_signs()
        return {"signs": signs, "total": len(signs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get available signs: {str(e)}")
