#!/usr/bin/env python3
"""
Convert CSV Learning Graph to JSON for vis-network.js
Converts the concept dependency CSV into the JSON format
used by the existing graph viewer (vis.js network format).

IMPORTANT: For custom taxonomies, provide taxonomy-names.json to ensure
human-readable classifierName values in the output. Without this file,
taxonomy IDs will be used as fallback (which is usually wrong).
"""

VERSION = "1.05"

import csv
import json
from collections import defaultdict, deque
from typing import Dict, List
from datetime import datetime


def calculate_cis(nodes: List[dict], edges: List[dict]) -> Dict[int, int]:
    """
    Compute the Concept Impact Score (CIS) for every node: a PageRank-style
    recursive importance measure over the concept dependency DAG.

        CIS(x) = 1 + sum(CIS(d) for d in direct_dependents(x))

    A concept's impact is itself (1) plus the combined impact of every
    concept that depends on it, computed transitively. This captures how
    much of the book's total understanding ultimately rests on a concept,
    which plain in-degree (direct dependents only) undercounts for concepts
    that are foundational only transitively (few direct dependents but many
    indirect ones -- e.g. "Constant" or "Coefficient" in a typical algebra
    course).

    Because a learning graph is a DAG (never contains a cycle), CIS has an
    exact closed-form solution computable in a single topological-order
    pass -- no PageRank damping factor or iteration is required. See the
    "Predicting Concept Content Size" paper (Definition 3, Proposition 1)
    for the full derivation.

    Edge convention (matches every other skill in this project): edge['from']
    is the DEPENDENT concept, edge['to'] is its PREREQUISITE. Edge
    {from: 5, to: 1} means concept 5 depends on concept 1. NEVER invert this
    -- see the "CRITICAL: Edge Direction" warnings in book-chapter-generator
    and chapter-content-generator.
    """
    node_ids = [n['id'] for n in nodes]

    dependents_of = defaultdict(list)  # prereq_id -> [dependent_id, ...]
    prereqs_of = defaultdict(list)     # dependent_id -> [prereq_id, ...]
    for e in edges:
        dependents_of[e['to']].append(e['from'])
        prereqs_of[e['from']].append(e['to'])

    # Process nodes in an order where every node is scored only after all of
    # its dependents are already scored -- terminal concepts (nothing
    # depends on them) first, foundational hub concepts last.
    remaining = {nid: len(dependents_of[nid]) for nid in node_ids}
    cis: Dict[int, int] = {}
    queue = deque([nid for nid in node_ids if remaining[nid] == 0])

    while queue:
        nid = queue.popleft()
        cis[nid] = 1 + sum(cis[d] for d in dependents_of[nid])
        for prereq in prereqs_of[nid]:
            remaining[prereq] -= 1
            if remaining[prereq] == 0:
                queue.append(prereq)

    if len(cis) != len(node_ids):
        unscored = [nid for nid in node_ids if nid not in cis]
        raise ValueError(
            f"CIS computation only scored {len(cis)}/{len(node_ids)} nodes -- "
            f"the graph likely contains a cycle (unscored IDs: {unscored[:10]}"
            f"{'...' if len(unscored) > 10 else ''}). Run analyze-graph.py or "
            f"validate-learning-graph.sh to verify DAG structure before retrying."
        )

    return cis


