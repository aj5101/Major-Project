"""
Video Processing Service

Handles the complete pipeline: speech-to-text, simplification, ASL retrieval, and video stitching.
"""

import os
import sys
from sqlalchemy.orm import Session
from app.models.db_models import Video, VideoASLClip, ASLVideoDataset
from app.models.database import SessionLocal

# Add ML pipeline to path (absolute path)
# Get the project root (3 levels up from this file)
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
project_root = os.path.dirname(backend_dir)
ml_pipeline_path = os.path.join(project_root, "ml_pipeline")
if os.path.exists(ml_pipeline_path) and ml_pipeline_path not in sys.path:
    sys.path.insert(0, project_root)  # Add project root so ml_pipeline can be imported

from ml_pipeline.speech_to_text import SpeechToText
from ml_pipeline.text_simplification import TextSimplifier
from ml_pipeline.asl_retrieval import ASLRetriever
from ml_pipeline.video_processing import VideoStitcher

class ProcessingService:
    """Service for processing videos through the ML pipeline"""
    
    def __init__(self):
        # Lazy initialization - only load models when needed
        self._stt = None
        self._simplifier = None
        self._asl_retriever = None
        self._video_stitcher = None
        self.asl_storage_path = os.getenv("ASL_STORAGE_PATH", "storage/asl_clips")
        self.output_path = os.getenv("OUTPUT_STORAGE_PATH", "storage/processed")
        os.makedirs(self.output_path, exist_ok=True)
    
    @property
    def stt(self):
        if self._stt is None:
            self._stt = SpeechToText()
        return self._stt
    
    @property
    def simplifier(self):
        if self._simplifier is None:
            self._simplifier = TextSimplifier()
        return self._simplifier
    
    @property
    def asl_retriever(self):
        if self._asl_retriever is None:
            self._asl_retriever = ASLRetriever()
        return self._asl_retriever
    
    @property
    def video_stitcher(self):
        if self._video_stitcher is None:
            self._video_stitcher = VideoStitcher()
        return self._video_stitcher
    
    async def process_video(self, video_id: str, db: Session = None):
        """
        Process a video through the complete pipeline.
        This runs in a background task.
        
        Args:
            video_id: ID of the video to process
            db: Database session (optional, creates new if None)
        """
        if db is None:
            db = SessionLocal()
        
        try:
            # Get video record
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                raise ValueError(f"Video {video_id} not found")
            
            # Update status
            video.status = "processing"
            video.progress = 0.1
            db.commit()
            
            # Step 1: Extract audio and convert to text
            print(f"Step 1: Transcribing audio for video {video_id}")
            original_text = await self.stt.transcribe(video.file_path)
            video.original_text = original_text
            video.progress = 0.3
            db.commit()
            
            if not original_text:
                raise ValueError("No speech detected in video")
            
            # Step 2: Simplify text for children
            print(f"Step 2: Simplifying text for video {video_id}")
            simplified_text = await self.simplifier.simplify(original_text, target_age=8)
            video.simplified_text = simplified_text
            video.progress = 0.5
            db.commit()
            
            # Step 3: Break into phrases and retrieve ASL clips
            print(f"Step 3: Retrieving ASL clips for video {video_id}")
            phrases = self._break_into_phrases(simplified_text)
            asl_clips = []
            
            for i, phrase in enumerate(phrases):
                if not phrase.strip():
                    continue
                
                # Retrieve best matching ASL video
                best_match = await self.asl_retriever.retrieve(phrase, db)
                
                if best_match:
                    # Create VideoASLClip record
                    clip = VideoASLClip(
                        video_id=video_id,
                        asl_video_id=best_match["video_id"],
                        sequence_order=i,
                        confidence=best_match["confidence"]
                    )
                    db.add(clip)
                    asl_clips.append({
                        "path": best_match["file_path"],
                        "confidence": best_match["confidence"]
                    })
                else:
                    # Use placeholder or skip
                    print(f"Warning: No ASL clip found for phrase: {phrase}")
            
            db.commit()
            video.progress = 0.7
            db.commit()
            
            # Step 4: Stitch ASL clips together
            if asl_clips:
                print(f"Step 4: Stitching ASL video for video {video_id}")
                output_path = os.path.join(
                    self.output_path,
                    f"asl_narration_{video_id}.mp4"
                )
                
                clip_paths = [clip["path"] for clip in asl_clips]
                await self.video_stitcher.stitch_clips(clip_paths, output_path)
                
                video.asl_video_path = output_path
                video.progress = 1.0
                video.status = "completed"
            else:
                video.status = "failed"
                video.error_message = "No ASL clips found for any phrases"
            
            db.commit()
            print(f"Processing completed for video {video_id}")
            
        except Exception as e:
            print(f"Error processing video {video_id}: {str(e)}")
            if db:
                video = db.query(Video).filter(Video.id == video_id).first()
                if video:
                    video.status = "failed"
                    video.error_message = str(e)
                    db.commit()
        finally:
            if db:
                db.close()
    
    def _break_into_phrases(self, text: str) -> list:
        """
        Break simplified text into ASL-friendly phrases.
        
        Args:
            text: Simplified text
            
        Returns:
            List of phrases
        """
        # Simple sentence splitting
        import re
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', text)
        phrases = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Further split long sentences (simple heuristic)
            words = sentence.split()
            if len(words) > 8:
                # Split into chunks of ~5 words
                chunk_size = 5
                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i:i+chunk_size])
                    phrases.append(chunk)
            else:
                phrases.append(sentence)
        
        return phrases

