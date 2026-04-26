"""
Video Service

Handles video file operations and retrieval of narration results.
"""

import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.db_models import Video, VideoASLClip
from app.models.schemas import NarrationResult, ASLClipInfo
from datetime import datetime

class VideoService:
    """Service for managing video files and metadata"""
    
    def __init__(self):
        self.storage_path = os.getenv("VIDEO_STORAGE_PATH", "storage/videos")
        os.makedirs(self.storage_path, exist_ok=True)
    
    async def save_uploaded_video(self, file: UploadFile, db: Session) -> str:
        """
        Save an uploaded video file to storage.
        
        Args:
            file: Uploaded file object
            db: Database session
            
        Returns:
            video_id: Unique identifier for the video
        """
        import uuid
        video_id = str(uuid.uuid4())
        
        # Create filename with video_id
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{video_id}{file_ext}"
        file_path = os.path.join(self.storage_path, filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create database record
        video = Video(
            id=video_id,
            filename=file.filename,
            file_path=file_path,
            status="pending"
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        
        return video_id
    
    async def get_narration_result(self, video_id: str, db: Session) -> NarrationResult:
        """
        Get complete narration result including ASL clips and metadata.
        
        Args:
            video_id: ID of the video
            db: Database session
            
        Returns:
            NarrationResult with all details
        """
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise ValueError(f"Video {video_id} not found")
        
        # Get ASL clips used in this video
        clips = (
            db.query(VideoASLClip)
            .filter(VideoASLClip.video_id == video_id)
            .order_by(VideoASLClip.sequence_order)
            .all()
        )
        
        asl_clips = [
            ASLClipInfo(
                clip_id=clip.id,
                gloss=clip.asl_video.gloss,
                start_time=clip.start_time,
                end_time=clip.end_time,
                confidence=clip.confidence
            )
            for clip in clips
        ]
        
        # Generate subtitles from simplified text
        subtitles = self._generate_subtitles(video.simplified_text, clips)
        
        return NarrationResult(
            video_id=video_id,
            original_text=video.original_text or "",
            simplified_text=video.simplified_text or "",
            asl_clips=asl_clips,
            asl_video_url=f"/api/videos/{video_id}/asl-video",
            subtitles=subtitles,
            created_at=video.created_at
        )
    
    def _generate_subtitles(self, text: str, clips: list) -> list:
        """
        Generate subtitle timings from text and ASL clips.
        
        Args:
            text: Simplified text
            clips: List of ASL clips with timing
            
        Returns:
            List of subtitle dictionaries
        """
        if not text or not clips:
            return []
        
        # Simple word-based subtitle generation
        words = text.split()
        subtitles = []
        current_time = 0.0
        
        for i, clip in enumerate(clips):
            clip_duration = clip.end_time - clip.start_time
            # Estimate words per clip (rough approximation)
            words_per_clip = max(1, len(words) // len(clips))
            start_idx = i * words_per_clip
            end_idx = min((i + 1) * words_per_clip, len(words))
            
            if start_idx < len(words):
                subtitle_text = " ".join(words[start_idx:end_idx])
                subtitles.append({
                    "text": subtitle_text,
                    "start_time": clip.start_time,
                    "end_time": clip.end_time
                })
        
        return subtitles

