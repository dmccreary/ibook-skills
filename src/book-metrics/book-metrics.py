#!/usr/bin/env python3
"""
Book Metrics Generator

Generates comprehensive metrics for intelligent textbooks, including:
- Book-level metrics (overall statistics)
- Chapter-level metrics (per-chapter statistics)

Usage:
    python book-metrics.py [docs_directory]
"""

import re
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Version of the Book Metrics Generator
VERSION = "0.09"

# Version of the book-metrics.json file format (see book-metrics.schema.json).
# Bump only on a breaking change to the JSON structure, not on every code change.
METRICS_FILE_VERSION = "1.0"


class BookMetricsGenerator:
    """Generates metrics for intelligent textbooks."""

    # Directories to exclude from student-facing content metrics
    EXCLUDED_DIRS = {'prompts', 'learning-graph'}

    def __init__(self, docs_dir: str = "docs"):
        """Initialize the metrics generator.

        Args:
            docs_dir: Path to the docs directory (default: "docs")
        """
        self.docs_dir = Path(docs_dir)
        self.chapters_dir = self.docs_dir / "chapters"
        self.learning_graph_dir = self.docs_dir / "learning-graph"
        self.sims_dir = self.docs_dir / "sims"
        self.stories_dir = self.docs_dir / "stories"
        self.labs_dir = self.docs_dir / "labs"
        self.mascot_dir = self.docs_dir / "img" / "mascot"
        self.glossary_file = self.docs_dir / "glossary.md"
        self.faq_file = self.docs_dir / "faq.md"
        self.course_description_file = self.docs_dir / "course-description.md"
        # mkdocs.yml lives in the project root, one level above docs/
        self.mkdocs_file = self.docs_dir.parent / "mkdocs.yml"

        # Appendices directory - accept the correct spelling and the common
        # "appendicies" misspelling found in some textbook repos.
        self.appendices_dir = None
        for candidate in ("appendices", "appendicies"):
            candidate_dir = self.docs_dir / candidate
            if candidate_dir.exists():
                self.appendices_dir = candidate_dir
                break

    def _is_excluded_path(self, path: Path) -> bool:
        """Check if a path is in an excluded directory.

        Args:
            path: Path to check

        Returns:
            True if path is in an excluded directory
        """
        try:
            relative_path = path.relative_to(self.docs_dir)
            # Check if any parent directory is in excluded list
            return any(part in self.EXCLUDED_DIRS for part in relative_path.parts)
        except ValueError:
            # Path is not relative to docs_dir
            return False

    def count_chapters(self) -> Tuple[int, List[Dict[str, Any]]]:
        """Count number of chapter directories and collect chapter info.

        Returns:
            Tuple of (chapter_count, list of chapter info dicts)
        """
        chapters = []

        if not self.chapters_dir.exists():
            return 0, []

        # Look for directories with index.md files
        for item in sorted(self.chapters_dir.iterdir()):
            if item.is_dir() and (item / "index.md").exists():
                # Extract chapter number from directory name
                match = re.match(r'^0*(\d+)', item.name)
                if match:
                    chapter_num = int(match.group(1))
                    index_file = item / "index.md"

                    # Read chapter title from index.md
                    title = self._extract_title(index_file)

                    chapters.append({
                        'number': chapter_num,
                        'name': title,
                        'path': item,
                        'index_file': index_file
                    })

        return len(chapters), chapters

    def _extract_title(self, markdown_file: Path) -> str:
        """Extract the first H1 title from a markdown file.

        Args:
            markdown_file: Path to the markdown file

        Returns:
            The title string, or the filename if no title found
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.match(r'^#\s+(.+)$', line.strip())
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")

        return markdown_file.parent.name

    def count_concepts(self) -> int:
        """Count concepts from learning-graph.csv.

        Returns:
            Number of concepts
        """
        csv_file = self.learning_graph_dir / "learning-graph.csv"

        if not csv_file.exists():
            return 0

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return sum(1 for _ in reader)
        except Exception as e:
            print(f"Warning: Could not read learning graph CSV: {e}")
            return 0

    def count_glossary_terms(self) -> int:
        """Count glossary terms from glossary.md.

        Returns:
            Number of glossary terms
        """
        if not self.glossary_file.exists():
            return 0

        try:
            with open(self.glossary_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count H4 headers as glossary terms
                h4_count = len(re.findall(r'^####\s+', content, re.MULTILINE))
                return h4_count
        except Exception as e:
            print(f"Warning: Could not read glossary: {e}")
            return 0

    def count_faqs(self) -> int:
        """Count FAQ items from faq.md.

        Returns:
            Number of FAQ items
        """
        if not self.faq_file.exists():
            return 0

        try:
            with open(self.faq_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count H3 headers as FAQ questions (exactly 3 #, not 4+)
                # Use negative lookahead to exclude #### headers
                return len(re.findall(r'^###(?!#)\s+', content, re.MULTILINE))
        except Exception as e:
            print(f"Warning: Could not read FAQ: {e}")
            return 0

    def count_quiz_questions(self) -> int:
        """Count quiz questions across all chapters.

        Returns:
            Total number of quiz questions
        """
        total = 0

        if not self.chapters_dir.exists():
            return 0

        # Look for quiz.md files in chapter directories
        for chapter_dir in self.chapters_dir.iterdir():
            if chapter_dir.is_dir():
                quiz_file = chapter_dir / "quiz.md"
                if quiz_file.exists():
                    total += self._count_quiz_in_file(quiz_file)

        return total

    def _count_quiz_in_file(self, quiz_file: Path) -> int:
        """Count quiz questions in a single quiz file.

        Args:
            quiz_file: Path to quiz.md file

        Returns:
            Number of questions in the file
        """
        try:
            with open(quiz_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count H4 headers with numbered questions (e.g., "#### 1.")
                h4_pattern = len(re.findall(r'^####\s+\d+\.', content, re.MULTILINE))
                # Also count H2 headers as questions (legacy format)
                h2_pattern = len(re.findall(r'^##\s+', content, re.MULTILINE))
                return h4_pattern + h2_pattern
        except Exception as e:
            print(f"Warning: Could not read {quiz_file}: {e}")
            return 0

    def count_diagrams_in_file(self, markdown_file: Path) -> int:
        """Count diagrams in a single markdown file.

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of diagrams (H4 headers starting with "#### Diagram:")
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                return len(re.findall(r'^####\s+Diagram:', content, re.MULTILINE))
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0

    def count_all_diagrams(self, exclude_non_content: bool = True) -> int:
        """Count all diagrams in all markdown files.

        Args:
            exclude_non_content: If True, exclude prompts/ and learning-graph/ directories

        Returns:
            Total number of diagrams
        """
        total = 0

        # Search all markdown files in docs directory
        for md_file in self.docs_dir.rglob('*.md'):
            if exclude_non_content and self._is_excluded_path(md_file):
                continue
            total += self.count_diagrams_in_file(md_file)

        return total

    def count_equations_in_file(self, markdown_file: Path) -> int:
        """Count LaTeX equations in a single markdown file.

        Fixed to:
        1. Remove display math before counting inline math (avoids double-counting)
        2. Exclude dollar amounts like $500 from being counted as equations

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of equations (LaTeX expressions)
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Count display math: $$...$$ (must come first)
                display_matches = re.findall(r'\$\$[^$]+?\$\$', content, re.DOTALL)
                display = len(display_matches)

                # Remove all display math blocks to avoid double-counting
                content_no_display = re.sub(r'\$\$[^$]+?\$\$', '', content, flags=re.DOTALL)

                # Count inline math: $...$
                # Negative lookahead (?!\d) ensures we don't match dollar amounts like $500
                inline_matches = re.findall(r'\$(?!\d)([^\$]+?)\$', content_no_display)
                inline = len(inline_matches)

                return inline + display
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0

    def count_all_equations(self, exclude_non_content: bool = True) -> int:
        """Count all equations in all markdown files.

        Args:
            exclude_non_content: If True, exclude prompts/ and learning-graph/ directories

        Returns:
            Total number of equations
        """
        total = 0

        # Search all markdown files in docs directory
        for md_file in self.docs_dir.rglob('*.md'):
            if exclude_non_content and self._is_excluded_path(md_file):
                continue
            total += self.count_equations_in_file(md_file)

        return total

    def count_microsims(self) -> int:
        """Count MicroSim directories in docs/sims.

        Returns:
            Number of MicroSim directories
        """
        if not self.sims_dir.exists():
            return 0

        count = 0
        for item in self.sims_dir.iterdir():
            if item.is_dir() and (item / "index.md").exists():
                count += 1

        return count

    def count_species_cards(self) -> Dict[str, int]:
        """Count species cards and per-card asset coverage in docs/plants.

        Returns a dict with keys:
          total            — number of <slug>.md files in docs/plants/
          with_illustration — cards whose docs/plants/img/<slug>-illustration.png exists
          with_photos      — cards with at least one Wikipedia photo
          with_quick_facts — cards whose Quick Facts table has any non-empty cells
                             (i.e., something other than "—")

        Returns all zeros if docs/plants doesn't exist (project doesn't use
        the plant-gallery-generator skill)."""
        plants_dir = self.docs_dir / "plants"
        img_dir = plants_dir / "img"
        result = {
            "total": 0,
            "with_illustration": 0,
            "with_photos": 0,
            "with_quick_facts": 0,
        }
        if not plants_dir.exists():
            return result

        for card in plants_dir.iterdir():
            if not (card.is_file() and card.suffix == ".md"
                    and card.name != "index.md"):
                continue
            result["total"] += 1
            slug = card.stem
            try:
                text = card.read_text(encoding="utf-8")
            except Exception:
                continue
            if (img_dir / f"{slug}-illustration.png").exists():
                result["with_illustration"] += 1
            # Photo references in the card body, e.g. ![alt](img/<slug>-1.jpg)
            if f"{slug}-1.jpg" in text or f"{slug}-1.JPG" in text:
                result["with_photos"] += 1
            # Quick Facts populated: at least one DATA row (Family, Height,
            # Bloom time, Sun, Moisture, Soil, Wildlife value) has content
            # other than "—". The Scientific name row is auto-populated
            # and doesn't count.
            in_facts = False
            data_keys = {"family", "height", "bloom time", "sun",
                         "moisture", "soil", "wildlife value",
                         "hardiness zone", "native range"}
            for line in text.splitlines():
                if line.strip().startswith("## Quick Facts"):
                    in_facts = True
                    continue
                if in_facts:
                    if line.strip().startswith("## "):
                        break
                    if "|" in line and "---" not in line:
                        cells = [c.strip().strip("*").lower()
                                 for c in line.split("|")[1:-1]]
                        if len(cells) >= 2 and cells[0] in data_keys:
                            value = cells[1].strip("*")
                            if value and value != "—":
                                result["with_quick_facts"] += 1
                                break
        return result

    def count_host_plant_relationships(self) -> int:
        """Approximate count of host-plant relationships documented in
        chapter prose. Looks for the phrase 'host plant' or 'larval host'
        appearing near a species name. Useful for tracking pollinator-
        ecology coverage in textbooks.

        Returns 0 if no chapters use the convention. This is a soft
        metric — exact counts require a pollinator-host-plant matrix
        in structured data, which most textbooks don't have."""
        if not self.chapters_dir.exists():
            return 0
        count = 0
        for chapter in self.chapters_dir.iterdir():
            if not chapter.is_dir():
                continue
            index = chapter / "index.md"
            if not index.exists():
                continue
            try:
                text = index.read_text(encoding="utf-8").lower()
            except Exception:
                continue
            count += text.count("host plant")
            count += text.count("larval host")
        return count

    def count_stories(self) -> int:
        """Count stories in docs/stories.

        Each story is a subdirectory containing an index.md file (e.g.
        docs/stories/gregor-mendel/index.md). The top-level index.md and any
        "story ideas" markdown files are not counted.

        Returns:
            Number of story directories
        """
        if not self.stories_dir.exists():
            return 0

        count = 0
        for item in self.stories_dir.iterdir():
            if item.is_dir() and (item / "index.md").exists():
                count += 1

        return count

    def count_labs(self) -> int:
        """Count hands-on lab pages in docs/labs.

        Each lab is a subdirectory containing an index.md file (e.g.
        docs/labs/01-hello-world/index.md). The top-level index.md is not
        counted.

        Returns:
            Number of lab directories
        """
        if not self.labs_dir.exists():
            return 0

        count = 0
        for item in self.labs_dir.iterdir():
            if item.is_dir() and (item / "index.md").exists():
                count += 1

        return count

    def count_chapter_quizzes(self) -> int:
        """Count chapters that have a quiz.md file.

        This is distinct from the total number of quiz questions - it reports
        how many chapters provide a quiz at all.

        Returns:
            Number of chapters with a quiz.md file
        """
        if not self.chapters_dir.exists():
            return 0

        count = 0
        for chapter_dir in self.chapters_dir.iterdir():
            if chapter_dir.is_dir() and (chapter_dir / "quiz.md").exists():
                count += 1

        return count

    def count_chapter_references(self) -> Tuple[int, int]:
        """Count chapter reference files and total reference entries.

        References live in a references.md file inside each chapter directory.
        Each reference is a numbered list item (e.g. "1. [Title](url) - ...").

        Returns:
            Tuple of (number of chapters with references.md, total reference entries)
        """
        if not self.chapters_dir.exists():
            return 0, 0

        files = 0
        total_entries = 0
        for chapter_dir in self.chapters_dir.iterdir():
            if not chapter_dir.is_dir():
                continue
            ref_file = chapter_dir / "references.md"
            if not ref_file.exists():
                continue
            files += 1
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Count numbered list items (e.g. "1. ", "12. ")
                    total_entries += len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
            except Exception as e:
                print(f"Warning: Could not read {ref_file}: {e}")

        return files, total_entries

    def count_appendices(self) -> int:
        """Count appendix pages in the appendices directory.

        Counts markdown files (excluding index.md) in docs/appendices/ (or the
        "appendicies" misspelling). Subdirectories with their own index.md are
        also counted as a single appendix each.

        Returns:
            Number of appendix pages
        """
        if not self.appendices_dir:
            return 0

        count = 0
        for item in self.appendices_dir.iterdir():
            if item.is_file() and item.suffix == ".md" and item.name != "index.md":
                count += 1
            elif item.is_dir() and (item / "index.md").exists():
                count += 1

        return count

    def count_mascot_images(self) -> int:
        """Count mascot image files in docs/img/mascot.

        A mascot is optional. Books that have one typically provide several
        emotional-state poses (welcome, thinking, warning, celebration, etc.).

        Returns:
            Number of mascot image files (png/jpg/jpeg/gif/svg/webp)
        """
        if not self.mascot_dir.exists():
            return 0

        image_exts = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
        count = 0
        for item in self.mascot_dir.iterdir():
            if item.is_file() and item.suffix.lower() in image_exts:
                count += 1

        return count

    def get_development_stage(self) -> str:
        """Determine the book's development stage.

        Looks for a `development_stage` (or `development-stage`) value, first in
        mkdocs.yml (typically under the `extra:` block) and then in the
        course-description.md front matter. Returns "Not specified" when no
        value is found so the author knows to record one.

        Returns:
            The development stage string, or "Not specified"
        """
        stage_pattern = re.compile(
            r'^\s*development[-_]stage:\s*(.+?)\s*$',
            re.MULTILINE | re.IGNORECASE
        )

        for source in (self.mkdocs_file, self.course_description_file):
            if not source.exists():
                continue
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Warning: Could not read {source}: {e}")
                continue
            match = stage_pattern.search(content)
            if match:
                # Strip surrounding quotes if present
                return match.group(1).strip().strip('"').strip("'")

        return "Not specified"

    def count_words_in_file(self, markdown_file: Path) -> int:
        """Count words in a single markdown file.

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of words
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove code blocks
                content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                # Remove inline code
                content = re.sub(r'`[^`]+`', '', content)
                # Remove URLs
                content = re.sub(r'https?://\S+', '', content)
                # Count words
                words = re.findall(r'\b\w+\b', content)
                return len(words)
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0

    def count_total_words(self, exclude_non_content: bool = True) -> int:
        """Count total words in all markdown files.

        Args:
            exclude_non_content: If True, exclude prompts/ and learning-graph/ directories

        Returns:
            Total word count
        """
        total = 0

        # Search all markdown files in docs directory
        for md_file in self.docs_dir.rglob('*.md'):
            if exclude_non_content and self._is_excluded_path(md_file):
                continue
            total += self.count_words_in_file(md_file)

        return total

    def count_links_in_file(self, markdown_file: Path) -> int:
        """Count markdown links in a single file.

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of links
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count markdown links [text](url)
                return len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0

    def count_all_links(self, exclude_non_content: bool = True) -> int:
        """Count all links in all markdown files.

        Args:
            exclude_non_content: If True, exclude prompts/ and learning-graph/ directories

        Returns:
            Total number of links
        """
        total = 0

        # Search all markdown files in docs directory
        for md_file in self.docs_dir.rglob('*.md'):
            if exclude_non_content and self._is_excluded_path(md_file):
                continue
            total += self.count_links_in_file(md_file)

        return total

    def calculate_equivalent_pages(self, total_words: int, diagrams: int, microsims: int) -> int:
        """Calculate equivalent pages based on words, diagrams, and MicroSims.

        Assumptions:
        - 250 words per page
        - Each diagram takes 0.25 page
        - Each MicroSim takes 0.5 page

        Args:
            total_words: Total word count
            diagrams: Number of diagrams
            microsims: Number of MicroSims

        Returns:
            Estimated page count
        """
        words_per_page = 250
        diagram_pages = diagrams * 0.25
        microsim_pages = microsims * 0.5
        text_pages = total_words / words_per_page

        return int(text_pages + diagram_pages + microsim_pages)

    def count_sections_in_file(self, markdown_file: Path) -> int:
        """Count sections (H2 and H3 headers) in a markdown file.

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of sections
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
                h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
                return h2_count + h3_count
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0

    def get_chapter_metrics(self, chapter: Dict[str, Any]) -> Dict[str, Any]:
        """Get metrics for a single chapter.

        Args:
            chapter: Chapter info dict

        Returns:
            Dict with chapter metrics
        """
        index_file = chapter['index_file']
        chapter_dir = chapter['path']

        # Count sections in index.md
        sections = self.count_sections_in_file(index_file)

        # Count diagrams, equations, words, and links in all markdown files in chapter directory
        diagrams = 0
        equations = 0
        words = 0
        links = 0
        for md_file in chapter_dir.rglob('*.md'):
            diagrams += self.count_diagrams_in_file(md_file)
            equations += self.count_equations_in_file(md_file)
            words += self.count_words_in_file(md_file)
            links += self.count_links_in_file(md_file)

        # Quiz questions and references for this chapter
        quiz_file = chapter_dir / "quiz.md"
        quiz_questions = self._count_quiz_in_file(quiz_file) if quiz_file.exists() else 0

        ref_file = chapter_dir / "references.md"
        references = 0
        if ref_file.exists():
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    references = len(re.findall(r'^\s*\d+\.\s+', f.read(), re.MULTILINE))
            except Exception as e:
                print(f"Warning: Could not read {ref_file}: {e}")

        return {
            'number': chapter['number'],
            'name': chapter['name'],
            'sections': sections,
            'diagrams': diagrams,
            'equations': equations,
            'words': words,
            'links': links,
            'quiz_questions': quiz_questions,
            'references': references
        }

    def get_aggregated_chapter_metrics(self) -> Dict[str, int]:
        """Aggregate metrics across all chapters for comparison.

        Returns:
            Dict with aggregated metrics from all chapters
        """
        _, chapters = self.count_chapters()

        aggregated = {
            'diagrams': 0,
            'equations': 0,
            'words': 0,
            'links': 0
        }

        for chapter in chapters:
            metrics = self.get_chapter_metrics(chapter)
            aggregated['diagrams'] += metrics['diagrams']
            aggregated['equations'] += metrics['equations']
            aggregated['words'] += metrics['words']
            aggregated['links'] += metrics['links']

        return aggregated

    def generate_book_metrics_md(self) -> str:
        """Generate the book-metrics.md content.

        Returns:
            Markdown content as string
        """
        # Collect all metrics (excluding non-content directories)
        chapter_count, _ = self.count_chapters()
        concepts = self.count_concepts()
        glossary_terms = self.count_glossary_terms()
        faqs = self.count_faqs()
        quiz_questions = self.count_quiz_questions()
        chapter_quizzes = self.count_chapter_quizzes()
        ref_files, ref_entries = self.count_chapter_references()
        stories = self.count_stories()
        labs = self.count_labs()
        appendices = self.count_appendices()
        mascot_images = self.count_mascot_images()
        development_stage = self.get_development_stage()
        diagrams = self.count_all_diagrams(exclude_non_content=True)
        equations = self.count_all_equations(exclude_non_content=True)
        microsims = self.count_microsims()
        total_words = self.count_total_words(exclude_non_content=True)
        links = self.count_all_links(exclude_non_content=True)
        equivalent_pages = self.calculate_equivalent_pages(total_words, diagrams, microsims)

        # Botany / species-card metrics (only rendered when docs/plants/ exists)
        species = self.count_species_cards()
        host_relationships = self.count_host_plant_relationships()

        # Get chapter-aggregated metrics for comparison
        chapter_aggregated = self.get_aggregated_chapter_metrics()

        # Get current timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        # Helper: flag required elements that are still empty/unset
        def status_cell(label: str, value, empty) -> str:
            """Return the status text, adding a ⚠️ when a required element is missing."""
            if label == "Required" and value in empty:
                return "Required ⚠️"
            return label

        # Build markdown table
        md = "# Book Metrics\n\n"
        md += f"**Generated by**: Book Metrics Python Program v{VERSION}  \n"
        md += f"**Generated on**: {timestamp}\n\n"
        md += "This file contains overall metrics for the intelligent textbook.\n\n"
        md += "**Note**: Student-facing content metrics exclude `prompts/` and `learning-graph/` directories. "
        md += "Chapter-only metrics show what students see in the main chapters.\n\n"

        md += "## Book Composition\n\n"
        md += "The thirteen tracked elements of an intelligent textbook. The **Status** column "
        md += "shows whether each element is *Required*, *Recommended*, or *Optional*; a ⚠️ marks "
        md += "a required element that is still missing.\n\n"
        md += "| # | Element | Value | Status | Notes |\n"
        md += "|---|---------|-------|--------|-------|\n"
        md += f"| 1 | Concepts | {concepts} | {status_cell('Required', concepts, (0,))} | Concepts from learning graph |\n"
        md += f"| 2 | Chapters | {chapter_count} | {status_cell('Required', chapter_count, (0,))} | Chapter directories with index.md |\n"
        md += f"| 3 | MicroSims | {microsims} | Recommended | Interactive simulations in docs/sims/ |\n"
        md += f"| 4 | Stories | {stories} | Optional | Graphic-novel narratives in docs/stories/ |\n"
        md += f"| 5 | Chapter Quizzes | {chapter_quizzes} / {chapter_count} | Recommended | Chapters with a quiz.md ({quiz_questions} questions total) |\n"
        md += f"| 6 | Chapter References | {ref_files} / {chapter_count} | Recommended | Chapters with references.md ({ref_entries} references total) |\n"
        md += f"| 7 | Glossary Terms | {glossary_terms} | Recommended | Defined terms in glossary.md |\n"
        md += f"| 8 | FAQs | {faqs} | Recommended | Questions in faq.md |\n"
        md += f"| 9 | Words | {total_words:,} | {status_cell('Required', total_words, (0,))} | Words across student-facing markdown |\n"
        md += f"| 10 | Mascot | {mascot_images if mascot_images else 'None'} | Optional | Mascot image poses in docs/img/mascot/ |\n"
        md += f"| 11 | Appendices | {appendices} | Optional | Appendix pages |\n"
        md += f"| 12 | Development Stage | {development_stage} | {status_cell('Required', development_stage, ('Not specified',))} | From mkdocs.yml or course-description.md |\n"
        md += f"| 13 | Labs | {labs} | Optional | Hands-on lab pages in docs/labs/ |\n"

        md += "\n## Student-Facing Content Metrics\n\n"
        md += "Excludes administrative directories (`prompts/`, `learning-graph/`).\n\n"
        md += "| Metric Name | All Content | Chapters Only | Notes |\n"
        md += "|-------------|-------------|---------------|-------|\n"
        md += f"| Diagrams | {diagrams} | {chapter_aggregated['diagrams']} | H4 headers starting with '#### Diagram:' |\n"
        md += f"| Equations | {equations} | {chapter_aggregated['equations']} | LaTeX expressions (inline and display) |\n"
        md += f"| Total Words | {total_words:,} | {chapter_aggregated['words']:,} | Words in markdown files |\n"
        md += f"| Links | {links} | {chapter_aggregated['links']} | Hyperlinks in markdown format |\n"
        md += f"| Equivalent Pages | {equivalent_pages} | {self.calculate_equivalent_pages(chapter_aggregated['words'], chapter_aggregated['diagrams'], microsims)} | Estimated pages (250 words/page + visuals) |\n"

        # Botany / species-card metrics — only shown when the project uses the
        # plant-gallery-generator (i.e., docs/plants/ exists)
        if species["total"] > 0:
            md += "\n## Species Card Coverage\n\n"
            md += "Botany textbooks built with the plant-gallery-generator track per-species "
            md += "reference cards and their asset coverage.\n\n"
            md += "| Metric | Value | Notes |\n"
            md += "|--------|-------|-------|\n"
            md += f"| Species Cards | {species['total']} | Per-species reference pages in docs/plants/ |\n"
            md += (f"| Cards w/ Illustration | {species['with_illustration']} "
                   f"({species['with_illustration'] * 100 // species['total']}%) "
                   f"| Botanical plate available |\n")
            md += (f"| Cards w/ Photos | {species['with_photos']} "
                   f"({species['with_photos'] * 100 // species['total']}%) "
                   f"| Wikipedia/Wikimedia photo present |\n")
            md += (f"| Cards w/ Quick Facts | {species['with_quick_facts']} "
                   f"({species['with_quick_facts'] * 100 // species['total']}%) "
                   f"| Trait data populated (not just dashes) |\n")
            if host_relationships > 0:
                md += (f"| Host-plant Mentions | {host_relationships} "
                       f"| Pollinator-host coverage signal |\n")

        md += "\n## Metrics Explanation\n\n"
        md += "### Book Composition Elements\n\n"
        md += "- **Concepts** *(required)*: Number of rows in learning-graph.csv\n"
        md += "- **Chapters** *(required)*: Count of chapter directories containing index.md files\n"
        md += "- **MicroSims** *(recommended)*: Directories in docs/sims/ with index.md files\n"
        md += "- **Stories** *(optional)*: Story directories in docs/stories/ with index.md files\n"
        md += "- **Chapter Quizzes** *(recommended)*: Chapters containing a quiz.md file (with total quiz questions in the notes)\n"
        md += "- **Chapter References** *(recommended)*: Chapters containing a references.md file (with total reference entries in the notes)\n"
        md += "- **Glossary Terms** *(recommended)*: H4 headers in glossary.md\n"
        md += "- **FAQs** *(recommended)*: H3 headers in faq.md\n"
        md += "- **Words** *(required)*: All words in student-facing markdown files (excluding code blocks and URLs)\n"
        md += "- **Mascot** *(optional)*: Image files (poses) in docs/img/mascot/\n"
        md += "- **Appendices** *(optional)*: Pages in the appendices/ directory (excluding index.md)\n"
        md += "- **Development Stage** *(required)*: `development_stage` value in mkdocs.yml (or course-description.md); shows 'Not specified' if absent\n"
        md += "- **Labs** *(optional)*: Hands-on lab directories in docs/labs/ with index.md files\n\n"

        md += "### Content Metrics\n\n"
        md += "- **Diagrams**: H4 headers starting with '#### Diagram:'\n"
        md += "- **Equations**: LaTeX expressions using $ and $$ delimiters\n"
        md += "- **Total Words**: All words in markdown files (excluding code blocks and URLs)\n"
        md += "- **Links**: Markdown-formatted links `[text](url)`\n"
        md += "- **Equivalent Pages**: Based on 250 words/page + 0.25 page/diagram + 0.5 page/MicroSim\n\n"

        if species["total"] > 0:
            md += "### Species Card Coverage\n\n"
            md += "- **Species Cards**: Files in docs/plants/ (excluding index.md)\n"
            md += "- **Cards w/ Illustration**: Cards whose docs/plants/img/<slug>-illustration.png exists\n"
            md += "- **Cards w/ Photos**: Cards referencing at least one <slug>-1.jpg photo\n"
            md += "- **Cards w/ Quick Facts**: Cards whose Quick Facts table has at least one populated row (not just em-dashes)\n"
            if host_relationships > 0:
                md += "- **Host-plant Mentions**: Occurrences of 'host plant' or 'larval host' in chapters — soft signal of pollinator-ecology coverage\n"
            md += "\n"

        md += "### Column Explanations\n\n"
        md += "- **All Content**: Includes all student-facing content (chapters, glossary, FAQ, sims, etc.) but excludes administrative directories\n"
        md += "- **Chapters Only**: Aggregated from chapter directories only - represents the core textbook content students read\n\n"

        md += "**Excluded Directories**: `prompts/`, `learning-graph/` (administrative content not visible to students)\n"

        return md

    def generate_chapter_metrics_md(self) -> str:
        """Generate the chapter-metrics.md content.

        Returns:
            Markdown content as string
        """
        # Collect chapter info
        chapter_count, chapters = self.count_chapters()

        # Get current timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        if chapter_count == 0:
            md = "# Chapter Metrics\n\n"
            md += f"**Generated by**: Book Metrics Python Program v{VERSION}  \n"
            md += f"**Generated on**: {timestamp}\n\n"
            md += "No chapters found.\n"
            return md

        # Build markdown table
        md = "# Chapter Metrics\n\n"
        md += f"**Generated by**: Book Metrics Python Program v{VERSION}  \n"
        md += f"**Generated on**: {timestamp}\n\n"
        md += "This file contains chapter-by-chapter metrics for student-facing content.\n\n"
        md += "| Chapter | Name | Sections | Diagrams | Equations | Words | Links | Quiz | Refs |\n"
        md += "|---------|------|----------|----------|-----------|-------|-------|------|------|\n"

        # Add rows for each chapter
        for chapter in chapters:
            metrics = self.get_chapter_metrics(chapter)
            # Create link to chapter index.md (relative to learning-graph directory)
            chapter_dir_name = chapter['path'].name
            chapter_link = f"[{metrics['name']}](../chapters/{chapter_dir_name}/index.md)"
            md += f"| {metrics['number']} | {chapter_link} | {metrics['sections']} | {metrics['diagrams']} | {metrics['equations']} | {metrics['words']:,} | {metrics['links']} | {metrics['quiz_questions']} | {metrics['references']} |\n"

        md += "\n## Metrics Explanation\n\n"
        md += "- **Chapter**: Chapter number (leading zeros removed)\n"
        md += "- **Name**: Chapter title from index.md\n"
        md += "- **Sections**: Count of H2 and H3 headers in chapter markdown files\n"
        md += "- **Diagrams**: Count of H4 headers starting with '#### Diagram:'\n"
        md += "- **Equations**: LaTeX expressions using $ and $$ delimiters\n"
        md += "- **Words**: Word count across all markdown files in the chapter\n"
        md += "- **Links**: Markdown-formatted links `[text](url)`\n"
        md += "- **Quiz**: Number of quiz questions in the chapter's quiz.md (0 if none)\n"
        md += "- **Refs**: Number of references in the chapter's references.md (0 if none)\n"

        return md

    def collect_book_totals(self) -> Dict[str, Any]:
        """Collect the book-wide total metrics used in the case-studies index.

        These are the same totals shown in the intelligent-textbooks
        case-studies cards (e.g. "200 Concepts · 12 Chapters · 18 MicroSims ·
        171K Words · 200 Glossary Terms"). Only book-level totals are
        returned here - per-chapter breakdowns are intentionally excluded.

        Returns:
            Dict of metric name -> total value (ints, plus the development
            stage string). Botany species-card totals are included only when
            the project has a docs/plants/ directory.
        """
        chapter_count, _ = self.count_chapters()
        ref_files, ref_entries = self.count_chapter_references()
        diagrams = self.count_all_diagrams(exclude_non_content=True)
        microsims = self.count_microsims()
        total_words = self.count_total_words(exclude_non_content=True)

        totals = {
            "concepts": self.count_concepts(),
            "chapters": chapter_count,
            "microsims": microsims,
            "stories": self.count_stories(),
            "labs": self.count_labs(),
            "glossaryTerms": self.count_glossary_terms(),
            "faqs": self.count_faqs(),
            "quizQuestions": self.count_quiz_questions(),
            "chapterQuizzes": self.count_chapter_quizzes(),
            "chapterReferences": ref_files,
            "references": ref_entries,
            "diagrams": diagrams,
            "equations": self.count_all_equations(exclude_non_content=True),
            "words": total_words,
            "links": self.count_all_links(exclude_non_content=True),
            "appendices": self.count_appendices(),
            "mascotImages": self.count_mascot_images(),
            "developmentStage": self.get_development_stage(),
            "equivalentPages": self.calculate_equivalent_pages(
                total_words, diagrams, microsims),
        }

        # Include species-card totals only for botany projects (docs/plants/)
        species = self.count_species_cards()
        if species["total"] > 0:
            totals["speciesCards"] = species["total"]
            totals["speciesCardsWithIllustration"] = species["with_illustration"]
            totals["speciesCardsWithPhotos"] = species["with_photos"]
            totals["speciesCardsWithQuickFacts"] = species["with_quick_facts"]

        return totals

    def build_metrics_payload(self) -> Dict[str, Any]:
        """Build the full book-metrics.json payload (provenance + totals).

        This is the single in-memory representation that is written verbatim to
        the canonical docs/learning-graph/book-metrics.json file and whose
        `metrics` block is also mirrored into book-metadata.json. Generating
        both files from one payload guarantees the two can never drift.

        Returns:
            Dict conforming to book-metrics.schema.json.
        """
        return {
            "$schema": (
                "https://raw.githubusercontent.com/dmccreary/ibook-skills/"
                "main/src/book-metrics/book-metrics.schema.json"
            ),
            "metricsVersion": METRICS_FILE_VERSION,
            "metricsGeneratedBy": f"Book Metrics Python Program v{VERSION}",
            "metricsGeneratedOn": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            "metricsGeneratedOnISO": datetime.now().replace(microsecond=0).isoformat(),
            "metrics": self.collect_book_totals(),
        }

    def write_book_metrics_json(self, output_dir: Path = None,
                                payload: Dict[str, Any] = None) -> None:
        """Write the canonical, machine-generated book-metrics.json.

        This file is the SINGLE SOURCE OF TRUTH for book-wide totals. Unlike
        book-metadata.json (which holds author-supplied descriptive fields and
        is merged in place), book-metrics.json is fully owned by this script and
        overwritten wholesale every run - there are no hand-edited fields to
        preserve, so there is no merge logic and no risk of clobbering author
        content. Consuming skills (readme-generator, linkedin-announcement-
        generator, case-study-generator) READ this file instead of re-deriving
        counts from markdown.

        Args:
            output_dir: Directory to write book-metrics.json to
                        (defaults to the learning-graph directory).
            payload: Pre-built payload from build_metrics_payload(); built here
                     if not supplied.
        """
        if output_dir is None:
            output_dir = self.learning_graph_dir
        if payload is None:
            payload = self.build_metrics_payload()

        metrics_file = output_dir / "book-metrics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Wrote {metrics_file}")

    def update_book_metadata(self, output_dir: Path = None,
                             payload: Dict[str, Any] = None) -> None:
        """Create or update book-metadata.json with the book's total metrics.

        The canonical home for these totals is book-metrics.json (written by
        write_book_metrics_json). This method maintains a BACKWARD-COMPATIBLE
        mirror inside book-metadata.json for consumers that have not yet
        migrated (notably the intelligent-textbooks case-studies index). The
        learning-graph-generator workflow creates book-metadata.json with
        descriptive fields (title, description, creator, cover image, etc.).
        This method PRESERVES those author-supplied fields and adds/updates a
        single `metrics` object holding the book-wide totals. Per-chapter
        metrics are never written here - only totals.

        The mirrored `metrics` block is taken from the SAME payload used for
        book-metrics.json, so the two files can never drift.

        If the existing file cannot be parsed as JSON it is left untouched (we
        never clobber the author's metadata) and a warning is printed.

        Args:
            output_dir: Directory containing book-metadata.json
                        (defaults to the learning-graph directory)
            payload: Shared payload from build_metrics_payload(); built here if
                     not supplied.
        """
        if output_dir is None:
            output_dir = self.learning_graph_dir
        if payload is None:
            payload = self.build_metrics_payload()

        metadata_file = output_dir / "book-metadata.json"

        # Load existing metadata so author-supplied fields survive the update
        data: Dict[str, Any] = {}
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"⚠️  Could not parse {metadata_file} ({e}); leaving it "
                      f"untouched to avoid losing author metadata.")
                return
            if not isinstance(data, dict):
                print(f"⚠️  {metadata_file} is not a JSON object; leaving it "
                      f"untouched.")
                return

        # Merge: replace only the metrics block + provenance, keep everything
        # else the author put in book-metadata.json. Sourced from the shared
        # payload so book-metadata.json and book-metrics.json stay identical.
        data["metrics"] = payload["metrics"]
        data["metricsGeneratedBy"] = payload["metricsGeneratedBy"]
        data["metricsGeneratedOn"] = payload["metricsGeneratedOn"]

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Updated {metadata_file}")

    def generate_metrics(self, output_dir: Path = None):
        """Generate the metrics reports and the machine-readable metrics files.

        Writes four artifacts to the learning-graph directory:
          - book-metrics.md       (human-readable book totals)
          - chapter-metrics.md    (human-readable per-chapter breakdown)
          - book-metrics.json     (canonical machine-readable totals)
          - book-metadata.json    (author metadata + mirrored metrics block)

        Args:
            output_dir: Directory to write files to (defaults to learning-graph directory)
        """
        if output_dir is None:
            output_dir = self.learning_graph_dir

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate book metrics
        book_metrics_content = self.generate_book_metrics_md()
        book_metrics_file = output_dir / "book-metrics.md"
        with open(book_metrics_file, 'w', encoding='utf-8') as f:
            f.write(book_metrics_content)
        print(f"✅ Generated {book_metrics_file}")

        # Generate chapter metrics
        chapter_metrics_content = self.generate_chapter_metrics_md()
        chapter_metrics_file = output_dir / "chapter-metrics.md"
        with open(chapter_metrics_file, 'w', encoding='utf-8') as f:
            f.write(chapter_metrics_content)
        print(f"✅ Generated {chapter_metrics_file}")

        # Build the totals + provenance payload ONCE, then write both JSON
        # files from it so book-metrics.json and book-metadata.json's mirrored
        # `metrics` block are guaranteed identical.
        payload = self.build_metrics_payload()

        # Canonical machine-readable totals (single source of truth)
        self.write_book_metrics_json(output_dir, payload)

        # Backward-compatible mirror inside author metadata
        self.update_book_metadata(output_dir, payload)


def main():
    """Main entry point."""
    import sys

    # Get docs directory from command line or use default
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"

    # Check if docs directory exists
    if not Path(docs_dir).exists():
        print(f"❌ Error: Directory '{docs_dir}' does not exist")
        sys.exit(1)

    # Generate metrics
    generator = BookMetricsGenerator(docs_dir)
    generator.generate_metrics()

    print(f"\n✅ Book metrics generation version {VERSION} complete!")
    print("\nUpdates in v0.09:")
    print("  - Added Labs tracking: hands-on lab directories under docs/labs/")
    print("    (each with an index.md) are now element #13 in the Book")
    print("    Composition table and the 'labs' total in book-metrics.json.")
    print("\nPrevious updates (v0.08):")
    print("  - NEW canonical docs/learning-graph/book-metrics.json - the single")
    print("    source of truth for book-wide totals. Fully machine-owned and")
    print("    overwritten each run; validates against book-metrics.schema.json.")
    print("  - Consuming skills (README, LinkedIn, case-study) should READ this")
    print("    file instead of re-deriving counts from markdown.")
    print("  - book-metadata.json still gets a mirrored `metrics` block (built")
    print("    from the same payload) for backward compatibility.")
    print("\nPrevious updates (v0.07):")
    print("  - Create/update docs/learning-graph/book-metadata.json with the")
    print("    book-wide totals used in the case-studies index (concepts,")
    print("    chapters, MicroSims, stories, words, glossary, quiz, FAQ, etc.)")
    print("  - Author-supplied fields in book-metadata.json are preserved;")
    print("    only the `metrics` block is added/updated (no per-chapter data)")
    print("  - Re-added optional species-card coverage metrics for botany books")
    print("\nPrevious updates (v0.06):")
    print("  - Added a Book Composition table tracking all 12 textbook elements")
    print("    with a Required/Recommended/Optional status for each")
    print("  - New elements: Stories, Chapter Quizzes, Chapter References,")
    print("    Mascot, Appendices, and Development Stage")
    print("  - Chapter metrics now include per-chapter Quiz and Refs columns")
    print("\nPrevious updates (v0.05):")
    print("  - Fixed FAQ counting to correctly match H3 headers only (not H4+)")
    print("\nPrevious updates (v0.04):")
    print("  - Added version number and human-readable timestamp to reports")
    print("  - Clear attribution: 'Generated by Book Metrics Python Program'")
    print("\nhttp://localhost:8000/conversational-ai/learning-graph/book-metrics/")
    print("http://localhost:8000/conversational-ai/learning-graph/chapter-metrics/")



if __name__ == "__main__":
    main()
