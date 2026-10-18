# Image Sourcing

Every part section opens with a photo, because recognition is the first thing a
buyer needs: a teacher holding a bag of parts has to be able to match what is
in their hand to what is on the screen. A wrong or missing photo defeats the
whole page.

## Order of preference

### 1. Images already in this workspace (best)

Dan's workspace holds 100+ sibling textbook repos, and component photography
has been accumulating in them for years. Almost every part in a Moving Rainbow
kit has already been photographed for some other book. Those images are already
license-clean, already match the house look, and cost nothing.

```bash
python3 .claude/skills/purchasing-guide-generator/scripts/find_part_image.py momentary push button
python3 .claude/skills/purchasing-guide-generator/scripts/find_part_image.py "screw terminal" --deep
```

The finder searches this repo's whole `docs/` tree plus every sibling repo's
`docs/img/`, and ranks by filename match, locality, and resolution. Add
`--deep` to walk each sibling's entire `docs/` tree when the quick pass turns
up nothing — kit-local photos often sit beside their `index.md` rather than in
`docs/img/`.

- Images already in **this** repo's `docs/img/`: reference in place as
  `../../img/name.png` (from `docs/learning-graph/teachers-guide/`). Do not copy.
- Images from a **sibling** repo: copy into
  `docs/learning-graph/teachers-guide/` and reference as `./name.png`. Copy
  rather than linking across repos — sibling repos move and get renamed, and a
  cross-repo path will not survive a site build anyway.

### 2. Wikimedia Commons and other free sources

When nothing local fits, Wikimedia Commons is the reliable option. Its
electronics component photography is good and its licensing is explicit.

Check three things on the file's description page before using it:

- **License.** Public domain, CC0, CC BY, or CC BY-SA are all fine. Anything
  marked non-commercial or no-derivatives is not — this is a published site.
- **Attribution requirement.** CC BY and CC BY-SA require credit. Put it in a
  caption line directly under the image:
  `*Photo: {Author}, [{License}]({license-url}) via Wikimedia Commons*`
- **Watermarks and seller branding.** Look at the actual pixels, not just the
  metadata. A photo with a store logo burned into the corner is unusable
  regardless of its license.

Download the file into the guide's directory rather than hotlinking it.
Hotlinks break, and Wikimedia asks that you not hotlink at scale.

Other sources that are safe by license: NASA and other US federal agency images
(public domain), manufacturer press kits that explicitly grant editorial reuse,
and open-hardware project photography under a stated CC license.

**Never** take a product photo from an eBay, Amazon, or AliExpress listing.
Those are copyrighted seller assets, they disappear when the listing ends, and
a page full of broken images reads as abandoned. The one exception in the
moving-rainbow repo — screenshots of *search results* used to illustrate what a listing looks
like, such as `docs/img/led-strip-ebay-listing.png` — is editorial commentary
about the marketplace, not a substitute for a part photo. Use it sparingly.

### 3. A generation brief (last resort)

If you cannot find a high-quality image that is unwatermarked and free of
copyright restrictions, do not settle for a poor one and do not quietly ship
the section without a picture. Write a brief that a text-to-image model can
work from:

```
docs/learning-graph/teachers-guide/{part-slug}-image-description.md
```

Start from `assets/image-description-template.md`. Then leave a visible
placeholder in the guide so the gap is obvious rather than silent:

```markdown
<!-- TODO: image needed — see 2n2222-transistor-image-description.md -->
*Photo pending. See the [image brief](./2n2222-transistor-image-description.md).*
```

A brief is only useful if it is specific. "A transistor" produces something
that looks like no real transistor. "A single TO-92 package NPN transistor,
black plastic with one flat face, three silver leads splayed slightly, lying on
a plain white background, product-photography lighting, shot from a low
three-quarter angle, filling about 60% of a square frame" produces something a
teacher can match against the part in their hand.

## House style for part photos

Consistency across sections matters more than any single image being perfect:

- Plain white or very light neutral background.
- One part per image, filling most of the frame.
- Even lighting, no harsh shadow, no dramatic angle.
- Landscape or square. Very tall images push the description off screen.
- Roughly 600–1200px on the long edge — large enough to read fine detail like
  a resistor's color bands, small enough not to slow the page.
- Real photos beat renders for recognition; a render beats nothing.
- Use `{ width="400" }` on any image that would otherwise dominate the page:
  `![Screw terminal header](../../img/3-terminal-screw-header.png){ width="300" }`

## Alt text

Describe the part, not the file. `![Momentary push button with four leads]` is
useful to a screen-reader user and to anyone whose image failed to load;
`![]` is useful to nobody. Keep it to a short phrase — the surrounding
paragraph carries the detail.
