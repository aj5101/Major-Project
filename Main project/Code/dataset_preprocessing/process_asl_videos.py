"""
ASL Video Dataset Preprocessing Script

Processes raw ASL video datasets (WLASL, ASL Lexicon, etc.) and:
1. Validates video files
2. Extracts metadata (gloss, duration, etc.)
3. Normalizes video format
4. Generates embeddings
5. Imports into database

Usage:
    python process_asl_videos.py --dataset_path /path/to/wlasl --gloss_file glosses.txt
"""

import os
import sys
import argparse
import cv2
from pathlib import Path
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models.database import SessionLocal, engine, Base
from app.models.db_models import ASLVideoDataset
from ml_pipeline.asl_retrieval import ASLRetriever

class ASLDatasetProcessor:
    """
    Processes ASL video datasets for use in the platform.
    
    Handles:
    - Video validation and normalization
    - Metadata extraction
    - Embedding generation
    - Database import
    """
    
    def __init__(self):
        self.retriever = ASLRetriever()
        self.storage_path = os.getenv("ASL_STORAGE_PATH", "storage/asl_clips")
        os.makedirs(self.storage_path, exist_ok=True)
    
    def process_dataset(self, dataset_path: str, gloss_mapping: dict = None):
        """
        Process an ASL video dataset.
        
        Args:
            dataset_path: Path to dataset directory
            gloss_mapping: Dictionary mapping filenames/video IDs to glosses
        """
        print(f"Processing dataset from: {dataset_path}")
        
        # Initialize database
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        
        try:
            # Find all video files
            video_files = self._find_video_files(dataset_path)
            print(f"Found {len(video_files)} video files")
            
            processed = 0
            skipped = 0
            errors = 0
            
            for video_path in video_files:
                try:
                    # Determine gloss
                    gloss = self._extract_gloss(video_path, gloss_mapping)
                    
                    if not gloss:
                        print(f"Warning: Could not determine gloss for {video_path}, skipping")
                        skipped += 1
                        continue
                    
                    # Validate video
                    if not self._validate_video(video_path):
                        print(f"Warning: Invalid video {video_path}, skipping")
                        skipped += 1
                        continue
                    
                    # Copy to storage
                    stored_path = self._copy_to_storage(video_path, gloss)
                    
                    # Get duration
                    duration = self._get_duration(video_path)
                    
                    # Check if already exists
                    existing = (
                        db.query(ASLVideoDataset)
                        .filter(ASLVideoDataset.gloss == gloss.lower())
                        .filter(ASLVideoDataset.file_path == stored_path)
                        .first()
                    )
                    
                    if existing:
                        print(f"Video already exists: {gloss}")
                        skipped += 1
                        continue
                    
                    # Create database record
                    asl_video = ASLVideoDataset(
                        gloss=gloss.lower().strip(),
                        file_path=stored_path,
                        duration=duration
                    )
                    db.add(asl_video)
                    db.commit()
                    db.refresh(asl_video)
                    
                    # Generate embedding
                    print(f"Generating embedding for {gloss}...")
                    import asyncio
                    embedding = asyncio.run(self.retriever.generate_video_embedding(stored_path))
                    
                    # Save embedding
                    embedding_dir = os.getenv("EMBEDDINGS_PATH", "storage/embeddings")
                    os.makedirs(embedding_dir, exist_ok=True)
                    embedding_path = os.path.join(embedding_dir, f"{asl_video.id}.npy")
                    import numpy as np
                    np.save(embedding_path, embedding)
                    
                    asl_video.embedding_path = embedding_path
                    db.commit()
                    
                    processed += 1
                    print(f"Processed {processed}/{len(video_files)}: {gloss}")
                    
                except Exception as e:
                    print(f"Error processing {video_path}: {e}")
                    errors += 1
                    db.rollback()
                    continue
            
            print(f"\nProcessing complete:")
            print(f"  Processed: {processed}")
            print(f"  Skipped: {skipped}")
            print(f"  Errors: {errors}")
            
        finally:
            db.close()
    
    def _find_video_files(self, directory: str) -> list:
        """
        Find all video files in directory (recursive).
        
        Args:
            directory: Root directory to search
            
        Returns:
            List of video file paths
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        video_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(os.path.join(root, file))
        
        return video_files
    
    def _extract_gloss(self, video_path: str, gloss_mapping: dict = None) -> str:
        """
        Extract ASL gloss from video path or mapping.
        
        Args:
            video_path: Path to video file
            gloss_mapping: Optional mapping dictionary
            
        Returns:
            gloss: ASL gloss identifier
        """
        if gloss_mapping:
            filename = os.path.basename(video_path)
            if filename in gloss_mapping:
                return gloss_mapping[filename]
        
        # Try to extract from filename
        filename = os.path.splitext(os.path.basename(video_path))[0]
        
        # Common patterns:
        # - "gloss_001.mp4" -> "gloss"
        # - "001_gloss.mp4" -> "gloss"
        # - "gloss.mp4" -> "gloss"
        
        # Remove numbers and underscores
        parts = filename.split('_')
        gloss = parts[0] if parts else filename
        
        # Remove leading/trailing numbers
        gloss = ''.join(c for c in gloss if not c.isdigit())
        
        return gloss.strip() if gloss else None
    
    def _validate_video(self, video_path: str) -> bool:
        """
        Validate that video file is readable and has valid format.
        
        Args:
            video_path: Path to video file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return False
            
            # Check if we can read at least one frame
            ret, frame = cap.read()
            cap.release()
            
            return ret and frame is not None
        except:
            return False
    
    def _get_duration(self, video_path: str) -> float:
        """
        Get video duration in seconds.
        
        Args:
            video_path: Path to video file
            
        Returns:
            duration: Duration in seconds
        """
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps > 0 else 0.0
            cap.release()
            return duration
        except:
            return 0.0
    
    def _copy_to_storage(self, source_path: str, gloss: str) -> str:
        """
        Copy video to storage directory with standardized naming.
        
        Args:
            source_path: Source video path
            gloss: ASL gloss identifier
            
        Returns:
            stored_path: Path in storage
        """
        import shutil
        import hashlib
        
        # Create safe filename
        safe_gloss = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in gloss)
        
        # Add hash to ensure uniqueness
        file_hash = hashlib.md5(source_path.encode()).hexdigest()[:8]
        file_ext = os.path.splitext(source_path)[1]
        
        filename = f"{safe_gloss}_{file_hash}{file_ext}"
        stored_path = os.path.join(self.storage_path, filename)
        
        # Copy file
        shutil.copy2(source_path, stored_path)
        
        return stored_path


