import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter()


def _safe_join(base_dir: str, filename: str) -> str:
    # Prevent path traversal
    filename = os.path.basename(filename)
    return os.path.join(base_dir, filename)


@router.get("/generated/generative/{video_file}")
async def get_generative_video(video_file: str):
    """
    Stream a generated avatar MP4 with proper headers (Range support via FileResponse).
    """
    # project root: Code/ (two levels above backend/app)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    base_dir = os.path.join(project_root, "storage", "processed", "generative")
    path = _safe_join(base_dir, video_file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Generated video not found")
    return FileResponse(path, media_type="video/mp4", filename=video_file)