def csv_to_json(csv_path: str, json_path: str, color_config: dict = None,
                metadata: dict = None, taxonomy_names: dict = None):
    """
    Convert CSV dependency graph to vis.js JSON format with metadata and groups.

    Args:
        csv_path: Path to input CSV file with columns: ConceptID, ConceptLabel, Dependencies, TaxonomyID
        json_path: Path to output JSON file
        color_config: Optional dictionary mapping taxonomy IDs to colors.
                     If not provided, uses default color scheme.
        metadata: Optional dictionary with metadata fields (title, description, creator, etc.)
                 If not provided, creates minimal metadata.
        taxonomy_names: Dictionary mapping taxonomy IDs to human-readable names.
                       STRONGLY RECOMMENDED for custom taxonomies.
    """
    # Default 24-color palette designed for distinct, accessible category coloring.
    # Hues progress through subject-family groupings (cool blues for foundations,
    # greens for architecture/dev, yellows/golds for data, blues for network/cloud,
    # reds for security/privacy, purples for project/process/analysis, oranges
    # and browns for the AI cluster, an accent for knowledge graphs, neutral
    # for emerging topics) with alternating lightness so adjacent legend rows
    # never collide. Dark backgrounds automatically get white font for contrast;
    # light backgrounds get black. The previous all-pastel palette caused legend
    # collisions when a project had >12 categories — this palette supports up
    # to 24 distinct categories without color reuse.
    # Since the background is AliceBlue, do not use that color.
    DEFAULT_PALETTE = [
        'SteelBlue',       # 1  cool foundations
        'DarkSlateBlue',   # 2
        'DarkGreen',       # 3  architecture / build
        'LimeGreen',       # 4
        'Gold',            # 5  data band
        'DarkGoldenrod',   # 6
        'Khaki',           # 7
        'Teal',            # 8  enterprise
        'DodgerBlue',      # 9  network / cloud
        'LightSkyBlue',    # 10
        'Crimson',         # 11 security / privacy
        'DarkRed',         # 12
        'MediumPurple',    # 13 project / process / analysis
        'Indigo',          # 14
        'DarkOrchid',      # 15
        'HotPink',         # 16 user-facing
        'OliveDrab',       # 17 service management
        'Orange',          # 18 AI cluster
        'Coral',           # 19
        'Peru',            # 20
        'SaddleBrown',     # 21
        'Tomato',          # 22
        'DeepPink',        # 23 accent — knowledge graphs / connective concepts
        'DimGray',         # 24 neutral — emerging / miscellaneous
    ]
    default_colors = {str(i + 1): color for i, color in enumerate(DEFAULT_PALETTE)}

    # color_config may be the legacy flat format {tax_id: "ColorName"} or a
    # richer format {tax_id: {"color": "ColorName", "classifierName": "..."}}
    # (used by some existing projects' color-config.json). Normalize to a
    # flat tax_id -> color-string map, and harvest any embedded
    # classifierName values as a taxonomy-names source -- lower priority
    # than an explicitly-provided taxonomy_names.json, so that file can
    # still override. Passing the raw nested dict straight through as a
    # "color" (the previous behavior) produces an invalid learning-graph.json
    # that violates the schema and silently breaks group coloring in the
    # viewer -- this was found and fixed while regenerating an existing
    # project's learning-graph.json.
    color_config_names = {}
    if color_config is not None:
        taxonomy_colors = {}
        for tax_id, value in color_config.items():
            if isinstance(value, dict):
                taxonomy_colors[tax_id] = value.get('color', 'DimGray')
                if value.get('classifierName'):
                    color_config_names[tax_id] = value['classifierName']
            else:
                taxonomy_colors[tax_id] = value
    else:
        taxonomy_colors = default_colors

    # Default taxonomy ID to classifier name mapping
    # Supports both text codes (FOUND, DEF, etc.) and numeric IDs (1, 2, etc.)
    # These are the display names (classifierName in schema) for each taxonomy
    default_taxonomy_names = {
        # Custom taxonomies for intelligent textbook skills course
        'AIFND': 'AI Foundations',
        'SKILL': 'Claude Skills System',
        'IBOOK': 'Intelligent Textbooks',
        'MKDOC': 'MkDocs Platform',
        'GRAPH': 'Learning Graphs',
        'EDTHY': 'Educational Theory',
        'CONTE': 'Content Creation',
        'RSRCE': 'Educational Resources',
        'INTER': 'Interactive Elements',
        'VERCT': 'Version Control',
        'TOOLS': 'Development Tools',
        'DATAS': 'Data & Scripting',
        # Standard/default text codes
        'FOUND': 'Foundation Concepts',
        'DEF': 'Definitions',
        'CORE': 'Core Concepts',
        'ADV': 'Advanced',
        'APPL': 'Applied',
        'SPEC': 'Specialized',
        'CAP': 'Capstone Projects',
        'PROJ': 'Project Ideas',
        'MISC': 'Miscellaneous Concepts',
        # Numeric IDs (common mapping)
        '1': 'Foundation Concepts',
        '2': 'Definitions',
        '3': 'Core Concepts',
        '4': 'Intermediate',
        '5': 'Advanced',
        '6': 'Applied',
        '7': 'Specialized',
        '8': 'Capstone Projects',
        '9': 'Miscellaneous Concepts',
        '10': 'Extended Topics',
    }

    # Merge taxonomy names: built-in defaults, then names embedded in
    # color_config (if any), then an explicit taxonomy_names.json -- each
    # source overrides the previous, so an explicitly-provided file always
    # wins if both it and color_config supply a name for the same tax_id.
    all_taxonomy_names = default_taxonomy_names.copy()
    all_taxonomy_names.update(color_config_names)
    if taxonomy_names:
        all_taxonomy_names.update(taxonomy_names)

    # Read CSV
    nodes = []
    edges = []
    foundational_ids = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            concept_id = int(row['ConceptID'])
            # Support both ConceptLabel and ConceptName column names
            label = row.get('ConceptLabel') or row.get('ConceptName', '')
            taxonomy = row['TaxonomyID']
            dependencies_str = row['Dependencies']

            # Determine if foundational (no dependencies)
            is_foundational = (dependencies_str == '')
            if is_foundational:
                foundational_ids.append(concept_id)

            # Create node - use taxonomy ID directly as group reference
            node = {
                'id': concept_id,
                'label': label,
                'group': taxonomy
            }

            # Special styling for foundational concepts
            if is_foundational:
                node['shape'] = 'box'

            nodes.append(node)

            # Create edges (from concept to its prerequisites)
            if dependencies_str:
                prereq_ids = [int(pid) for pid in dependencies_str.split('|')]
                for prereq_id in prereq_ids:
                    edge = {
                        'from': concept_id,
                        'to': prereq_id
                    }
                    edges.append(edge)

    # Compute and attach the Concept Impact Score to every node
    cis_scores = calculate_cis(nodes, edges)
    for node in nodes:
        node['cis'] = cis_scores[node['id']]

    # Create metadata section
    default_metadata = {
        'title': 'Learning Graph',
        'description': f'Learning graph with {len(nodes)} concepts generated from CSV',
        'creator': 'CSV to JSON Converter',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'version': '1.0',
        'format': 'Learning Graph JSON v1.0',
        'schema': 'https://raw.githubusercontent.com/dmccreary/learning-graphs/refs/heads/main/src/schema/learning-graph-schema.json',
        'license': 'CC BY-NC-SA 4.0 DEED'
    }

    # Merge user-provided metadata with defaults
    if metadata:
        default_metadata.update(metadata)

    # Create groups section from taxonomy colors
    groups = {}

    # Determine which taxonomy IDs are actually used
    used_taxonomies = set(node['group'] for node in nodes)

    # Track taxonomies with missing human-readable names
    missing_names = []

    # Dark backgrounds need white text for contrast; everything else uses black.
    # Includes the new distinct palette plus a few legacy pastel colors retained
    # for back-compat with older color-config.json files. Checked first (exact,
    # hand-tuned) before falling back to computed luminance for any other named
    # color or hex code -- see font_color_for() below.
    DARK_BACKGROUND_COLORS = {
        'SteelBlue', 'DarkSlateBlue', 'DarkGreen', 'DarkGoldenrod', 'Teal',
        'DodgerBlue', 'Crimson', 'DarkRed', 'MediumPurple', 'Indigo',
        'DarkOrchid', 'OliveDrab', 'SaddleBrown', 'Tomato', 'DeepPink',
        'DimGray',
        # Legacy darks retained for back-compat with older color-config files
        'Plum', 'LightCoral',
    }

    # Hex values for common CSS color names NOT in the curated 24-color
    # palette above (e.g. plain "red", "purple", "indigo" as used directly
    # in a project's color-config.json). Used only as a luminance-lookup
    # fallback -- not exhaustive, just the common simple names a project is
    # likely to use directly rather than through the curated palette.
    NAMED_COLOR_HEX = {
        'red': '#FF0000', 'orange': '#FFA500', 'gold': '#FFD700',
        'green': '#008000', 'cyan': '#00FFFF', 'blue': '#0000FF',
        'indigo': '#4B0082', 'violet': '#EE82EE', 'purple': '#800080',
        'brown': '#A52A2A', 'teal': '#008080', 'olive': '#808000',
        'yellow': '#FFFF00', 'pink': '#FFC0CB', 'magenta': '#FF00FF',
        'navy': '#000080', 'maroon': '#800000', 'lime': '#00FF00',
        'silver': '#C0C0C0', 'tan': '#D2B48C', 'khaki': '#F0E68C',
        'coral': '#FF7F50', 'salmon': '#FA8072', 'turquoise': '#40E0D0',
        'plum': '#DDA0DD', 'orchid': '#DA70D6', 'beige': '#F5F5DC',
        'gray': '#808080', 'grey': '#808080', 'black': '#000000',
        'white': '#FFFFFF',
    }

    def luminance_font_color(hex_color: str) -> str:
        """Perceptual luminance (ITU-R BT.601) -> black or white text."""
        h = hex_color.lstrip('#')
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) != 6:
            return 'black'
        try:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        except ValueError:
            return 'black'
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return 'white' if luminance < 128 else 'black'

    def font_color_for(color: str) -> str:
        if color in DARK_BACKGROUND_COLORS:
            return 'white'
        if color.startswith('#'):
            return luminance_font_color(color)
        if color.lower() in NAMED_COLOR_HEX:
            return luminance_font_color(NAMED_COLOR_HEX[color.lower()])
        return 'black'

    for tax_id, color in taxonomy_colors.items():
        # Only include groups that are actually used
        if tax_id in used_taxonomies:
            # Get the classifier name for this taxonomy
            classifier_name = all_taxonomy_names.get(tax_id, tax_id)

            # Check if we're falling back to the ID (indicates missing name)
            if classifier_name == tax_id:
                missing_names.append(tax_id)

            groups[tax_id] = {
                'classifierName': classifier_name,
                'color': color,
                'font': {
                    'color': font_color_for(color)
                }
            }

    # Handle taxonomies in CSV that aren't in color config
    for tax_id in used_taxonomies:
        if tax_id not in groups:
            classifier_name = all_taxonomy_names.get(tax_id, tax_id)
            if classifier_name == tax_id:
                missing_names.append(tax_id)

            # Assign a default color based on position
            color_index = len(groups) % len(default_colors)
            color = list(default_colors.values())[color_index]

            groups[tax_id] = {
                'classifierName': classifier_name,
                'color': color,
                'font': {
                    'color': font_color_for(color)
                }
            }

    # Create final JSON structure
    graph_data = {
        'metadata': default_metadata,
        'groups': groups,
        'nodes': nodes,
        'edges': edges
    }

    # Write JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)

    print(f"✅ JSON graph created: {json_path} (csv-to-json v{VERSION})")
    print(f"   - Title: {default_metadata['title']}")
    print(f"   - {len(groups)} groups/taxonomies")
    print(f"   - {len(nodes)} nodes")
    print(f"   - {len(edges)} edges")
    print(f"   - {len(foundational_ids)} foundational concepts")
    print(f"\nFoundational concept IDs: {foundational_ids}")
    print(f"Groups: {list(groups.keys())}")

    top_cis = sorted(nodes, key=lambda n: -n['cis'])[:10]
    print(f"\nTop 10 concepts by Concept Impact Score (CIS):")
    for n in top_cis:
        print(f"   - {n['label']} (id {n['id']}): CIS={n['cis']}")

    # IMPORTANT: Warn about missing human-readable names
    if missing_names:
        print(f"\n⚠️  WARNING: The following taxonomy IDs are missing human-readable names:")
        for tax_id in missing_names:
            print(f"   - '{tax_id}' → classifierName set to '{tax_id}' (should be descriptive)")
        print(f"\n   To fix: Create taxonomy-names.json with mappings like:")
        print(f"   {{")
        for tax_id in missing_names:
            print(f'     "{tax_id}": "Human Readable Name Here",')
        print(f"   }}")
        print(f"\n   Then run: python csv-to-json.py {csv_path} {json_path} [colors.json] [metadata.json] taxonomy-names.json")

    return graph_data


