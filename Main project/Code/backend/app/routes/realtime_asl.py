"""
Real-Time ASL Generation API Route
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
from datetime import datetime
from typing import List

class Config:
    json_encoders = {
        'datetime': lambda v: v.isoformat()
    }

# Add project root to path to import generator
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from realtime_asl_generator import RealTimeASLGenerator
    print("✅ Successfully imported realtime_asl_generator")
except ImportError as e:
    print(f"❌ Failed to import realtime_asl_generator: {e}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    # Continue without raising exception

router = APIRouter()

class RealTimeASLRequest(BaseModel):
    user_input: str
    user_context: str = None

class RealTimeASLResponse(BaseModel):
    video_file: str
    concepts: List[str]
    asl_content: List[str]
    duration: float
    user_input: str
    created_at: str
    video_type: str

class Config:
    json_encoders = {
        'datetime': lambda v: v.isoformat()
    }

@router.post("/realtime-asl", response_model=RealTimeASLResponse)
async def generate_realtime_asl(request: RealTimeASLRequest):
    """
    Generate real-time ASL video based on user input.
    
    Args:
        request: User input and optional context
        
    Returns:
        Real-time ASL video generation response
    """
    try:
        generator = RealTimeASLGenerator()
        
        # Generate ASL video based on exact user input
        result = generator.generate_asl_from_prompt(request.user_input)
        
        return RealTimeASLResponse(
            video_file=result['video_file'],
            concepts=result['concepts'],
            asl_content=result['asl_content'],
            duration=result['duration'],
            user_input=result['user_input'],
            created_at=str(result['created_at']),
            video_type=str(result['video_type'])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate real-time ASL: {str(e)}")

@router.get("/realtime-history")
async def get_realtime_history():
    """
    Get history of real-time ASL generations.
    
    Returns:
        List of previous ASL generations
    """
    try:
        generator = RealTimeASLGenerator()
        
        # Get all metadata files
        history_path = generator.storage_path
        history = []
        
        if os.path.exists(history_path):
            for file in os.listdir(history_path):
                if file.endswith('.json'):
                    with open(os.path.join(history_path, file), 'r') as f:
                        metadata = json.load(f)
                        history.append({
                            'filename': metadata.get('video_file'),
                            'user_input': metadata.get('user_input'),
                            'concepts': metadata.get('concepts'),
                            'duration': metadata.get('duration'),
                            'created_at': metadata.get('created_at'),
                            'video_type': metadata.get('video_type')
                        })
        
        # Sort by creation time (newest first)
        history.sort(key=lambda x: x['created_at'], reverse=True)
        
        return {"history": history, "total": len(history)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")
