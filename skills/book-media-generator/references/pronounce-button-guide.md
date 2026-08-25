
# Glossary Pronounce Button Guide (ElevenLabs)

> Formerly the standalone skill `pronounce-button`.

Add an inline audio "Pronounce" button to a glossary term or any term heading
in a markdown file, powered by ElevenLabs text-to-speech.

## When to Use

Trigger this skill when the user asks to:

- "Create a pronounce button for the term 'Bryophytes'"
- "Create a pronounce button for the term 'Bryophytes' in glossary.md"
- "Add pronunciation for 'Sphagnum Moss'"
- "Add a pronounce button for X in chapter-03.md"

## Prerequisites

- The environment variable `ELEVENLABS_API_KEY` must be set. Never hard-code
  or commit this key.
- The ElevenLabs API reference repo is at `/Users/dan/Documents/ws/elevenlabs-skills`
  for additional documentation if needed.

## Workflow

### Step 1: Identify the Term and Target File

Parse the user's request to extract:

1. **Term** — the word or phrase to pronounce (e.g., "Bryophytes")
2. **Target file** — the markdown file containing the term (default: `docs/glossary.md`)

### Step 2: Generate the MP3

**Important: Try the plain word first.** ElevenLabs handles most scientific
terms correctly when given the actual word. Only fall back to phonetic
spelling if the plain word sounds wrong after listening to it.

**Three-tier approach (escalate only when the user reports a problem):**

1. **Tier 1 — Plain word (default).** Send the actual term (e.g.,
   `"Biogeography"`). This works for most words. Always try this first.

2. **Tier 2 — Hyphenated phonetic (fallback).** If the user says the plain
   word sounds wrong, regenerate using a hyphenated phonetic version (e.g.,
   `"Gah-mee-toh-fyte"`). This can backfire — ElevenLabs sometimes reads
   each syllable as a separate word — so only use when Tier 1 fails.

3. **Tier 3 — SSML with CMU Arpabet (last resort).** If both plain and
   phonetic versions fail, use the `--ssml` flag with a CMU Arpabet string.
   This switches to `eleven_flash_v2` which supports SSML `<phoneme>` tags
   for precise phoneme-level control. Only use when the user explicitly
   indicates that Tiers 1 and 2 both failed.

**Tier 1 — Plain word:**

```bash
python3 SCRIPT "Biogeography" --output docs/audio/biogeography.mp3
```

**Tier 2 — Phonetic fallback:**

```bash
python3 SCRIPT "Gah-mee-toh-fyte" --output docs/audio/gametophyte.mp3
```

**Tier 3 — SSML (last resort):**

```bash
python3 SCRIPT "evapotranspiration" \
    --ssml "IH0 V AE2 P OW0 T R AE2 N S P ER0 EY1 SH AH0 N" \
    --output docs/audio/evapotranspiration.mp3
```

