"""
ASL Video Retrieval Module

Retrieves best-matching ASL video clips using:
1. Text-to-ASL gloss mapping
2. Vector similarity search on video embeddings
3. FAISS for efficient similarity search
"""

import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
import cv2
from app.models.db_models import ASLVideoDataset

class ASLRetriever:
    """
    Retrieves ASL video clips using semantic similarity.
    
    Uses sentence transformers to encode text queries and ASL video embeddings
    to find the best matching pre-recorded ASL clips.
    """
    
    def __init__(self):
        """Initialize retriever with embedding model"""
        model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.video_ids = []
        self.video_paths = []
        self._load_index()
    
    def _load_index(self):
        """
        Load or create FAISS index for ASL video embeddings.
        This allows fast similarity search.
        """
        index_path = os.getenv("FAISS_INDEX_PATH", "storage/faiss_index.bin")
        metadata_path = os.getenv("FAISS_METADATA_PATH", "storage/faiss_metadata.npz")
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            try:
                # Load existing index
                self.index = faiss.read_index(index_path)
                metadata = np.load(metadata_path, allow_pickle=True)
                self.video_ids = metadata["video_ids"].tolist()
                self.video_paths = metadata["video_paths"].tolist()
                print(f"Loaded FAISS index with {len(self.video_ids)} videos")
            except Exception as e:
                print(f"Error loading index: {e}, creating new index")
                self._create_empty_index()
        else:
            self._create_empty_index()
    
    def _create_empty_index(self):
        """Create empty FAISS index"""
        # Dimension for all-MiniLM-L6-v2 is 384
        dimension = 384
        self.index = faiss.IndexFlatL2(dimension)
        self.video_ids = []
        self.video_paths = []
        print("Created new FAISS index")
    
    async def generate_video_embedding(self, video_path: str) -> np.ndarray:
        """
        Generate embedding for an ASL video.
        
        Currently uses a simple approach: extract keyframes and use
        text-based embedding. In production, this could use video-specific
        models like CLIP or action recognition models.
        
        Args:
            video_path: Path to ASL video file
            
        Returns:
            embedding: Vector embedding of the video
        """
        try:
            # For now, we'll use the gloss text to generate embedding
            # In a more advanced system, you'd extract visual features from frames
            # This is a simplified approach
            
            # Extract filename/gloss from path
            filename = os.path.basename(video_path)
            # Assume gloss is in filename (can be improved)
            gloss = filename.split("_")[0] if "_" in filename else filename.split(".")[0]
            
            # Generate text embedding (as proxy for video content)
            # In production, use video feature extraction
            embedding = self.embedding_model.encode(gloss, convert_to_numpy=True)
            
            return embedding
            
        except Exception as e:
            print(f"Error generating video embedding: {e}")
            # Return zero vector as fallback
            return np.zeros(384, dtype=np.float32)
    
    async def retrieve(self, text: str, db: Session, top_k: int = 1) -> Optional[Dict]:
        """
        Retrieve best-matching ASL video for given text.
        
        Args:
            text: Text query (simplified phrase)
            db: Database session
            top_k: Number of top results to return
            
        Returns:
            best_match: Dictionary with video_id, file_path, confidence
        """
        if not text or not text.strip():
            return None
        
        try:
            # Generate embedding for query text
            query_embedding = self.embedding_model.encode(
                text.lower().strip(),
                convert_to_numpy=True
            ).reshape(1, -1).astype('float32')
            
            # Search in FAISS index
            if self.index.ntotal == 0:
                # Index is empty, try to build from database
                await self._rebuild_index(db)
            
            if self.index.ntotal == 0:
                # Still empty, try direct database lookup
                return await self._direct_database_lookup(text, db)
            
            # Search FAISS
            k = min(top_k, self.index.ntotal)
            distances, indices = self.index.search(query_embedding, k)
            
            if len(indices[0]) == 0:
                return await self._direct_database_lookup(text, db)
            
            # Get best match
            best_idx = indices[0][0]
            distance = distances[0][0]
            
            # Convert distance to confidence (lower distance = higher confidence)
            # Using simple inverse distance (can be improved)
            confidence = max(0.0, 1.0 - (distance / 10.0))
            
            video_id = self.video_ids[best_idx]
            file_path = self.video_paths[best_idx]
            
            # Verify video exists
            if not os.path.exists(file_path):
                return await self._direct_database_lookup(text, db)
            
            return {
                "video_id": video_id,
                "file_path": file_path,
                "confidence": float(confidence),
                "distance": float(distance)
            }
            
        except Exception as e:
            print(f"Error in ASL retrieval: {e}")
            return await self._direct_database_lookup(text, db)
    
    async def _rebuild_index(self, db: Session):
        """
        Rebuild FAISS index from database.
        
        Args:
            db: Database session
        """
        print("Rebuilding FAISS index from database...")
        
        videos = db.query(ASLVideoDataset).filter(ASLVideoDataset.is_active == True).all()
        
        if not videos:
            print("No ASL videos in database")
            return
        
        embeddings = []
        video_ids = []
        video_paths = []
        
        for video in videos:
            try:
                if video.embedding_path and os.path.exists(video.embedding_path):
                    embedding = np.load(video.embedding_path)
                else:
                    # Generate embedding on the fly
                    embedding = await self.generate_video_embedding(video.file_path)
                    # Save for future use
                    if not video.embedding_path:
                        embedding_dir = os.getenv("EMBEDDINGS_PATH", "storage/embeddings")
                        os.makedirs(embedding_dir, exist_ok=True)
                        embedding_path = os.path.join(embedding_dir, f"{video.id}.npy")
                        np.save(embedding_path, embedding)
                        video.embedding_path = embedding_path
                        db.commit()
                
                embeddings.append(embedding)
                video_ids.append(video.id)
                video_paths.append(video.file_path)
                
            except Exception as e:
                print(f"Error processing video {video.id}: {e}")
                continue
        
        if embeddings:
            # Create new index
            dimension = len(embeddings[0])
            self.index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
            
            # Save index and metadata
            index_path = os.getenv("FAISS_INDEX_PATH", "storage/faiss_index.bin")
            metadata_path = os.getenv("FAISS_METADATA_PATH", "storage/faiss_metadata.npz")
            
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            faiss.write_index(self.index, index_path)
            np.savez(metadata_path, video_ids=video_ids, video_paths=video_paths)
            
            self.video_ids = video_ids
            self.video_paths = video_paths
            
            print(f"Rebuilt index with {len(video_ids)} videos")
    
    async def _direct_database_lookup(self, text: str, db: Session) -> Optional[Dict]:
        """
        Fallback: Direct database lookup using gloss matching.
        
        Args:
            text: Query text
            db: Database session
            
        Returns:
            best_match or None
        """
        # Simple keyword matching on gloss
        words = text.lower().split()
        
        # Try to find videos with matching gloss
        for word in words:
            video = (
                db.query(ASLVideoDataset)
                .filter(ASLVideoDataset.gloss.ilike(f"%{word}%"))
                .filter(ASLVideoDataset.is_active == True)
                .first()
            )
            
            if video and os.path.exists(video.file_path):
                return {
                    "video_id": video.id,
                    "file_path": video.file_path,
                    "confidence": 0.5,  # Lower confidence for keyword match
                    "distance": 0.0
                }
        
        return None

