"""
Video Processing Routes

Handles video upload, processing status, and retrieval of ASL narration results.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
from app.models.database import get_db
from app.models.schemas import (
    VideoUploadResponse,
    ProcessingStatus,
    NarrationResult,
    ErrorResponse
)
from app.models.db_models import Video
from app.services.video_service import VideoService
from app.services.processing_service import ProcessingService

router = APIRouter()

# Initialize services
video_service = VideoService()
processing_service = ProcessingService()


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a video file for ASL narration processing.
    
    Args:
        file: Video file (mp4, avi, mov, etc.)
        db: Database session
        
    Returns:
        VideoUploadResponse with video_id and status
    """
    try:
        # Validate file type
        allowed_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        video_id = await video_service.save_uploaded_video(file, db)
        
        return VideoUploadResponse(
            video_id=video_id,
            message="Video uploaded successfully",
            status="pending"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{video_id}/process")
async def process_video(
    video_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start processing a video to generate ASL narration.
    Processing happens in the background.
    
    Args:
        video_id: ID of uploaded video
        background_tasks: FastAPI background tasks
        db: Database session
    """
    # Check if video exists
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.status == "processing":
        raise HTTPException(status_code=400, detail="Video is already being processed")
    
    # Start background processing
    background_tasks.add_task(processing_service.process_video, video_id, db)
    
    return {"message": "Processing started", "video_id": video_id}


@router.get("/{video_id}/status", response_model=ProcessingStatus)
async def get_processing_status(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the current processing status of a video.
    
    Args:
        video_id: ID of the video
        db: Database session
        
    Returns:
        ProcessingStatus with current progress
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return ProcessingStatus(
        video_id=video_id,
        status=video.status,
        progress=video.progress,
        message=video.error_message
    )


@router.get("/{video_id}/result", response_model=NarrationResult)
async def get_narration_result(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the final ASL narration result for a video.
    
    Args:
        video_id: ID of the video
        db: Database session
        
    Returns:
        NarrationResult with ASL video and metadata
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Video processing not completed. Current status: {video.status}"
        )
    
    # Get detailed result from service
    result = await video_service.get_narration_result(video_id, db)
    return result


@router.get("/{video_id}/asl-video")
async def stream_asl_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Stream the generated ASL narration video.
    
    Args:
        video_id: ID of the video
        db: Database session
        
    Returns:
        Video file stream
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if not video.asl_video_path or not os.path.exists(video.asl_video_path):
        raise HTTPException(status_code=404, detail="ASL video not found")
    
    return FileResponse(
        video.asl_video_path,
        media_type="video/mp4",
        filename=f"asl_narration_{video_id}.mp4"
    )


@router.get("/")
async def list_videos(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List all uploaded videos with their status.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of videos with metadata
    """
    videos = db.query(Video).offset(skip).limit(limit).all()
    return {
        "videos": [
            {
                "id": v.id,
                "filename": v.filename,
                "status": v.status,
                "progress": v.progress,
                "created_at": v.created_at.isoformat()
            }
            for v in videos
        ],
        "total": db.query(Video).count()
    }