def load_gloss_mapping(mapping_file: str) -> dict:
    """
    Load gloss mapping from file.
    
    Expected format: JSON or CSV with filename -> gloss mapping.
    
    Args:
        mapping_file: Path to mapping file
        
    Returns:
        Dictionary mapping filenames to glosses
    """
    if not os.path.exists(mapping_file):
        return {}
    
    if mapping_file.endswith('.json'):
        with open(mapping_file, 'r') as f:
            return json.load(f)
    elif mapping_file.endswith('.csv'):
        import csv
        mapping = {}
        with open(mapping_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    mapping[row[0]] = row[1]
        return mapping
    
    return {}


def main():
    """Main entry point for preprocessing script"""
    parser = argparse.ArgumentParser(description="Process ASL video dataset")
    parser.add_argument("--dataset_path", required=True, help="Path to dataset directory")
    parser.add_argument("--gloss_file", help="Path to gloss mapping file (JSON or CSV)")
    
    args = parser.parse_args()
    
    # Load gloss mapping if provided
    gloss_mapping = {}
    if args.gloss_file:
        gloss_mapping = load_gloss_mapping(args.gloss_file)
        print(f"Loaded {len(gloss_mapping)} gloss mappings")
    
    # Process dataset
    processor = ASLDatasetProcessor()
    processor.process_dataset(args.dataset_path, gloss_mapping)


if __name__ == "__main__":
    main()

