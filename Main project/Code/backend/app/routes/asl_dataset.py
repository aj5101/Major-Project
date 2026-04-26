"""
ASL Dataset Management Routes

Admin routes for managing the ASL video dataset (add, update, delete clips).
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from app.models.database import get_db
from app.models.schemas import ASLVideoMetadata, ASLVideoCreate
from app.models.db_models import ASLVideoDataset
from app.services.asl_dataset_service import ASLDatasetService

router = APIRouter()
dataset_service = ASLDatasetService()


@router.post("/", response_model=ASLVideoMetadata)
async def add_asl_video(
    gloss: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Add a new ASL video clip to the dataset.
    
    Args:
        gloss: ASL gloss (sign name/identifier)
        file: ASL video file
        db: Database session
        
    Returns:
        ASLVideoMetadata of the added video
    """
    try:
        # Save the ASL video file
        video_path = await dataset_service.save_asl_video(file, gloss)
        
        # Get video duration
        duration = await dataset_service.get_video_duration(video_path)
        
        # Create database record
        asl_video = ASLVideoDataset(
            gloss=gloss.lower().strip(),
            file_path=video_path,
            duration=duration
        )
        db.add(asl_video)
        db.commit()
        db.refresh(asl_video)
        
        # Generate embedding for this video (background task)
        await dataset_service.generate_embedding(asl_video.id, video_path, db)
        
        return ASLVideoMetadata(
            video_id=asl_video.id,
            gloss=asl_video.gloss,
            file_path=asl_video.file_path,
            duration=asl_video.duration
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ASLVideoMetadata])
async def list_asl_videos(
    skip: int = 0,
    limit: int = 100,
    gloss: str = None,
    db: Session = Depends(get_db)
):
    """
    List ASL videos in the dataset.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        gloss: Filter by gloss (optional)
        db: Database session
        
    Returns:
        List of ASLVideoMetadata
    """
    query = db.query(ASLVideoDataset).filter(ASLVideoDataset.is_active == True)
    
    if gloss:
        query = query.filter(ASLVideoDataset.gloss.ilike(f"%{gloss}%"))
    
    videos = query.offset(skip).limit(limit).all()
    
    return [
        ASLVideoMetadata(
            video_id=v.id,
            gloss=v.gloss,
            file_path=v.file_path,
            duration=v.duration,
            embedding_path=v.embedding_path
        )
        for v in videos
    ]


@router.get("/{video_id}/video")
async def stream_asl_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Stream an ASL video file.
    
    Args:
        video_id: ID of the ASL video
        db: Database session
        
    Returns:
        Video file stream
    """
    video = db.query(ASLVideoDataset).filter(ASLVideoDataset.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="ASL video not found")
    
    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        video.file_path,
        media_type="video/mp4",
        filename=f"asl_{video.gloss}.mp4"
    )


@router.get("/{video_id}", response_model=ASLVideoMetadata)
async def get_asl_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific ASL video.
    
    Args:
        video_id: ID of the ASL video
        db: Database session
        
    Returns:
        ASLVideoMetadata
    """
    video = db.query(ASLVideoDataset).filter(ASLVideoDataset.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="ASL video not found")
    
    return ASLVideoMetadata(
        video_id=video.id,
        gloss=video.gloss,
        file_path=video.file_path,
        duration=video.duration,
        embedding_path=video.embedding_path
    )


@router.delete("/{video_id}")
async def delete_asl_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Soft delete an ASL video (marks as inactive).
    
    Args:
        video_id: ID of the ASL video
        db: Database session
        
    Returns:
        Success message
    """
    video = db.query(ASLVideoDataset).filter(ASLVideoDataset.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="ASL video not found")
    
    video.is_active = False
    db.commit()
    
    return {"message": "ASL video deleted successfully"}


@router.post("/{video_id}/regenerate-embedding")
async def regenerate_embedding(
    video_id: str,
    db: Session = Depends(get_db)
):
    """
    Regenerate the embedding for an ASL video.
    Useful when embedding model is updated.
    
    Args:
        video_id: ID of the ASL video
        db: Database session
        
    Returns:
        Success message
    """
    video = db.query(ASLVideoDataset).filter(ASLVideoDataset.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="ASL video not found")
    
    await dataset_service.generate_embedding(video_id, video.file_path, db)
    
    return {"message": "Embedding regenerated successfully"}

