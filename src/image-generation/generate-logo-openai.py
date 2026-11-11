#!/usr/bin/env python3
"""
generate_logo.py

Generate a minimalist square logo icon from a course description.

Pipeline:
1) Read course description text from a file.
2) Use the Responses API to identify the subject and produce a logo prompt.
3) Use GPT Image (Images API) to generate a square logo.
4) Resize to logo sizes (512x512 master, 64x64 for site).

Requirements:
  pip install openai pillow

Environment:
  export OPENAI_API_KEY="..."

Usage:
  python generate_logo.py --desc path/to/course_description.md

Optional:
  --out logo.png
  --text-model gpt-4o-mini
  --image-model gpt-image-2.6-sunburst
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from openai import OpenAI
from PIL import Image


# ----------------------------
# Theme Colors from mkdocs.yml
# ----------------------------
# Primary: Anthropic brown RGB(218, 120, 87) = #DA7857
# Accent: orange
PRIMARY_COLOR = "green"
ACCENT_COLOR = "yellow"


# ----------------------------
# Helpers
# ----------------------------

def read_text_file(path: str, max_chars: int = 40_000) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text[:max_chars]


def infer_title_from_markdown(text: str) -> Optional[str]:
    m = re.search(r"^\s*#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^\s*title\s*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def safe_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", s).strip("_")
    return s[:120] if s else "logo"


def strip_markdown_code_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) if present."""
    text = text.strip()
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.match(pattern, text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


# ----------------------------
# Prompting (Responses API)
# ----------------------------

@dataclass
class LogoPlan:
    subject: str
    icon_concept: str
    color: str
    image_prompt: str


def build_logo_plan(
    client: OpenAI,
    description_text: str,
    title: str,
    text_model: str,
) -> LogoPlan:
    """
    Ask a text model to produce:
      - subject (what the course is about)
      - icon_concept (what visual element represents it)
      - final image prompt for a minimalist logo
    """
    schema_hint = {
        "subject": "string (e.g., 'economics', 'data science')",
        "icon_concept": "string (e.g., 'supply and demand curves', 'bar chart')",
        "color": "string (hex color)",
        "image_prompt": "string",
    }

    instructions = f"""You are a professional logo designer and prompt engineer.
Given a course description, produce a logo design plan AND a final image prompt.

Hard constraints:
- The logo must be EXTREMELY minimalist - recognizable at 16x16 pixels
- Simple geometric shapes only
- Primary color: {PRIMARY_COLOR} (warm brown/terracotta)
- Transparent background
- Flat design, no gradients, no shadows
- NO text whatsoever
- Centered composition, square format
- Professional, clean lines
- Suitable for small size display (favicon, header logo)

The final image_prompt should follow this template:
"A minimalist [SUBJECT] logo icon, simple geometric shapes, [COLOR] on transparent background, flat design, suitable for small size display, professional, clean lines, no text, centered composition, square format"

Return ONLY valid JSON with keys exactly matching this schema:
{json.dumps(schema_hint, indent=2)}
"""

    user_input = (
        f"COURSE TITLE:\n{title}\n\n"
        "COURSE DESCRIPTION:\n"
        f"{description_text}\n"
    )

    resp = client.responses.create(
        model=text_model,
        instructions=instructions,
        input=user_input,
    )

    output_text = getattr(resp, "output_text", None)
    if not output_text:
        try:
            output_text = resp.output[0].content[0].text
        except Exception:
            raise RuntimeError("Could not extract text output from Responses API response.")

    try:
        clean_text = strip_markdown_code_fences(output_text)
        data = json.loads(clean_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Model did not return valid JSON. "
            "Tip: retry once or reduce description length.\n"
            f"Raw output:\n{output_text}"
        ) from e

    return LogoPlan(
        subject=data["subject"],
        icon_concept=data.get("icon_concept", ""),
        color=data.get("color", PRIMARY_COLOR),
        image_prompt=data["image_prompt"],
    )


# ----------------------------
# Image Generation (Images API)
# ----------------------------

def generate_base_image_png(
    client: OpenAI,
    image_model: str,
    prompt: str,
    size: str = "1024x1024",  # Square for logo
    quality: str = "high",
) -> bytes:
    """
    Generate an image via Images API (GPT Image). Returns PNG bytes.
    """
    img = client.images.generate(
        model=image_model,
        prompt=prompt,
        size=size,
        quality=quality,
        output_format="png",
        n=1,
    )

    b64 = img.data[0].b64_json
    return base64.b64decode(b64)


def postprocess_logo(
    png_bytes: bytes,
    out_path: str,
    target_size: Tuple[int, int] = (512, 512),
) -> None:
    """
    Resize logo to target size.
    """
    import io
    with Image.open(io.BytesIO(png_bytes)) as im:
        im = im.convert("RGBA")
        resized = im.resize(target_size, resample=Image.LANCZOS)
        resized.save(out_path, format="PNG")


# ----------------------------
# Main
# ----------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a minimalist logo icon from a course description.")
    parser.add_argument("--desc", required=True, help="Path to course description file (Markdown/text).")
    parser.add_argument("--title", default=None, help="Course title. If omitted, inferred from the file if possible.")
    parser.add_argument("--out", default=None, help="Output PNG path (default: logo.png).")
    parser.add_argument("--size", type=int, default=512, help="Output size in pixels (default: 512).")
    parser.add_argument("--text-model", default=os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"),
                        help="Text model for planning/prompting (default: gpt-4o-mini).")
    parser.add_argument("--image-model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.6-sunburst"),
                        help="Image model (default: gpt-image-2.6-sunburst).")
    parser.add_argument("--debug-json", default=None,
                        help="Optional path to write the intermediate logo-plan JSON.")
    args = parser.parse_args()

    description_text = read_text_file(args.desc)
    title = args.title or infer_title_from_markdown(description_text) or "Untitled Course"

    out_path = args.out
    if not out_path:
        out_path = f"{safe_filename(title)}_logo_{args.size}x{args.size}.png"

    client = OpenAI()

    print(f"Building logo plan for: {title}")
    print(f"Primary color: {PRIMARY_COLOR}")

    # 1) Build logo plan + final image prompt
    plan = build_logo_plan(
        client=client,
        description_text=description_text,
        title=title,
        text_model=args.text_model,
    )

    if args.debug_json:
        with open(args.debug_json, "w", encoding="utf-8") as f:
            json.dump(plan.__dict__, f, indent=2, ensure_ascii=False)

    print(f"Subject: {plan.subject}")
    print(f"Icon concept: {plan.icon_concept}")
    print(f"Generating image...")

    # 2) Generate square logo image
    base_png = generate_base_image_png(
        client=client,
        image_model=args.image_model,
        prompt=plan.image_prompt,
        size="1024x1024",
        quality="high",
    )

    # 3) Resize to target size
    postprocess_logo(
        png_bytes=base_png,
        out_path=out_path,
        target_size=(args.size, args.size),
    )

    print(f"Wrote: {out_path}")
    print(f"Size: {args.size}x{args.size}")


if __name__ == "__main__":
    main()
