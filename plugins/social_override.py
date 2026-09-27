"""MkDocs hook that replaces the social plugin's auto-generated og:image
and twitter:image meta tags with a custom image URL from a page's
`image:` frontmatter field.

Loaded via the `hooks:` entry in mkdocs.yml, not as a plugin — this
avoids collisions with other projects that also install a package
called `social_override` or a top-level module called `plugins`.

Usage:
    In mkdocs.yml, add at the top level (NOT under `plugins:`):

        hooks:
          - plugins/social_override.py

    Make sure `social` is in your plugins list so the default cards
    still get generated (this hook only rewrites the emitted meta
    tags; pages without an `image:` frontmatter field fall through
    to the generated card).

    Then on any page you want a custom preview image:

        ---
        title: My Page
        image: img/my-custom-social-card.png
        ---
"""

import re


def on_page_context(context, page, config, **kwargs):
    """Stash the custom image path on the page for the post_page hook."""
    if page.meta and 'image' in page.meta:
        page.custom_image = page.meta['image']
    return context


def on_post_page(html, page, config, **kwargs):
    """Replace the social plugin's generated og:image / twitter:image
    tags with the page's custom cover image URL."""
    if not hasattr(page, 'custom_image'):
        return html

    site_url = config['site_url'].rstrip('/')
    image_path = '/' + page.custom_image.lstrip('/')
    full_image_url = site_url + image_path

    # og:image uses property=
    og_pattern = re.compile(r'<meta\s+property="og:image"[^>]*?>')
    for tag in og_pattern.findall(html):
        if '/assets/images/social/' in tag:
            new_tag = f'<meta property="og:image" content="{full_image_url}">'
            html = html.replace(tag, new_tag)

    # Material emits twitter:image with property= (not name=), so match both
    twitter_pattern = re.compile(
        r'<meta\s+(?:property|name)="twitter:image"[^>]*?>'
    )
    for tag in twitter_pattern.findall(html):
        if '/assets/images/social/' in tag:
            # Preserve whichever attribute style was in the original tag
            attr = 'property' if 'property=' in tag else 'name'
            new_tag = f'<meta {attr}="twitter:image" content="{full_image_url}">'
            html = html.replace(tag, new_tag)

    # The social plugin's cards are PNGs, so it always says image/png.
    # Make og:image:type match the custom image instead (a .jpg photo
    # would otherwise be announced as a PNG).
    image_types = {'.png': 'image/png', '.jpg': 'image/jpeg',
                   '.jpeg': 'image/jpeg', '.gif': 'image/gif',
                   '.webp': 'image/webp'}
    extension = '.' + image_path.rsplit('.', 1)[-1].lower()
    if extension in image_types:
        html = re.sub(r'<meta\s+property="og:image:type"[^>]*?>',
                      f'<meta property="og:image:type" '
                      f'content="{image_types[extension]}">', html)

    return html