The `--ssml` flag takes a CMU Arpabet phoneme string. Stress markers are
required: `1` = primary stress, `2` = secondary stress, `0` = no stress.
See [CMU Arpabet reference](https://en.wikipedia.org/wiki/ARPABET) for
the full phoneme set.

**Known terms that required SSML (user-verified):**

| Term | CMU Arpabet |
|---|---|
| Acrocarpous | `AE2 K R OW0 K AA1 R P AH0 S` |
| Evapotranspiration | `IH0 V AE2 P OW0 T R AE2 N S P ER0 EY1 SH AH0 N` |

Where `SCRIPT` is:

```
python3 $BK_HOME/skills/book-media-generator/scripts/audio/generate-pronunciation.py
```

Where `SLUG` is the term lowercased with spaces replaced by hyphens
(e.g., "Sphagnum Moss" → `sphagnum-moss`).

The script:

- Reads `ELEVENLABS_API_KEY` from the environment
- Calls the ElevenLabs v1 TTS endpoint with the `eleven_multilingual_v2` model
- Writes an MP3 file to `docs/audio/SLUG.mp3`
- Uses the "Sarah" voice by default (clear US female voice suitable
  for term pronunciation)

If the API call fails, report the error to the user. Common issues:

- 401: Invalid API key — ask the user to check `ELEVENLABS_API_KEY`
- 429: Rate limit — wait and retry

### Step 3: Insert the Pronounce Button

Locate the term heading in the target markdown file. The heading format is
typically `#### Term Name` in the glossary, but may be other heading levels
in chapter files.

Insert the pronounce button HTML immediately after the heading line, before
the definition text. Use this exact HTML pattern:

```html
<audio id="audio-SLUG" src="../audio/SLUG.mp3" preload="none"></audio>
<button onclick="document.getElementById('audio-SLUG').play()" class="pronounce-btn">🔊 Pronounce</button> *PHONETIC-GUIDE*
```

The phonetic guide uses italics with the stressed syllable in ALL CAPS
(e.g., `*gah-MEE-toh-fyte*`). Always include this next to the button so
users can verify the pronunciation visually.

**Adjust the relative path** (`src` attribute) based on the target file's
location relative to `docs/audio/`. MkDocs uses directory URLs by default,
so each page is served from a subdirectory (e.g., `glossary.md` becomes
`glossary/index.html`). Count directory levels from the page's served URL
back to the site root, then append `audio/SLUG.mp3`. For example:

| Target file | Served URL path | Relative path |
|---|---|---|
| `docs/glossary.md` | `/glossary/` | `../audio/SLUG.mp3` |
| `docs/appendices/common-terms.md` | `/appendices/common-terms/` | `../../audio/SLUG.mp3` |
| `docs/chapters/03-what-is-moss/index.md` | `/chapters/03-what-is-moss/` | `../../audio/SLUG.mp3` |

**Example result in glossary.md:**

```markdown
#### Bryophytes

<audio id="audio-bryophytes" src="../audio/bryophytes.mp3" preload="none"></audio>
<button onclick="document.getElementById('audio-bryophytes').play()" class="pronounce-btn">🔊 Pronounce</button> *BRY-oh-fytes*

A division of non-vascular land plants that includes mosses, liverworts,
and hornworts, all of which reproduce via spores and lack true roots,
stems, or leaves.
```

### Step 4: Ensure CSS Exists

Check if `docs/stylesheets/extra.css` (or whatever custom CSS file is
referenced in `mkdocs.yml`) contains a `.pronounce-btn` style. If not,
append the following:

```css
/* Pronounce button for glossary terms */
.pronounce-btn {
    background: #e8f5e9;
    border: 1px solid #4caf50;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.85em;
    cursor: pointer;
    margin-bottom: 8px;
    display: inline-block;
}
.pronounce-btn:hover {
    background: #c8e6c9;
}
```

### Step 5: Confirm to User

Report success with the local preview URL:

```
Generated pronunciation for "Bryophytes" → docs/audio/bryophytes.mp3
Added Pronounce button to docs/glossary.md
Preview: http://127.0.0.1:8000/moss/glossary/#bryophytes
```

## Voice Options

The default voice is Sarah (`EXAVITQu4vr4xnSDxMaL`) — a clear US female
voice well-suited for academic term pronunciation. If the user requests a
different voice, pass `--voice-id` to the script. Common alternatives:

| Voice | ID | Style |
|---|---|---|
| Sarah (default) | EXAVITQu4vr4xnSDxMaL | Female, soft |
| Charlotte | XB0fDUnXU5powFXDhCwa | Female, conversational |
| George | JBFqnCBsd6RMkjVDRZzb | Male, narrative |
| Daniel | onwK4e9ZLuTAKqWW03F9 | Male, authoritative |

## Batch Mode

To add pronounce buttons for multiple terms at once, the user may say
"Add pronounce buttons for all terms in the glossary." In this case:

1. Read `docs/glossary.md` and extract all `#### ` headings
2. For each term, run the script and insert the button
3. Report the total count when done

**Important:** Batch mode makes one API call per term. Warn the user
about the number of API calls before proceeding (e.g., "This will make
400 API calls to ElevenLabs. Proceed?").
