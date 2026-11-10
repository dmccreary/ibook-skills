#!/usr/bin/env python3
"""
generate_cover.py

Generate a wide-landscape (1.91:1) social-preview cover image from a course description.

Pipeline:
1) Read course description text from a file.
2) Use the Responses API to extract visual motifs + produce a strong image prompt.
3) Use GPT Image (Images API) to generate a landscape image.
4) Center-crop to 1.91:1 and resize to 1200x630 (OG image standard).

Requirements:
  pip install openai pillow

Environment:
  export OPENAI_API_KEY="..."

Usage:
  python generate_cover.py --desc path/to/course_description.md --title "My Course Title"

  # Generate prompt only (for use with ChatGPT Plus):
  python generate_cover.py --desc path/to/course_description.md --title "My Course Title" --prompt-only

Optional:
  --out cover.png
  --text-model gpt-4o-mini
  --image-model gpt-image-2.6-sunburst
  --prompt-only  (output the image prompt without generating the image)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI
from PIL import Image


# ----------------------------
# Helpers
# ----------------------------

def read_text_file(path: str, max_chars: int = 40_000) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Keep it bounded (course descriptions can get big)
    return text[:max_chars]


def infer_title_from_markdown(text: str) -> Optional[str]:
    # Look for first Markdown H1: "# Title"
    m = re.search(r"^\s*#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Or a YAML front-matter title: title: ...
    m = re.search(r"^\s*title\s*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def safe_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", s).strip("_")
    return s[:120] if s else "cover"


def strip_markdown_code_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) if present."""
    text = text.strip()
    # Match ```json or ``` at start and ``` at end
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.match(pattern, text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def center_crop_to_aspect(img: Image.Image, target_aspect: float) -> Image.Image:
    """Center-crop PIL image to target aspect ratio (w/h)."""
    w, h = img.size
    current_aspect = w / h

    if abs(current_aspect - target_aspect) < 1e-6:
        return img

    if current_aspect > target_aspect:
        # too wide -> crop width
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        # too tall -> crop height
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


# ----------------------------
# Prompting (Responses API)
# ----------------------------

@dataclass
class CoverPlan:
    title: str
    theme_keywords: List[str]
    motifs: List[str]
    color_palette: List[str]
    composition_notes: str
    image_prompt: str


def build_cover_plan(
    client: OpenAI,
    description_text: str,
    title: str,
    text_model: str,
) -> CoverPlan:
    """
    Ask a text model to produce:
      - motifs (8-14)
      - palette (3-6)
      - composition notes
      - final, production-ready image prompt
    """
    schema_hint = {
        "title": "string",
        "theme_keywords": ["string"],
        "motifs": ["string"],
        "color_palette": ["string"],
        "composition_notes": "string",
        "image_prompt": "string",
    }

    instructions = (
        "You are a senior book-cover designer and prompt engineer.\n"
        "Given a course description, produce a strong art direction plan AND a final image prompt.\n"
        "Hard constraints:\n"
        "- The cover is a wide-landscape social preview image.\n"
        "- The TITLE text must be centered, large, crisp, high-contrast, readable.\n"
        "- Surround the title with a montage/collage of relevant visual elements derived from the description.\n"
        "- Avoid any other readable text besides the title.\n"
        "- No logos, no watermarks, no trademarks.\n"
        "- Keep it tasteful, modern, and not cluttered.\n"
        "Return ONLY valid JSON with keys exactly matching this schema:\n"
        f"{json.dumps(schema_hint, indent=2)}\n"
    )

    user_input = (
        f"TITLE:\n{title}\n\n"
        "COURSE DESCRIPTION:\n"
        f"{description_text}\n"
    )

    resp = client.responses.create(
        model=text_model,
        instructions=instructions,
        input=user_input,
    )

    # The Python SDK provides output_text convenience in many examples; fall back if missing.
    output_text = getattr(resp, "output_text", None)
    if not output_text:
        # Generic extraction fallback: find the first text output
        try:
            output_text = resp.output[0].content[0].text  # type: ignore[attr-defined]
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

    return CoverPlan(
        title=data["title"],
        theme_keywords=list(data.get("theme_keywords", [])),
        motifs=list(data.get("motifs", [])),
        color_palette=list(data.get("color_palette", [])),
        composition_notes=data.get("composition_notes", ""),
        image_prompt=data["image_prompt"],
    )


# ----------------------------
# Local Prompt Generation (No API)
# ----------------------------

def extract_keywords_from_text(text: str, max_keywords: int = 15) -> List[str]:
    """Extract likely topic keywords from course description text."""
    # Common words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
        'we', 'they', 'what', 'which', 'who', 'whom', 'when', 'where', 'why',
        'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then',
        'once', 'if', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'about', 'out', 'up',
        'down', 'off', 'over', 'any', 'our', 'your', 'their', 'its', 'his',
        'her', 'my', 'course', 'learn', 'student', 'students', 'understand',
        'understanding', 'knowledge', 'skills', 'concepts', 'introduction',
        'chapter', 'section', 'example', 'examples', 'using', 'used', 'use',
        'include', 'includes', 'including', 'based', 'well', 'new', 'first',
    }

    # Extract words (alphanumeric, 4+ chars)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

    # Count frequency, excluding stop words
    word_freq = {}
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def build_local_cover_plan(
    description_text: str,
    title: str,
) -> CoverPlan:
    """
    Build a cover plan locally without any API calls.
    Uses keyword extraction and templates.
    """
    keywords = extract_keywords_from_text(description_text)

    # Build a comprehensive image prompt
    keyword_str = ", ".join(keywords[:10]) if keywords else "technology, learning, education"

    image_prompt = (
        f"Please generate a new 1200x630 pixels (1.91:1 aspect ratio) image. "
        f"Create a modern, professional wide-landscape book cover for '{title}'. "
        f"The title '{title}' should be prominently displayed in large, crisp, "
        f"high-contrast white or light text, centered on the image. "
        f"The background should feature a sophisticated montage or abstract visualization "
        f"related to: {keyword_str}. "
        f"Use a modern color palette with deep blues, teals, and subtle accent colors. "
        f"The design should be clean, professional, and not cluttered. "
        f"No other text besides the title. No logos, watermarks, or trademarks. "
        f"Style: modern textbook cover, professional, educational, high-quality digital art."
    )

    return CoverPlan(
        title=title,
        theme_keywords=keywords[:10],
        motifs=keywords[5:12] if len(keywords) > 5 else keywords,
        color_palette=["deep blue", "teal", "white", "subtle orange accent"],
        composition_notes="Centered title with abstract/montage background",
        image_prompt=image_prompt,
    )


