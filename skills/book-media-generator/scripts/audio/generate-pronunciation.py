#!/usr/bin/env python3
"""Generate an MP3 pronunciation file for a glossary term using ElevenLabs TTS API.

Usage:
    # Plain word (default, try this first):
    python3 generate-pronunciation.py "Bryophytes" --output docs/audio/bryophytes.mp3

    # SSML with CMU Arpabet (last resort, when plain and phonetic both fail):
    python3 generate-pronunciation.py "evapotranspiration" \
        --ssml "IH0 V AE2 P OW0 T R AE2 N S P ER0 EY1 SH AH0 N" \
        --output docs/audio/evapotranspiration.mp3

Environment:
    ELEVENLABS_API_KEY is read from the user's login shell (~/.zshrc) first,
    then from this process's environment. See resolve_api_key().
"""

import argparse
import os
import subprocess
import sys
import urllib.request
import urllib.error
import json


def _looks_like_key(value: str) -> bool:
    # ElevenLabs secret keys start with "sk_". A 64-character hex value is the
    # key's ID, which the API rejects with "api_key_id_used_as_api_key".
    return bool(value) and value.startswith("sk_")


def _key_from_login_shell() -> str:
    """Read ELEVENLABS_API_KEY as an interactive zsh sees it (i.e. from ~/.zshrc).

    GUI apps such as the Claude desktop app inherit macOS's launchctl
    environment rather than ~/.zshrc, so their ELEVENLABS_API_KEY can be stale
    or wrong even when the terminal's is correct. The value is captured
    between markers so other .zshrc output is ignored, and it is never printed.
    """
    shell = os.environ.get("SHELL", "/bin/zsh")
    if "zsh" not in shell:
        shell = "/bin/zsh"
    try:
        out = subprocess.run(
            [shell, "-i", "-c", 'printf "__ELKEY__%s__ELEND__" "$ELEVENLABS_API_KEY"'],
            capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL,
        ).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""
    start, end = out.rfind("__ELKEY__"), out.rfind("__ELEND__")
    return out[start + len("__ELKEY__"):end].strip() if 0 <= start < end else ""


def resolve_api_key() -> str:
    """Prefer the key in ~/.zshrc; fall back to the environment."""
    for source, value in (("~/.zshrc", _key_from_login_shell()),
                          ("environment", os.environ.get("ELEVENLABS_API_KEY", ""))):
        if _looks_like_key(value):
            return value
    print("Error: no valid ELEVENLABS_API_KEY found. Set it in ~/.zshrc to the "
          "secret key (it starts with 'sk_'), not the key's ID.", file=sys.stderr)
    sys.exit(1)


def slugify(term: str) -> str:
    """Convert a term to a filename-safe slug."""
    return term.lower().replace(" ", "-").replace("'", "").replace('"', "")


def generate_pronunciation(term: str, output_path: str,
                           voice_id: str = "EXAVITQu4vr4xnSDxMaL",
                           ssml_arpabet: str = None):
    """Call ElevenLabs TTS API to generate an MP3 pronunciation.

    Args:
        term: The word or phrase to pronounce.
        output_path: Path to write the MP3 file.
        voice_id: ElevenLabs voice ID (default: Sarah).
        ssml_arpabet: Optional CMU Arpabet string. When provided, uses
            eleven_flash_v2 with SSML phoneme tags for precise control.
    """
    api_key = resolve_api_key()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    if ssml_arpabet:
        # SSML mode: use eleven_flash_v2 which supports phoneme tags
        text = (f'<phoneme alphabet="cmu-arpabet" ph="{ssml_arpabet}">'
                f'{term}</phoneme>')
        model_id = "eleven_flash_v2"
    else:
        # Default mode: plain text with eleven_multilingual_v2
        text = term
        model_id = "eleven_multilingual_v2"

    payload = json.dumps({
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.0,
            "speed": 0.9,
        },
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with urllib.request.urlopen(req) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        mode = f"SSML/flash_v2 ({ssml_arpabet})" if ssml_arpabet else "plain/multilingual_v2"
        print(f"Generated: {output_path}  [{mode}]")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate MP3 pronunciation via ElevenLabs TTS")
    parser.add_argument("term", help="The term to pronounce")
    parser.add_argument("--output", "-o", help="Output MP3 file path")
    parser.add_argument("--voice-id", default="EXAVITQu4vr4xnSDxMaL",
                        help="ElevenLabs voice ID (default: Sarah)")
    parser.add_argument("--ssml", dest="ssml_arpabet", default=None,
                        help="CMU Arpabet phoneme string for SSML mode "
                             "(uses eleven_flash_v2). Example: "
                             "'IH0 V AE2 P OW0 T R AE2 N S P ER0 EY1 SH AH0 N'")
    args = parser.parse_args()

    if args.output:
        output_path = args.output
    else:
        slug = slugify(args.term)
        output_path = f"docs/audio/{slug}.mp3"

    generate_pronunciation(args.term, output_path, args.voice_id, args.ssml_arpabet)


if __name__ == "__main__":
    main()
