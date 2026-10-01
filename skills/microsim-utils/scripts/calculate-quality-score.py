#!/usr/bin/env python3
"""
Calculate quality scores for MicroSims based on the standardization rubric.

This script evaluates each MicroSim against the quality checklist and
updates the index.md file with the calculated quality_score.

Scoring Rubric (100 points total):
- Title in index.md (level 1 header): 2 pts
- main.html present: 10 pts
- YAML metadata (title & description): 3 pts
- Social preview images in YAML: 5 pts
- metadata.json present: 10 pts
- metadata.json Dublin Core fields present: 20 pts
  (a field-presence check, not JSON Schema validation; see check_metadata_json)
- iframe with src="main.html": 10 pts
- Fullscreen link button: 5 pts
- Copy-paste iframe example: 5 pts
- Screenshot image present: 5 pts
- Overview/Description section: 5 pts
- Lesson Plan section: 10 pts
- References section: 5 pts
- Type-specific (p5.js editor link): 5 pts

Usage:
    python calculate_quality_scores.py [--dry-run] [--verbose]
"""

import json
import re
import argparse
from pathlib import Path
import sys


# Dublin Core fields checked for the metadata.json presence score
REQUIRED_DUBLIN_CORE = [
    "title", "description", "creator", "date", "subject",
    "type", "format", "language", "rights"
]


def check_title_header(content: str) -> bool:
    """Check if index.md has a level 1 markdown header."""
    # Look for # Title after YAML frontmatter
    lines = content.split('\n')
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter and line.startswith('# '):
            return True
    return False


def check_main_html(sim_dir: Path) -> bool:
    """Check if main.html exists."""
    return (sim_dir / "main.html").exists()


def check_yaml_metadata(content: str) -> tuple[bool, bool]:
    """Check YAML frontmatter for title/description and image fields."""
    # Extract YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, False

    yaml_content = match.group(1)

    has_title_desc = ('title:' in yaml_content and 'description:' in yaml_content)
    has_images = ('image:' in yaml_content or 'og:image' in yaml_content)

    return has_title_desc, has_images


def check_metadata_json(sim_dir: Path) -> tuple[bool, bool]:
    """Check if metadata.json exists and has most Dublin Core fields.

    Returns (exists, has_dublin_core). This is a field-presence check, not
    validation against microsim-schema.json: most existing metadata.json files
    use a flat layout that the schema rejects. Switch to the real validator
    (src/microsim-schema/validate.py in the microsims repo) once metadata has
    been migrated to the schema.
    """
    metadata_path = sim_dir / "metadata.json"

    if not metadata_path.exists():
        return False, False

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Check for required Dublin Core fields
        # Handle both flat structure and nested microsim structure
        if "microsim" in metadata:
            dc = metadata.get("microsim", {}).get("dublinCore", {})
        else:
            dc = metadata

        missing_fields = []
        for field in REQUIRED_DUBLIN_CORE:
            if field not in dc or not dc[field]:
                missing_fields.append(field)

        is_valid = len(missing_fields) <= 2  # Allow up to 2 missing fields
        return True, is_valid

    except (json.JSONDecodeError, Exception):
        return True, False  # File exists but invalid JSON


def check_iframe(content: str) -> bool:
    """Check for iframe with src='main.html'."""
    return bool(re.search(r'<iframe[^>]*src=["\']main\.html["\']', content, re.IGNORECASE))


def check_fullscreen_button(content: str) -> bool:
    """Check for fullscreen link button."""
    patterns = [
        r'\[.*[Ff]ull\s*[Ss]creen.*\]\(main\.html\)',
        r'\[.*[Rr]un.*\]\(main\.html\).*\.md-button',
        r'\.md-button.*main\.html'
    ]
    for pattern in patterns:
        if re.search(pattern, content):
            return True
    return False


def check_iframe_example(content: str) -> bool:
    """Check for copy-paste iframe example in code block."""
    # Look for iframe in a code block (```html ... ```)
    code_blocks = re.findall(r'```(?:html)?\s*\n(.*?)\n```', content, re.DOTALL | re.IGNORECASE)
    for block in code_blocks:
        if '<iframe' in block.lower() and 'main.html' in block:
            return True
    return False


def check_screenshot(sim_dir: Path) -> bool:
    """Check if a screenshot PNG exists."""
    for png in sim_dir.glob("*.png"):
        # Exclude common non-screenshot files
        if png.name not in ['favicon.png', 'icon.png']:
            return True
    return False


def check_description_section(content: str) -> bool:
    """Check for description/overview section."""
    patterns = [
        r'^##\s+[Dd]escription',
        r'^##\s+[Aa]bout',
        r'^##\s+[Oo]verview',
        r'^##\s+[Hh]ow [Tt]o [Uu]se',
        r'^##\s+[Ii]ntroduction'
    ]
    for pattern in patterns:
        if re.search(pattern, content, re.MULTILINE):
            return True
    return False


