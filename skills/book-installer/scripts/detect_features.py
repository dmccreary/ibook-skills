#!/usr/bin/env python3
"""
Feature Detection Script for Intelligent Textbooks

Scans an MkDocs Material project to detect which features are implemented.
Outputs a JSON file with detection results that can be used to generate
a feature-checklist.md file.

Usage:
    python detect-features.py /path/to/project [--output results.json]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_mkdocs_yml(project_path: Path) -> dict:
    """Load and parse mkdocs.yml file."""
    mkdocs_path = project_path / "mkdocs.yml"
    if not mkdocs_path.exists():
        return {}

    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Strip !!python/name: tags that safe_load rejects — we only need
    # the surrounding config keys, not the Python objects themselves.
    raw = re.sub(r'!!python/name:\S+', '""', raw)

    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError as e:
        print(f"Warning: Error parsing mkdocs.yml: {e}")
        return {}


def get_theme_features(config: dict) -> list:
    """Extract theme features from config."""
    theme = config.get('theme', {})
    if isinstance(theme, dict):
        return theme.get('features', []) or []
    return []


def get_markdown_extensions(config: dict) -> list:
    """Extract markdown extensions from config."""
    return config.get('markdown_extensions', []) or []


def get_plugins(config: dict) -> list:
    """Extract plugins from config."""
    plugins = config.get('plugins', []) or []
    # Normalize to list of strings
    result = []
    for p in plugins:
        if isinstance(p, str):
            result.append(p)
        elif isinstance(p, dict):
            result.extend(p.keys())
    return result


def get_extra_javascript(config: dict) -> list:
    """Extract extra JavaScript files from config."""
    return config.get('extra_javascript', []) or []


def get_extra_css(config: dict) -> list:
    """Extract extra CSS files from config."""
    return config.get('extra_css', []) or []


def get_hooks(config: dict) -> list:
    """Extract MkDocs hook paths from config."""
    hooks = config.get('hooks', []) or []
    return [str(hook) for hook in hooks]


def count_files(directory: Path, pattern: str) -> int:
    """Count files matching a glob pattern."""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def count_directories(directory: Path) -> int:
    """Count subdirectories in a directory."""
    if not directory.exists():
        return 0
    return len([d for d in directory.iterdir() if d.is_dir()])


def count_chapters(chapters_path: Path) -> int:
    """Count directory-based or flat-file chapters without counting indexes."""
    if not chapters_path.exists():
        return 0

    chapter_directories = [
        path for path in chapters_path.iterdir()
        if path.is_dir() and not path.name.startswith('.')
    ]
    if chapter_directories:
        return len(chapter_directories)

    numbered_chapters = [
        path for path in chapters_path.glob("*.md")
        if re.match(r'^\d+[._-].+\.md$', path.name)
    ]
    if numbered_chapters:
        return len(numbered_chapters)

    return len([
        path for path in chapters_path.glob("*.md")
        if path.name.lower() not in {"index.md", "readme.md"}
    ])


def count_microsims(sims_path: Path) -> int:
    """Count runnable MicroSim directories, excluding shared utilities."""
    if not sims_path.exists():
        return 0
    return len([
        path for path in sims_path.iterdir()
        if path.is_dir() and (path / "main.html").is_file()
    ])


def has_social_media_cards(project_path: Path, plugins: list, hooks: list) -> bool:
    """Detect MkDocs social cards supplied by a plugin or a social hook."""
    if "social" in plugins:
        return True

    return any(
        "social" in Path(hook).name.lower() and (project_path / hook).is_file()
        for hook in hooks
    )


def has_graph_viewer(docs_path: Path) -> bool:
    """Detect the legacy MicroSim viewer or a learning-graph explorer."""
    if (docs_path / "sims" / "graph-viewer").is_dir():
        return True

    graph_path = docs_path / "learning-graph"
    return (
        (graph_path / "explorer.md").is_file()
        and any((graph_path / f"explorer.{suffix}").is_file() for suffix in ("html", "js"))
    )


def count_glossary_terms(glossary_path: Path) -> int:
    """Count terms in a glossary.md file (level 2, 3, or 4 headers after first heading)."""
    if not glossary_path.exists():
        return 0

    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count ## or ### or #### headers (glossary terms use various formats)
    # Most common: #### for terms (300 terms), ## for categories
    h4_count = len(re.findall(r'^#### ', content, re.MULTILINE))
    if h4_count > 10:  # If many h4 headers, this is the term format
        return h4_count

    h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
    if h3_count > 10:  # If many h3 headers, this is the term format
        return h3_count

    # Fall back to h2 count
    return len(re.findall(r'^## ', content, re.MULTILINE))


def count_faq_questions(faq_path: Path) -> int:
    """Count questions in a faq.md file (level 3 headers)."""
    if not faq_path.exists():
        return 0

    with open(faq_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count ### headers (FAQ questions)
    return len(re.findall(r'^### ', content, re.MULTILINE))


def file_exists(docs_path: Path, filename: str) -> bool:
    """Check if a file exists in docs directory."""
    return (docs_path / filename).exists()


def dir_exists(docs_path: Path, dirname: str) -> bool:
    """Check if a directory exists in docs directory."""
    return (docs_path / dirname).is_dir()


def extension_in_list(extensions: list, name: str) -> bool:
    """Check if an extension is in the list (handles dict format)."""
    for ext in extensions:
        if isinstance(ext, str) and ext == name:
            return True
        if isinstance(ext, dict) and name in ext:
            return True
    return False


def detect_features(project_path: Path) -> dict:
    """Detect all features in the project."""
    docs_path = project_path / "docs"
    config = load_mkdocs_yml(project_path)

    features = get_theme_features(config)
    extensions = get_markdown_extensions(config)
    plugins = get_plugins(config)
    extra_js = get_extra_javascript(config)
    extra_css = get_extra_css(config)
    hooks = get_hooks(config)
    theme = config.get('theme', {})
    extra = config.get('extra', {})

    # Convert extra_js to lowercase strings for checking
    extra_js_lower = [str(js).lower() for js in extra_js]

    results = {
        "project_path": str(project_path),
        "scan_date": datetime.now().isoformat(),
        "mkdocs_yml_found": (project_path / "mkdocs.yml").exists(),
        "docs_dir_found": docs_path.exists(),

        # Project info
        "site_name": config.get('site_name', 'Unknown'),
        "site_description": config.get('site_description', ''),
        "site_author": config.get('site_author', ''),

        # Counts
        "chapter_count": count_chapters(docs_path / "chapters"),
        "microsim_count": count_microsims(docs_path / "sims"),
        "glossary_term_count": count_glossary_terms(docs_path / "glossary.md"),
        "faq_question_count": count_faq_questions(docs_path / "faq.md"),
        "quiz_file_count": count_files(docs_path, "**/quiz.md"),

        # Basic Features
        "basic": {
            "navigation_sidebar": True,  # Always present
            "search_functionality": "search" in plugins or len(plugins) == 0,  # Default plugin
            "table_of_contents": True,  # Always present
            "site_title": bool(config.get('site_name')),
            "site_author": bool(config.get('site_author')),
            "github_repo": bool(config.get('repo_url')),
            "custom_logo": bool(theme.get('logo') if isinstance(theme, dict) else False),
            "custom_favicon": bool(theme.get('favicon') if isinstance(theme, dict) else False),
            "color_theme": bool(theme.get('palette') if isinstance(theme, dict) else False),
            "footer_navigation": "navigation.footer" in features,
            "navigation_expand": "navigation.expand" in features,
            "back_to_top": "navigation.top" in features,
            "breadcrumbs": "navigation.path" in features,
            "section_index": "navigation.indexes" in features,
            "license_page": file_exists(docs_path, "license.md"),
            "contact_page": file_exists(docs_path, "contact.md"),
            "about_page": file_exists(docs_path, "about.md"),
            "how_we_built": file_exists(docs_path, "how-we-built-this-site.md"),
            "copyright_footer": bool(config.get('copyright')),
        },

        # Content Enhancement Features
        "content_enhancement": {
            "glightbox": "glightbox" in plugins,
            "katex": (extension_in_list(extensions, "pymdownx.arithmatex") and
                     any("katex" in js for js in extra_js_lower)),
            "mathjax": (extension_in_list(extensions, "pymdownx.arithmatex") and
                       any("mathjax" in js for js in extra_js_lower)),
            "admonitions": extension_in_list(extensions, "admonition"),
            "code_copy_button": "content.code.copy" in features,
            "syntax_highlighting": extension_in_list(extensions, "pymdownx.highlight"),
            "tabbed_content": extension_in_list(extensions, "pymdownx.tabbed"),
            "task_lists": extension_in_list(extensions, "pymdownx.tasklist"),
            "mark_highlight": extension_in_list(extensions, "pymdownx.mark"),
            "strikethrough": extension_in_list(extensions, "pymdownx.tilde"),
            "magic_links": extension_in_list(extensions, "pymdownx.magiclink"),
            "snippets": extension_in_list(extensions, "pymdownx.snippets"),
            "emoji": extension_in_list(extensions, "pymdownx.emoji"),
            "collapsible_details": extension_in_list(extensions, "pymdownx.details"),
            "mermaid": extension_in_list(extensions, "pymdownx.superfences"),
        },

        # Site-Wide Resources
        "site_resources": {
            "glossary": file_exists(docs_path, "glossary.md"),
            "faq": file_exists(docs_path, "faq.md"),
            "references": file_exists(docs_path, "references.md"),
            "per_chapter_references": count_files(docs_path / "chapters", "**/references.md") > 0,
            "per_chapter_references_count": count_files(docs_path / "chapters", "**/references.md"),
            "custom_css": (len(list((docs_path / "css").glob("*.css")) if (docs_path / "css").exists() else []) > 0 or
                          len([c for c in extra_css if not c.startswith('http')]) > 0),
            "custom_js": (len(list((docs_path / "js").glob("*.js")) if (docs_path / "js").exists() else []) > 0 or
                         len([j for j in extra_js if not str(j).startswith('http')]) > 0),
            "google_analytics": bool(extra.get('analytics', {}).get('property') if isinstance(extra.get('analytics'), dict) else False),
            "document_status": bool(extra.get('status') if isinstance(extra.get('status'), dict) else False),
        },

        # Publishing Features
        "publishing": {
            "social_media_cards": has_social_media_cards(project_path, plugins, hooks),
            "edit_page_button": bool(config.get('edit_uri')) or "content.action.edit" in features,
        },

        # Advanced Features - Interactive Learning
        "interactive_learning": {
            "microsims": count_microsims(docs_path / "sims") > 0,
            "microsim_index": file_exists(docs_path / "sims", "index.md"),
            "per_chapter_quizzes": count_files(docs_path, "**/quiz.md") > 0,
        },

        # Learning Graph System
        "learning_graph": {
            "course_description": file_exists(docs_path, "course-description.md"),
            "learning_graph_csv": len(list((docs_path / "learning-graph").glob("*.csv")) if dir_exists(docs_path, "learning-graph") else []) > 0,
            "learning_graph_json": len(list((docs_path / "learning-graph").glob("*.json")) if dir_exists(docs_path, "learning-graph") else []) > 0,
            "graph_viewer": has_graph_viewer(docs_path),
            "concept_taxonomy": file_exists(docs_path / "learning-graph", "concept-taxonomy.md"),
            "concept_list": file_exists(docs_path / "learning-graph", "concept-list.md"),
            "quality_metrics": file_exists(docs_path / "learning-graph", "quality-metrics.md"),
            "book_metrics": file_exists(docs_path / "learning-graph", "book-metrics.md"),
            "chapter_metrics": file_exists(docs_path / "learning-graph", "chapter-metrics.md"),
            "glossary_quality_report": file_exists(docs_path / "learning-graph", "glossary-quality-report.md"),
            "faq_quality_report": file_exists(docs_path / "learning-graph", "faq-quality-report.md"),
            "faq_coverage_gaps": file_exists(docs_path / "learning-graph", "faq-coverage-gaps.md"),
            "quiz_generation_report": file_exists(docs_path / "learning-graph", "quiz-generation-report.md"),
            "reading_level_analysis": file_exists(docs_path / "learning-graph", "chapter-reading-levels.md"),
        },

        # Content Generation
        "content_generation": {
            "chapters": count_chapters(docs_path / "chapters") > 0,
            "pedagogical_agent": dir_exists(docs_path / "img", "mascot"),
            "prompts_collection": dir_exists(docs_path, "prompts"),
        },
    }

    return results


def generate_status_icon(detected: bool, partial: bool = False) -> str:
    """Generate the appropriate status icon."""
    if partial:
        return ":construction:"
    return ":white_check_mark:" if detected else ":x:"


def main():
    parser = argparse.ArgumentParser(
        description="Detect features in an MkDocs Material intelligent textbook project"
    )
    parser.add_argument(
        "project_path",
        type=str,
        help="Path to the project root (containing mkdocs.yml)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file path (default: stdout)"
    )
    parser.add_argument(
        "--pretty", "-p",
        action="store_true",
        help="Pretty-print JSON output"
    )

    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    if not (project_path / "mkdocs.yml").exists():
        print(f"Error: No mkdocs.yml found in {project_path}", file=sys.stderr)
        sys.exit(1)

    results = detect_features(project_path)

    indent = 2 if args.pretty else None
    json_output = json.dumps(results, indent=indent, default=str)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"Results written to: {output_path}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
