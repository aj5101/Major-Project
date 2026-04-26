"""
SQLAlchemy Database Models

This module defines the database table schemas using SQLAlchemy ORM.
These models represent the structure of data stored in PostgreSQL.
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import uuid


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


class Video(Base):
    """
    Model for uploaded videos that need ASL narration.
    
    Stores metadata about the original video and processing status.
    """
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    original_text = Column(Text, nullable=True)  # Transcribed text
    simplified_text = Column(Text, nullable=True)  # Simplified for children
    status = Column(String, default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)
    asl_video_path = Column(String, nullable=True)  # Path to generated ASL video
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship to ASL clips used in this video
    asl_clips = relationship("VideoASLClip", back_populates="video", cascade="all, delete-orphan")


class ASLVideoDataset(Base):
    """
    Model for ASL video clips in the dataset.
    
    Stores metadata about pre-recorded ASL videos that can be retrieved
    for narration generation.
    """
    __tablename__ = "asl_video_dataset"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    gloss = Column(String, nullable=False, index=True)  # ASL gloss (sign name)
    file_path = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    embedding_path = Column(String, nullable=True)  # Path to pre-computed embedding
    is_active = Column(Boolean, default=True)  # Can be disabled without deletion
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship to video clips that use this ASL video
    video_clips = relationship("VideoASLClip", back_populates="asl_video")


class VideoASLClip(Base):
    """
    Junction table linking videos to ASL clips used in narration.
    
    Tracks which ASL clips were used and their timing in the final video.
    """
    __tablename__ = "video_asl_clips"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    asl_video_id = Column(String, ForeignKey("asl_video_dataset.id"), nullable=False)
    start_time = Column(Float, nullable=False)  # Start time in final video
    end_time = Column(Float, nullable=False)  # End time in final video
    sequence_order = Column(Integer, nullable=False)  # Order in narration
    confidence = Column(Float, default=0.0)  # Matching confidence score
    
    # Relationships
    video = relationship("Video", back_populates="asl_clips")
    asl_video = relationship("ASLVideoDataset", back_populates="video_clips")

