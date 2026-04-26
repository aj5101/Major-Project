"""
Lesson Mode API

Keeps the existing ASL pipeline intact while providing a teacher-friendly
JSON shape for classroom lesson generation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import re

from app.services.ai_agent_service import AIAgentService
from app.services.generative_asl_service import GenerativeASLService


router = APIRouter()


class LessonGenerateRequest(BaseModel):
    lesson_title: str = Field(default="Untitled lesson")
    text: str = Field(..., description="Full lesson text (2–10 short sentences recommended).")
    generate_videos: bool = Field(default=True, description="If false, only returns split + simplified text.")


class LessonSentence(BaseModel):
    text: str
    simplified: str
    asl_video_path: Optional[str] = None


class LessonGenerateResponse(BaseModel):
    lesson_title: str
    sentences: List[LessonSentence]


def _split_into_sentences(raw: str) -> List[str]:
    cleaned = re.sub(r"\s+", " ", (raw or "")).strip()
    if not cleaned:
        return []

    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", cleaned) if p.strip()]

    # If teacher pasted a long paragraph without punctuation, chunk by words.
    if len(parts) <= 1 and len(cleaned.split(" ")) > 16:
        words = cleaned.split(" ")
        chunk_size = 10
        return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return parts


def _simplify(sentence: str) -> str:
    # Lightweight simplification; avoids heavy model coupling in Lesson Mode.
    # The main video upload pipeline still uses the ML simplifier.
    s = (sentence or "").strip()
    s = re.sub(r"\btherefore\b", "so", s, flags=re.IGNORECASE)
    s = re.sub(r"\bhowever\b", "but", s, flags=re.IGNORECASE)
    s = re.sub(r"\bapproximately\b", "about", s, flags=re.IGNORECASE)
    s = re.sub(r"\butilize\b", "use", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", " ", s).strip()
    return s


@router.post("/lessons/generate", response_model=LessonGenerateResponse)
async def generate_lesson(request: LessonGenerateRequest):
    """
    Lesson Mode:
    - Accepts structured lesson text
    - Breaks into sentences
    - Produces simplified student-friendly sentences
    - Optionally generates an ASL avatar video per sentence

    This endpoint is intentionally minimal and reuses the existing generative avatar service.
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="text is required")

        sentences = _split_into_sentences(request.text)
        if not sentences:
            raise HTTPException(status_code=400, detail="No sentences found in lesson text")

        out: List[LessonSentence] = []

        ai = AIAgentService()
        gen = GenerativeASLService()

        for s in sentences:
            simplified = _simplify(s)
            asl_path = None

            if request.generate_videos:
                tokens = ai._local_keywords(simplified)[:10]  # noqa: SLF001
                result = gen.generate(simplified, tokens)
                asl_path = f"/storage/processed/generative/{result.video_file}"

            out.append(LessonSentence(text=s, simplified=simplified, asl_video_path=asl_path))

        return LessonGenerateResponse(
            lesson_title=(request.lesson_title or "Untitled lesson").strip() or "Untitled lesson",
            sentences=out,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

