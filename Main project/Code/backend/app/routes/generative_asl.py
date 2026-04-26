from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.services.ai_agent_service import AIAgentService
from app.services.generative_asl_service import GenerativeASLService


router = APIRouter()


class GenerativeASLRequest(BaseModel):
    text: str
    # If provided, we use these tokens directly (useful for debugging)
    tokens: Optional[List[str]] = None


class GenerativeASLResponse(BaseModel):
    video_file: str
    tokens: List[str]
    duration: float
    text: str
    video_url: str
    created_at: str
    video_type: str


@router.post("/generate-asl-avatar", response_model=GenerativeASLResponse)
async def generate_asl_avatar(request: GenerativeASLRequest):
    """
    Fully generative (no pre-recorded clips) ASL-ish avatar video.

    Output is a simple 2D stick-figure animation driven by extracted keywords,
    with fingerspelling fallback so any input remains relevant.
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="text is required")

        ai = AIAgentService()

        # Keep tokens intentionally small + meaningful
        tokens = request.tokens
        if not tokens:
            # No "available signs" constraint here; we want semantic concepts,
            # and the renderer will fingerspell unknowns.
            tokens = ai._local_keywords(request.text)[:10]  # noqa: SLF001 (internal helper)

        gen = GenerativeASLService()
        result = gen.generate(request.text, tokens)

        return GenerativeASLResponse(
            video_file=result.video_file,
            tokens=result.tokens,
            duration=result.duration,
            text=request.text,
            video_url=f"/storage/processed/generative/{result.video_file}",
            created_at=result.created_at,
            video_type=result.video_type,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate avatar ASL video: {str(e)}")

