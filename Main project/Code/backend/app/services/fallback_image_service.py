"""
Fallback ASL Image Generator using Pillow
Creates clean ASL concept cards locally — no external API required.
"""

import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont


# Palette: one colour per concept index (cycles)
_PALETTE = [
    ("#4F46E5", "#EEF2FF"),  # indigo
    ("#0891B2", "#ECFEFF"),  # cyan
    ("#059669", "#ECFDF5"),  # emerald
    ("#D97706", "#FFFBEB"),  # amber
    ("#DC2626", "#FEF2F2"),  # red
    ("#7C3AED", "#F5F3FF"),  # violet
]

_HAND_EMOJI_FALLBACK = "🤟"   # shown as text when no emoji font available


def _draw_card(concept: str, image_number: int, size: int = 512) -> Image.Image:
    """Render a single ASL concept card."""
    fg, bg = _PALETTE[(image_number - 1) % len(_PALETTE)]

    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)

    # --- border ---
    border = 12
    draw.rounded_rectangle(
        [border, border, size - border, size - border],
        radius=32,
        outline=fg,
        width=6,
    )

    # --- top badge ---
    badge_h = 56
    draw.rounded_rectangle([border, border, size - border, border + badge_h],
                            radius=28, fill=fg)
    try:
        badge_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        badge_font = ImageFont.load_default()
    badge_text = "ASL SIGN"
    bw, bh = draw.textlength(badge_text, font=badge_font), 22
    draw.text(((size - bw) / 2, border + (badge_h - bh) / 2), badge_text,
              font=badge_font, fill="white")

    # --- hand icon (large circle placeholder) ---
    cx, cy, r = size // 2, size // 2 - 20, size // 5
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg, outline=fg)
    try:
        icon_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 80)
        draw.text((cx - 42, cy - 48), "🤟", font=icon_font, embedded_color=True)
    except Exception:
        # fallback: draw a simple hand outline
        try:
            icon_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 64)
        except Exception:
            icon_font = ImageFont.load_default()
        draw.text((cx - 20, cy - 32), "✋", font=icon_font, fill="white")

    # --- concept label ---
    label = concept.upper()
    try:
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except Exception:
        label_font = ImageFont.load_default()
    lw = draw.textlength(label, font=label_font)
    draw.text(((size - lw) / 2, size - 110), label, font=label_font, fill=fg)

    # --- subtitle ---
    sub = f"Sign #{image_number}"
    try:
        sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        sub_font = ImageFont.load_default()
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((size - sw) / 2, size - 58), sub, font=sub_font, fill="#6B7280")

    return img


def generate_concept_cards(
    concepts: List[str],
    storage_dir: str,
) -> Optional[List[Dict[str, Any]]]:
    """
    Generate one card per concept and save to storage_dir/processed/images/.
    Returns list of image metadata dicts compatible with working_image_service output.
    """
    image_dir = os.path.join(storage_dir, "processed", "images")
    os.makedirs(image_dir, exist_ok=True)

    results = []
    for i, concept in enumerate(concepts, start=1):
        try:
            img = _draw_card(concept, i)
            filename = f"asl_card_{uuid.uuid4().hex[:8]}_{i}.png"
            img.save(os.path.join(image_dir, filename), "PNG")
            results.append({
                "image_file": filename,
                "concept": concept,
                "image_number": i,
                "provider": "local-pillow",
            })
            print(f"🖼️  Generated card {i}: {concept} → {filename}")
        except Exception as e:
            print(f"❌ Failed to generate card for '{concept}': {e}")

    return results if results else None
