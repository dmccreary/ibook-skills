# Image Generation Scripts

Scripts for generating book cover images and logos using OpenAI's image generation API.

Both scripts default to `gpt-image-2.6-sunburst` for high-quality image generation. Override it with `OPENAI_IMAGE_MODEL` or `--image-model`.

## Requirements

```bash
pip install openai pillow
```

## Environment Setup

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Note:** API usage requires active billing on your OpenAI account. See [Billing Options](#billing-options) below.

## Scripts

### generate-cover.sh

Main script for generating book cover images. Run from your project's root directory (where `mkdocs.yml` is located).

**Full Generation (requires API billing):**
```bash
cd /path/to/your/book-project
/path/to/ibook-skills/src/image-generation/generate-cover.sh
```

**Local Prompt Mode (NO API required - for ChatGPT Plus users):**
```bash
cd /path/to/your/book-project
/path/to/ibook-skills/src/image-generation/generate-cover.sh --local-prompt
```

**Open Browser Mode (opens ChatGPT and pastes prompt automatically):**
```bash
cd /path/to/your/book-project
/path/to/ibook-skills/src/image-generation/generate-cover.sh --open-browser
```

**API Prompt-Only Mode (requires API billing):**
```bash
cd /path/to/your/book-project
/path/to/ibook-skills/src/image-generation/generate-cover.sh --prompt-only
```

The script will:
1. Read the book title from `mkdocs.yml` (site_name field)
2. Read imagery keywords from `docs/course-description.md`
3. Show a configuration summary and ask for confirmation
4. Generate an optimized image prompt
5. Either generate the image via API, or display the prompt for manual use

**Output:** `docs/img/cover.png` (1200x630 pixels, 1.91:1 aspect ratio)

### generate-cover-openai.py

Python script that does the actual work. Can be called directly with more options:

```bash
python generate-cover-openai.py \
    --desc path/to/course-description.md \
    --title "My Book Title" \
    --out output/cover.png
```

**Options:**
| Flag | Description |
|------|-------------|
| `--desc` | Path to course description file (required) |
| `--title` | Cover title (inferred from file if omitted) |
| `--out` | Output PNG path (default: derived from title) |
| `--prompt-only` | Only generate the prompt via API, don't create image |
| `--local-prompt` | Generate prompt locally without any API calls |
| `--open-browser` | Open ChatGPT in browser and paste prompt (implies --local-prompt) |
| `--text-model` | Model for prompt generation (default: gpt-4o-mini) |
| `--image-model` | Model for image generation (default: gpt-image-2.6-sunburst) |
| `--debug-json` | Path to save the intermediate cover plan JSON |

### test-key.sh

Test if your OpenAI API key is valid and has active billing:

```bash
./test-key.sh
```

Tests three API endpoints:
1. Models endpoint (basic connectivity)
2. Chat completions (requires billing)
3. Responses API (used by cover generator)

### test-key.py

Python version of the API key test, useful for debugging SDK-specific issues:

```bash
python test-key.py
```

### open-chatgpt.py

Opens ChatGPT in your browser and automatically pastes a prompt. Used by `--open-browser` flag but can also be used standalone:

```bash
python open-chatgpt.py "Your prompt here"
```

**Options:**
| Flag | Description |
|------|-------------|
| `--no-paste` | Only open browser and copy to clipboard, don't auto-paste |
| `--delay N` | Seconds to wait before pasting (default: 4) |

**Note:** macOS only. Uses AppleScript for browser automation.

## Billing Options

### Option 1: OpenAI API Credits (Automated)

For fully automated image generation:

1. Go to https://platform.openai.com/settings/organization/billing
2. Add a payment method
3. Purchase API credits

Cost: ~$0.04-0.08 per image depending on size and model.

### Option 2: ChatGPT Plus (Manual)

If you have a ChatGPT Plus subscription ($20/month), you can generate images manually:

1. Run the script with `--local-prompt` (no API billing required):
   ```bash
   ./generate-cover.sh --local-prompt
   ```

2. Copy the generated IMAGE PROMPT

3. Paste it into ChatGPT (web or app)

4. Download the generated image

5. Save it to `docs/img/cover.png`

6. Resize to 1200x630 pixels if needed (1.91:1 aspect ratio)

**Important:** ChatGPT Plus and the OpenAI API are separate billing systems. A ChatGPT Plus subscription does NOT provide API credits.

## Output Specifications

- **Format:** PNG
- **Size:** 1200x630 pixels
- **Aspect Ratio:** 1.91:1 (standard for Open Graph/social preview images)
- **Use Cases:** GitHub social preview, Open Graph meta tags, book cover thumbnails

## Troubleshooting

### "billing_not_active" Error

Your OpenAI account doesn't have active billing for API usage.

**Solutions:**
- Add credits at https://platform.openai.com/settings/organization/billing
- Or use `--prompt-only` mode with ChatGPT Plus

### "Could not extract site_name from mkdocs.yml"

Make sure your `mkdocs.yml` has a `site_name:` field:

```yaml
site_name: My Book Title
```

### "Course description not found"

Create a course description file at `docs/course-description.md` in your project.
