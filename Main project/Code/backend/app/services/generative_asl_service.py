import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

import cv2
import numpy as np

try:
    import imageio.v2 as imageio  # type: ignore
    import imageio_ffmpeg  # type: ignore
except Exception:
    imageio = None
    imageio_ffmpeg = None


@dataclass
class GenerativeASLResult:
    video_file: str
    tokens: List[str]
    duration: float
    created_at: str
    video_type: str = "generative_avatar_2d"


class GenerativeASLService:
    """
    Generates a simple 2D "avatar" video without using pre-recorded sign clips.

    This is intentionally lightweight:
    - Stick figure body + simple arm/hand motion per token
    - Captioned with the token being "signed"
    - Unknown tokens fall back to fingerspelling (letter-by-letter)
    """

    def __init__(self):
        # This file lives at: Code/backend/app/services/...
        # Project root is: Code/
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.output_dir = os.path.join(project_root, "storage", "processed", "generative")
        os.makedirs(self.output_dir, exist_ok=True)

        self.width = int(os.getenv("GEN_AVATAR_WIDTH", "960"))
        # Use a height divisible by 16 for best H.264 compatibility.
        self.height = int(os.getenv("GEN_AVATAR_HEIGHT", "544"))
        self.fps = int(os.getenv("GEN_AVATAR_FPS", "24"))
        self.seconds_per_token = float(os.getenv("GEN_AVATAR_SECONDS_PER_TOKEN", "1.2"))

    def generate(self, text: str, tokens: List[str]) -> GenerativeASLResult:
        safe = re.sub(r"[^a-zA-Z0-9_\- ]+", "", text).strip().replace(" ", "_")[:24] or "text"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_file = f"gen_{safe}_{ts}.mp4"
        out_path = os.path.join(self.output_dir, video_file)

        rendered_tokens = self._expand_with_fingerspelling(tokens)
        frames = self._render_frames(rendered_tokens)

        self._write_mp4(out_path, frames)

        duration = len(frames) / float(self.fps) if frames else 0.0
        return GenerativeASLResult(
            video_file=video_file,
            tokens=rendered_tokens,
            duration=duration,
            created_at=datetime.now().isoformat(),
        )

    def _expand_with_fingerspelling(self, tokens: List[str]) -> List[str]:
        """
        Keep a small set of gestureable tokens. Everything else becomes
        FS-<letter> sequence so it's always relevant to the input.
        """
        gesture_vocab = {
            "hello",
            "learn",
            "teacher",
            "student",
            "school",
            "book",
            "science",
            "math",
            "question",
            "answer",
            "together",
            "knowledge",
        }

        expanded: List[str] = []
        for t in tokens:
            t = (t or "").strip().lower()
            if not t:
                continue
            if t in gesture_vocab:
                expanded.append(t)
                continue

            # Fingerspell unknown token (letters + digits)
            letters = re.findall(r"[a-z0-9]", t)
            if not letters:
                continue
            expanded.append("fs")
            expanded.extend([f"fs-{ch}" for ch in letters])
        return expanded[: int(os.getenv("ASL_MAX_SIGNS", "40"))]

    def _render_frames(self, tokens: List[str]) -> List[np.ndarray]:
        frames: List[np.ndarray] = []
        frames_per_token = max(8, int(self.seconds_per_token * self.fps))

        for token in tokens:
            for i in range(frames_per_token):
                t = i / max(1, frames_per_token - 1)
                frame = self._draw_avatar_frame(token, t)
                frames.append(frame)
        return frames

    def _draw_avatar_frame(self, token: str, t: float) -> np.ndarray:
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img[:] = (245, 247, 250)  # light background (BGR-ish feel)

        # Body anchor points
        cx, cy = self.width // 2, int(self.height * 0.55)
        head_r = int(min(self.width, self.height) * 0.06)
        neck = (cx, cy - int(self.height * 0.20))
        hip = (cx, cy + int(self.height * 0.10))

        # Draw head + torso
        cv2.circle(img, (cx, neck[1] - head_r - 8), head_r, (40, 40, 40), 3)
        cv2.line(img, neck, hip, (40, 40, 40), 4)

        # Legs
        leg_len = int(self.height * 0.18)
        cv2.line(img, hip, (cx - 40, hip[1] + leg_len), (40, 40, 40), 4)
        cv2.line(img, hip, (cx + 40, hip[1] + leg_len), (40, 40, 40), 4)

        # Arms: simple param motion depending on token
        shoulder_l = (cx - 60, neck[1] + 20)
        shoulder_r = (cx + 60, neck[1] + 20)

        elbow_l, hand_l = self._arm_pose("left", token, t, shoulder_l)
        elbow_r, hand_r = self._arm_pose("right", token, t, shoulder_r)

        cv2.line(img, shoulder_l, elbow_l, (40, 40, 40), 4)
        cv2.line(img, elbow_l, hand_l, (40, 40, 40), 4)
        cv2.line(img, shoulder_r, elbow_r, (40, 40, 40), 4)
        cv2.line(img, elbow_r, hand_r, (40, 40, 40), 4)

        # Simple hands
        cv2.circle(img, hand_l, 10, (60, 60, 60), -1)
        cv2.circle(img, hand_r, 10, (60, 60, 60), -1)

        # Caption bar
        bar_h = 64
        cv2.rectangle(img, (0, 0), (self.width, bar_h), (20, 20, 20), -1)
        label = token.upper()
        if token.startswith("fs-"):
            label = f"FINGERSPELL {token.split('-', 1)[1].upper()}"
        elif token == "fs":
            label = "FINGERSPELL"
        cv2.putText(
            img,
            label,
            (24, 44),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        return img

    def _arm_pose(self, side: str, token: str, t: float, shoulder: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        sx, sy = shoulder
        upper = 70
        lower = 70

        # Default resting
        ang1 = np.deg2rad(110 if side == "left" else 70)
        ang2 = np.deg2rad(140 if side == "left" else 40)

        # Token-based simple gestures (not linguistically perfect, but deterministic and distinct)
        if token == "hello":
            # Wave right hand
            if side == "right":
                ang1 = np.deg2rad(20 + 20 * np.sin(2 * np.pi * t))
                ang2 = np.deg2rad(40 + 25 * np.sin(2 * np.pi * t))
        elif token == "learn":
            # Bring hands toward head
            ang1 = np.deg2rad(300 if side == "left" else 240)
            ang2 = np.deg2rad(320 if side == "left" else 220)
        elif token in {"teacher", "student", "school"}:
            # Small chest-level motion
            ang1 = np.deg2rad(220 if side == "left" else 320)
            ang2 = np.deg2rad(260 if side == "left" else 280)
        elif token in {"math", "science", "knowledge"}:
            # Alternating hands up/down
            delta = 25 * np.sin(2 * np.pi * t)
            ang1 = np.deg2rad((250 + delta) if side == "left" else (290 - delta))
            ang2 = np.deg2rad((270 + delta) if side == "left" else (270 - delta))
        elif token.startswith("fs-") or token == "fs":
            # Hold hands centered
            ang1 = np.deg2rad(260 if side == "left" else 280)
            ang2 = np.deg2rad(270 if side == "left" else 270)

        ex = int(sx + upper * np.cos(ang1))
        ey = int(sy + upper * np.sin(ang1))
        hx = int(ex + lower * np.cos(ang2))
        hy = int(ey + lower * np.sin(ang2))
        return (ex, ey), (hx, hy)

    def _write_mp4(self, path: str, frames: List[np.ndarray]) -> None:
        if not frames:
            raise ValueError("No frames to write")
        # Best-effort: encode with FFmpeg (libx264 + yuv420p) for browser compatibility.
        # We use imageio-ffmpeg so we don't require system ffmpeg.
        if imageio is not None and imageio_ffmpeg is not None:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            os.environ.setdefault("IMAGEIO_FFMPEG_EXE", ffmpeg_exe)

            # imageio expects RGB frames
            with imageio.get_writer(
                path,
                fps=self.fps,
                codec="libx264",
                format="FFMPEG",
                ffmpeg_params=[
                    "-pix_fmt",
                    "yuv420p",
                    "-movflags",
                    "+faststart",
                ],
            ) as writer:
                for f in frames:
                    rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                    writer.append_data(rgb)
            return

        # Fallback: OpenCV (may produce unplayable MP4 on some machines/browsers)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(path, fourcc, self.fps, (self.width, self.height))
        if not writer.isOpened():
            writer.release()
            raise RuntimeError(
                "Failed to open OpenCV VideoWriter and FFmpeg encoder is unavailable. "
                "Install backend deps (imageio-ffmpeg) or install system FFmpeg."
            )
        try:
            for f in frames:
                writer.write(f)
        finally:
            writer.release()