def create_taxonomy_legend(groups: dict = None):
    """
    Generate a legend of taxonomy colors for documentation.

    Args:
        groups: Dictionary of groups from the generated JSON (contains classifierName, color, etc.)
    """
    if not groups:
        print("\n⚠️  No groups to display in legend")
        return

    print("\n## Taxonomy Color Legend\n")
    print("| Category | TaxonomyID | Color |")
    print("|----------|------------|-------|")
    for tax_id in sorted(groups.keys()):
        group_info = groups[tax_id]
        name = group_info.get('classifierName', tax_id)
        color = group_info.get('color', 'gray')
        print(f"| {name} | {tax_id} | {color} |")


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    if len(sys.argv) < 3:
        print(f"csv-to-json.py v{VERSION}")
        print("\nUsage: python csv-to-json.py <input_csv> <output_json> [color_config.json] [metadata.json] [taxonomy_names.json]")
        print("Looking for CSV column names: ConceptID, ConceptLabel, Dependencies, TaxonomyID")
        print("\nExample:")
        print("   python csv-to-json.py learning-graph.csv learning-graph.json")
        print("   python csv-to-json.py learning-graph.csv learning-graph.json color-config.json metadata.json taxonomy-names.json")
        print("\nOptional color_config.json format:")
        print(json.dumps({
            'FOUND': 'MistyRose',
            'CORE': 'LightYellow',
            'ADV': 'PowderBlue'
        }, indent=2))
        print("\nOptional metadata.json format:")
        print(json.dumps({
            'title': 'My Learning Graph',
            'description': 'A comprehensive learning graph',
            'creator': 'Your Name',
            'license': 'CC BY 4.0'
        }, indent=2))
        print("\n⚠️  RECOMMENDED: taxonomy-names.json format (prevents ID-as-name bug):")
        print(json.dumps({
            'FOUND': 'Foundation Concepts',
            'EDA1': 'Exploratory Data Analysis I',
            'REG': 'Regression & Correlation'
        }, indent=2))
        sys.exit(1)

    csv_path = sys.argv[1]
    json_path = sys.argv[2]

    # Load color config if provided
    color_config = None
    if len(sys.argv) > 3:
        config_file = sys.argv[3]
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                color_config = json.load(f)
            print(f"📋 Loaded color config from: {config_file}")
        except FileNotFoundError:
            print(f"⚠️  Color config file not found: {config_file}, using defaults")

    # Load metadata config if provided
    metadata = None
    if len(sys.argv) > 4:
        metadata_file = sys.argv[4]
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"📋 Loaded metadata from: {metadata_file}")
        except FileNotFoundError:
            print(f"⚠️  Metadata file not found: {metadata_file}, using defaults")

    # Load taxonomy names if provided (STRONGLY RECOMMENDED)
    taxonomy_names = None
    if len(sys.argv) > 5:
        names_file = sys.argv[5]
        try:
            with open(names_file, 'r', encoding='utf-8') as f:
                taxonomy_names = json.load(f)
            print(f"📋 Loaded taxonomy names from: {names_file}")
        except FileNotFoundError:
            print(f"⚠️  Taxonomy names file not found: {names_file}")
            print(f"   This may result in taxonomy IDs being used as display names.")

    graph_data = csv_to_json(csv_path, json_path, color_config, metadata, taxonomy_names)
    create_taxonomy_legend(graph_data['groups'])

    print("\n✅ CSV to JSON format complete. Ready to use with graph-viewer!")
    print(f"   Validate with: ./validate-learning-graph.sh {json_path}")
