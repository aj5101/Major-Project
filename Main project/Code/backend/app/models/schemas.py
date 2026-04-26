"""
Pydantic Schemas for Request/Response Validation

This module defines data models for API request and response validation
using Pydantic. These schemas ensure type safety and data validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VideoUploadResponse(BaseModel):
    """Response model for video upload"""
    video_id: str
    message: str
    status: str


class ProcessingStatus(BaseModel):
    """Status of video processing"""
    video_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: float  # 0.0 to 1.0
    message: Optional[str] = None


class ASLClipInfo(BaseModel):
    """Information about an ASL video clip"""
    clip_id: str
    gloss: str
    start_time: float
    end_time: float
    confidence: float


class NarrationResult(BaseModel):
    """Final narration result with ASL video"""
    video_id: str
    original_text: str
    simplified_text: str
    asl_clips: List[ASLClipInfo]
    asl_video_url: str
    subtitles: List[dict]  # List of {text, start_time, end_time}
    created_at: datetime


class ASLVideoMetadata(BaseModel):
    """Metadata for ASL video in dataset"""
    video_id: str
    gloss: str
    file_path: str
    duration: float
    embedding_path: Optional[str] = None


class ASLVideoCreate(BaseModel):
    """Schema for adding new ASL video to dataset"""
    gloss: str = Field(..., description="ASL gloss (sign name)")
    file_path: str = Field(..., description="Path to ASL video file")
    duration: Optional[float] = None


class TextSimplificationRequest(BaseModel):
    """Request for text simplification"""
    text: str
    target_age: int = Field(default=8, ge=6, le=12)


class ErrorResponse(BaseModel):
    """Error response model"""
    message: str
    error: Optional[str] = None
    video_id: Optional[str] = None

