"""
ASL Dataset Service

Handles operations on the ASL video dataset (saving, embedding generation).
"""

import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.db_models import ASLVideoDataset
import cv2
import numpy as np

class ASLDatasetService:
    """Service for managing ASL video dataset"""
    
    def __init__(self):
        self.storage_path = os.getenv("ASL_STORAGE_PATH", "storage/asl_clips")
        self.embeddings_path = os.getenv("EMBEDDINGS_PATH", "storage/embeddings")
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.embeddings_path, exist_ok=True)
    
    async def save_asl_video(self, file: UploadFile, gloss: str) -> str:
        """
        Save an uploaded ASL video file.
        
        Args:
            file: Uploaded ASL video file
            gloss: ASL gloss identifier
            
        Returns:
            file_path: Path to saved file
        """
        # Create safe filename from gloss
        safe_gloss = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in gloss)
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{safe_gloss}_{os.urandom(4).hex()}{file_ext}"
        file_path = os.path.join(self.storage_path, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    async def get_video_duration(self, file_path: str) -> float:
        """
        Get duration of a video file in seconds.
        
        Args:
            file_path: Path to video file
            
        Returns:
            duration: Duration in seconds
        """
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                return 0.0
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps > 0 else 0.0
            
            cap.release()
            return duration
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return 0.0
    
    async def generate_embedding(self, video_id: str, file_path: str, db: Session):
        """
        Generate and save embedding for an ASL video.
        This is used for similarity search.
        
        Args:
            video_id: ID of the ASL video
            file_path: Path to ASL video file
            db: Database session
        """
        try:
            # Import embedding generator from ML pipeline
            import sys
            current_file = os.path.abspath(__file__)
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            project_root = os.path.dirname(backend_dir)
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from ml_pipeline.asl_retrieval import ASLRetriever
            
            retriever = ASLRetriever()
            embedding = await retriever.generate_video_embedding(file_path)
            
            # Save embedding
            embedding_path = os.path.join(self.embeddings_path, f"{video_id}.npy")
            np.save(embedding_path, embedding)
            
            # Update database record
            video = db.query(ASLVideoDataset).filter(ASLVideoDataset.id == video_id).first()
            if video:
                video.embedding_path = embedding_path
                db.commit()
        except Exception as e:
            print(f"Error generating embedding for {video_id}: {e}")