# ----------------------------
# Image Generation (Images API)
# ----------------------------

def generate_base_image_png(
    client: OpenAI,
    image_model: str,
    prompt: str,
    size: str = "1536x1024",  # GPT Image landscape option
    quality: str = "high",
) -> bytes:
    """
    Generate an image via Images API (GPT Image). Returns PNG bytes.
    Note: GPT Image models return base64-encoded image bytes in b64_json.
    """
    img = client.images.generate(
        model=image_model,
        prompt=prompt,
        size=size,
        quality=quality,
        # For GPT Image, output_format is supported (png/jpeg/webp). Default is png.
        output_format="png",
        n=1,
    )

    b64 = img.data[0].b64_json
    return base64.b64decode(b64)


def postprocess_to_og(
    png_bytes: bytes,
    out_path: str,
    target_size: Tuple[int, int] = (1200, 630),
    target_aspect: float = 1.91,
) -> None:
    """
    Crop to 1.91:1 and resize to 1200x630.
    """
    import io
    with Image.open(io.BytesIO(png_bytes)) as im:
        im = im.convert("RGBA")
        cropped = center_crop_to_aspect(im, target_aspect=target_aspect)
        resized = cropped.resize(target_size, resample=Image.LANCZOS)
        # Save as PNG (keeps crisp title text)
        resized.save(out_path, format="PNG")


