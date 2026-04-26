"""
Real-Time ASL Generation API Route - Simplified
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
from datetime import datetime
from typing import List, Optional

class Config:
    json_encoders = {
        'datetime': lambda v: v.isoformat()
    }

class RealTimeASLRequest(BaseModel):
    user_input: str
    user_context: Optional[str] = None

class RealTimeASLResponse(BaseModel):
    video_file: str
    concepts: List[str]
    asl_content: List[str]
    duration: float
    user_input: str
    created_at: str
    video_type: str

# Add parent dir to path to import realtime_asl_generator
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from realtime_asl_generator import RealTimeASLGenerator
except ImportError as e:
    print(f"Error importing RealTimeASLGenerator: {e}")
    RealTimeASLGenerator = None

router = APIRouter()

@router.post("/realtime-asl", response_model=RealTimeASLResponse)
async def generate_realtime_asl(request: RealTimeASLRequest):
    """
    Generate real-time ASL video based on user input.
    """
    try:
        if not RealTimeASLGenerator:
            raise HTTPException(status_code=500, detail="RealTimeASLGenerator not available")
            
        generator = RealTimeASLGenerator()
        result = generator.generate_asl_from_prompt(request.user_input)
        
        return RealTimeASLResponse(
            video_file=result['video_file'],
            concepts=result['concepts'],
            asl_content=result['asl_content'],
            duration=result['duration'],
            user_input=result['user_input'],
            created_at=result['created_at'],
            video_type=result['video_type']
        )
        
    except Exception as e:
        print(f"Error in realtime-asl: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate real-time ASL: {str(e)}")

@router.get("/realtime-history")
async def get_realtime_history():
    """
    Get history of real-time ASL generations.
    """
    return {"history": [], "total": 0}
