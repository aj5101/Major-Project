"""
Embedding Generation Script

Regenerates embeddings for all ASL videos in the database.
Useful when:
- Embedding model is updated
- New videos are added
- FAISS index needs to be rebuilt
"""

import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models.database import SessionLocal
from app.models.db_models import ASLVideoDataset
from ml_pipeline.asl_retrieval import ASLRetriever
import numpy as np

async def regenerate_all_embeddings():
    """
    Regenerate embeddings for all ASL videos in database.
    """
    db = SessionLocal()
    retriever = ASLRetriever()
    
    try:
        videos = db.query(ASLVideoDataset).filter(ASLVideoDataset.is_active == True).all()
        print(f"Found {len(videos)} videos to process")
        
        embedding_dir = os.getenv("EMBEDDINGS_PATH", "storage/embeddings")
        os.makedirs(embedding_dir, exist_ok=True)
        
        processed = 0
        errors = 0
        
        for video in videos:
            try:
                print(f"Processing {video.gloss} ({video.id})...")
                
                # Generate embedding
                embedding = await retriever.generate_video_embedding(video.file_path)
                
                # Save embedding
                embedding_path = os.path.join(embedding_dir, f"{video.id}.npy")
                np.save(embedding_path, embedding)
                
                # Update database
                video.embedding_path = embedding_path
                db.commit()
                
                processed += 1
                print(f"  ✓ Processed {processed}/{len(videos)}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                errors += 1
                db.rollback()
                continue
        
        print(f"\nComplete: {processed} processed, {errors} errors")
        
        # Rebuild FAISS index
        print("\nRebuilding FAISS index...")
        await retriever._rebuild_index(db)
        print("FAISS index rebuilt")
        
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(regenerate_all_embeddings())