# ----------------------------
# Main
# ----------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an OG/social cover image from a course description.")
    parser.add_argument("--desc", required=True, help="Path to course description file (Markdown/text).")
    parser.add_argument("--title", default=None, help="Cover title. If omitted, inferred from the file if possible.")
    parser.add_argument("--out", default=None, help="Output PNG path (default: derived from title).")
    parser.add_argument("--text-model", default=os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"),
                        help="Text model for planning/prompting (default: gpt-4o-mini).")
    parser.add_argument("--image-model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.6-sunburst"),
                        help="Image model (default: gpt-image-2.6-sunburst).")
    parser.add_argument("--debug-json", default=None,
                        help="Optional path to write the intermediate cover-plan JSON.")
    parser.add_argument("--prompt-only", action="store_true",
                        help="Only generate and display the image prompt (no image generation). "
                             "Use this to copy the prompt into ChatGPT Plus.")
    parser.add_argument("--local-prompt", action="store_true",
                        help="Generate prompt locally without any API calls. "
                             "Use this if you don't have API billing active.")
    parser.add_argument("--open-browser", action="store_true",
                        help="Open ChatGPT in browser and paste the prompt automatically. "
                             "Implies --local-prompt.")
    args = parser.parse_args()

    description_text = read_text_file(args.desc)
    title = args.title or infer_title_from_markdown(description_text) or "Untitled Course"

    out_path = args.out
    if not out_path:
        out_path = f"{safe_filename(title)}_og_1200x630.png"

    # Handle --open-browser (implies --local-prompt)
    if args.open_browser:
        args.local_prompt = True

    # 1) Build cover plan + final image prompt
    if args.local_prompt:
        # Generate prompt locally without API calls
        plan = build_local_cover_plan(
            description_text=description_text,
            title=title,
        )
        # Force prompt-only mode when using local prompt
        args.prompt_only = True
    else:
        client = OpenAI()  # reads OPENAI_API_KEY from environment
        plan = build_cover_plan(
            client=client,
            description_text=description_text,
            title=title,
            text_model=args.text_model,
        )

    if args.debug_json:
        with open(args.debug_json, "w", encoding="utf-8") as f:
            json.dump(plan.__dict__, f, indent=2, ensure_ascii=False)

    # If --prompt-only, display the prompt and exit
    if args.prompt_only:
        print("=" * 60)
        print("COVER IMAGE PROMPT")
        print("=" * 60)
        print(f"\nTitle: {plan.title}\n")
        if plan.theme_keywords:
            print(f"Keywords: {', '.join(plan.theme_keywords)}\n")
        if plan.motifs:
            print(f"Motifs: {', '.join(plan.motifs)}\n")
        if plan.color_palette:
            print(f"Color Palette: {', '.join(plan.color_palette)}\n")
        if plan.composition_notes:
            print(f"Composition: {plan.composition_notes}\n")
        print("-" * 60)
        print("IMAGE PROMPT (copy this into ChatGPT):")
        print("-" * 60)
        print(f"\n{plan.image_prompt}\n")
        print("=" * 60)

        # If --open-browser, launch ChatGPT and paste the prompt
        if args.open_browser:
            print("\nOpening ChatGPT and pasting prompt...")
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            browser_script = os.path.join(script_dir, "open-chatgpt.py")

            try:
                subprocess.run(
                    ["python", browser_script, plan.image_prompt],
                    check=True
                )
                print(f"\nAfter generating the image:")
                print(f"1. Download the image from ChatGPT")
                print(f"2. Save it to: {out_path}")
            except subprocess.CalledProcessError as e:
                print(f"\nFailed to open browser: {e}")
                print("The prompt is displayed above - copy it manually.")
            except FileNotFoundError:
                print(f"\nBrowser script not found: {browser_script}")
                print("The prompt is displayed above - copy it manually.")
        else:
            print("\nInstructions:")
            print("1. Copy the IMAGE PROMPT above")
            print("2. Paste it into ChatGPT Plus")
            print("3. Download the generated image")
            print(f"4. Save it to: {out_path}")
            print("5. Recommended size: 1200x630 pixels (1.91:1 aspect ratio)")
        return

    # 2) Generate base landscape image (GPT Image sizes are fixed; we crop later)
    base_png = generate_base_image_png(
        client=client,
        image_model=args.image_model,
        prompt=plan.image_prompt,
        size="1536x1024",
        quality="high",
    )

    # 3) Crop to 1.91:1 and resize to 1200x630 (OG)
    postprocess_to_og(
        png_bytes=base_png,
        out_path=out_path,
        target_size=(1200, 630),
        target_aspect=1.91,
    )

    print(f"Wrote: {out_path}")
    print(f"Title: {plan.title}")
    if plan.theme_keywords:
        print(f"Keywords: {', '.join(plan.theme_keywords[:10])}")


if __name__ == "__main__":
    main()