def check_lesson_plan(content: str) -> bool:
    """Check for lesson plan section."""
    return bool(re.search(r'^##\s+[Ll]esson\s*[Pp]lan', content, re.MULTILINE))


def check_references(content: str) -> bool:
    """Check for references section."""
    return bool(re.search(r'^##\s+[Rr]eferences', content, re.MULTILINE))


def check_p5js_editor_link(sim_dir: Path, content: str) -> tuple[bool, bool]:
    """Check if MicroSim uses p5.js and has editor link."""
    main_html = sim_dir / "main.html"

    if not main_html.exists():
        return False, False

    try:
        with open(main_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception:
        return False, False

    # Check if p5.js is used
    is_p5js = bool(re.search(r'p5\.js|p5\.min\.js|p5js\.org', html_content, re.IGNORECASE))

    if not is_p5js:
        # Also check JS files
        for js_file in sim_dir.glob("*.js"):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                    if 'function setup()' in js_content and 'function draw()' in js_content:
                        is_p5js = True
                        break
            except Exception:
                pass

    if not is_p5js:
        return False, False  # Not a p5.js MicroSim

    # Check for p5.js editor link
    has_editor_link = bool(re.search(r'editor\.p5js\.org', content))

    return True, has_editor_link


def calculate_quality_score(sim_dir: Path, verbose: bool = False) -> tuple[int, dict]:
    """Calculate quality score for a MicroSim directory."""
    scores = {}
    details = {}

    # Read index.md
    index_md = sim_dir / "index.md"
    if not index_md.exists():
        return 0, {"error": "No index.md file"}

    try:
        with open(index_md, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 0, {"error": f"Cannot read index.md: {e}"}

    # 1. Title header (2 pts)
    has_title = check_title_header(content)
    scores['title'] = 2 if has_title else 0
    details['title'] = has_title

    # 2. main.html present (10 pts)
    has_main = check_main_html(sim_dir)
    scores['main_html'] = 10 if has_main else 0
    details['main_html'] = has_main

    # 3. YAML metadata - title & description (3 pts)
    has_yaml_basic, has_yaml_images = check_yaml_metadata(content)
    scores['yaml_basic'] = 3 if has_yaml_basic else 0
    details['yaml_basic'] = has_yaml_basic

    # 4. YAML metadata - images (5 pts)
    scores['yaml_images'] = 5 if has_yaml_images else 0
    details['yaml_images'] = has_yaml_images

    # 5. metadata.json present (10 pts)
    has_metadata, has_dublin_core = check_metadata_json(sim_dir)
    scores['metadata_present'] = 10 if has_metadata else 0
    details['metadata_present'] = has_metadata

    # 6. metadata.json Dublin Core fields present (20 pts)
    scores['metadata_dublin_core'] = 20 if has_dublin_core else 0
    details['metadata_dublin_core'] = has_dublin_core

    # 7. iframe embed (10 pts)
    has_iframe = check_iframe(content)
    scores['iframe'] = 10 if has_iframe else 0
    details['iframe'] = has_iframe

    # 8. Fullscreen button (5 pts)
    has_fullscreen = check_fullscreen_button(content)
    scores['fullscreen'] = 5 if has_fullscreen else 0
    details['fullscreen'] = has_fullscreen

    # 9. iframe example (5 pts)
    has_iframe_example = check_iframe_example(content)
    scores['iframe_example'] = 5 if has_iframe_example else 0
    details['iframe_example'] = has_iframe_example

    # 10. Screenshot (5 pts)
    has_screenshot = check_screenshot(sim_dir)
    scores['screenshot'] = 5 if has_screenshot else 0
    details['screenshot'] = has_screenshot

    # 11. Description section (5 pts)
    has_description = check_description_section(content)
    scores['description'] = 5 if has_description else 0
    details['description'] = has_description

    # 12. Lesson plan (10 pts)
    has_lesson_plan = check_lesson_plan(content)
    scores['lesson_plan'] = 10 if has_lesson_plan else 0
    details['lesson_plan'] = has_lesson_plan

    # 13. References (5 pts)
    has_references = check_references(content)
    scores['references'] = 5 if has_references else 0
    details['references'] = has_references

    # 14. Type-specific - p5.js editor link (5 pts)
    is_p5js, has_editor_link = check_p5js_editor_link(sim_dir, content)
    if is_p5js:
        scores['type_specific'] = 5 if has_editor_link else 0
        details['type_specific'] = f"p5.js: {'has' if has_editor_link else 'missing'} editor link"
    else:
        # Non-p5.js MicroSims get full points (or could check for other type-specific items)
        scores['type_specific'] = 5
        details['type_specific'] = "non-p5.js (full points)"

    total_score = sum(scores.values())

    if verbose:
        details['breakdown'] = scores

    return total_score, details


def get_existing_quality_score(content: str) -> int | None:
    """Extract existing quality_score from YAML frontmatter."""
    match = re.search(r'quality_score:\s*(\d+)', content)
    if match:
        return int(match.group(1))
    return None


def update_quality_score(index_md: Path, new_score: int, dry_run: bool = False) -> bool:
    """Update quality_score in index.md YAML frontmatter."""
    try:
        with open(index_md, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    # Check if YAML frontmatter exists
    if not content.startswith('---'):
        # Add frontmatter
        new_content = f"---\nquality_score: {new_score}\n---\n\n{content}"
    else:
        # Check if quality_score already exists
        if re.search(r'quality_score:\s*\d+', content):
            # Update existing score
            new_content = re.sub(
                r'quality_score:\s*\d+',
                f'quality_score: {new_score}',
                content
            )
        else:
            # Add quality_score after opening ---
            new_content = re.sub(
                r'^---\s*\n',
                f'---\nquality_score: {new_score}\n',
                content
            )

    if dry_run:
        return True

    try:
        with open(index_md, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Calculate and update quality scores for MicroSims."
    )
    parser.add_argument(
        "--sims-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "docs" / "sims",
        help="Path to the sims directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Calculate scores but don't update files"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed breakdown for each MicroSim"
    )
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only update MicroSims that don't have a quality_score"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="Only show MicroSims with score >= this value"
    )
    parser.add_argument(
        "--max-score",
        type=int,
        default=100,
        help="Only show MicroSims with score <= this value"
    )

    args = parser.parse_args()

    if not args.sims_dir.exists():
        print(f"Error: Sims directory not found: {args.sims_dir}")
        sys.exit(1)

    # Find all MicroSim directories
    microsim_dirs = sorted([
        d for d in args.sims_dir.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    ])

    print(f"Scanning {len(microsim_dirs)} MicroSim directories...\n")

    results = []
    updated_count = 0
    skipped_count = 0

    for sim_dir in microsim_dirs:
        index_md = sim_dir / "index.md"

        if not index_md.exists():
            if args.verbose:
                print(f"⚠️  {sim_dir.name}: No index.md file")
            continue

        # Read current content to check existing score
        with open(index_md, 'r', encoding='utf-8') as f:
            content = f.read()

        existing_score = get_existing_quality_score(content)

        # Skip if only processing missing scores
        if args.only_missing and existing_score is not None:
            skipped_count += 1
            continue

        # Calculate new score
        new_score, details = calculate_quality_score(sim_dir, args.verbose)

        # Filter by score range
        if new_score < args.min_score or new_score > args.max_score:
            continue

        # Determine if update needed
        score_changed = existing_score != new_score

        results.append({
            'name': sim_dir.name,
            'old_score': existing_score,
            'new_score': new_score,
            'changed': score_changed,
            'details': details
        })

        # Update file if needed
        if score_changed and not args.dry_run:
            if update_quality_score(index_md, new_score):
                updated_count += 1

    # Print results
    print(f"{'MicroSim':<40} {'Old':>5} {'New':>5} {'Status':<10}")
    print("-" * 65)

    for r in results:
        old_str = str(r['old_score']) if r['old_score'] is not None else "—"
        status = "updated" if r['changed'] else "unchanged"

        # Color coding
        if r['new_score'] >= 85:
            indicator = "✅"
        elif r['new_score'] >= 50:
            indicator = "🟡"
        else:
            indicator = "🔴"

        print(f"{indicator} {r['name']:<38} {old_str:>5} {r['new_score']:>5} {status:<10}")

        if args.verbose and 'breakdown' in r['details']:
            for key, value in r['details']['breakdown'].items():
                print(f"      {key}: {value}")
            print()

    # Summary
    print("-" * 65)
    print(f"\nSummary:")
    print(f"  Total MicroSims scanned: {len(microsim_dirs)}")
    print(f"  Scores calculated: {len(results)}")

    if args.only_missing:
        print(f"  Skipped (already had score): {skipped_count}")

    if args.dry_run:
        print(f"  Would update: {sum(1 for r in results if r['changed'])}")
        print("\n  (Dry run - no files modified)")
    else:
        print(f"  Files updated: {updated_count}")

    # Score distribution
    if results:
        scores = [r['new_score'] for r in results]
        avg_score = sum(scores) / len(scores)
        high_quality = sum(1 for s in scores if s >= 85)
        medium_quality = sum(1 for s in scores if 50 <= s < 85)
        low_quality = sum(1 for s in scores if s < 50)

        print(f"\nScore Distribution:")
        print(f"  Average score: {avg_score:.1f}")
        print(f"  High quality (≥85): {high_quality}")
        print(f"  Medium quality (50-84): {medium_quality}")
        print(f"  Low quality (<50): {low_quality}")


if __name__ == "__main__":
    main()
