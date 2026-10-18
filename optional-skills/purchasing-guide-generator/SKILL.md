---
name: purchasing-guide-generator
description: >-
  Write or update the Purchasing Guide subsection of a hardware textbook's
  Teacher's Guide (Instructor's Guide in college and professional-development
  books) at docs/learning-graph/teachers-guide/index.md, covering every part in
  every kit the book uses — a summary bill of materials with required parts first and optional
  parts after, then one section per part with a photo, what the part does in the
  kit, any prep work (soldering 22-gauge leads, cutting a strip to length),
  single-unit, classroom-of-20 and district price estimates, the exact search
  keywords that find it, and live eBay / AliExpress / Amazon search links.
  Use this skill whenever the user asks for a purchasing guide, parts list,
  parts page, bill of materials, BOM, shopping list, sourcing guide, "where do I
  buy this", "how much does this kit cost", "what do I need to order for 20
  students", or wants to add or refresh purchasing information for a kit — even
  if they never say the words "purchasing guide". Also use it when updating an
  existing purchasing guide with prices, images, or search links. Only for
  books whose kits include physical parts to buy.
---

# Purchasing Guide Generator

A Purchasing Guide is the page a teacher opens with a district purchase order
in one hand. It has to answer three questions without them leaving the page:
*what exactly do I order, what will it cost me for a class of 20, and where do
I click to buy it.* Everything in this skill exists to make one of those three
answers unambiguous.

The input is small — usually a handful of part names the user pastes in, or the
"Parts" sections already sitting in each kit's `index.md`. One Purchasing Guide
covers **all the kits in the book**, so a part shared by three kits is
described once and its section says which kits use it. The output is a long,
image-rich, link-rich page. Most of the work is sourcing: finding a clean photo,
finding a real price band, and finding the search phrase that actually surfaces
the right part instead of forty wrong ones.

## Where the output goes

```
docs/learning-graph/teachers-guide/index.md
```

The Purchasing Guide is a subsection (`## Purchasing Guide`) of the book's
Teacher's Guide page. College textbooks and professional-development books
call that page the **Instructor's Guide** — use whichever name the book already
uses (check the page's `#` title and the `mkdocs.yml` nav entry) and never mix
the two within one book.

- If `teachers-guide/index.md` exists, add or replace only the
  `## Purchasing Guide` section and leave the rest of the page alone.
- If it does not exist, create it with a `# Teacher's Guide` (or
  `# Instructor's Guide`) title and the Purchasing Guide as its first `##`
  section, and add it to `mkdocs.yml`.

**Front matter.** The Teacher's Guide page should open with mkdocs front
matter carrying a `title` and a `description`. If the page has none, add it;
if it has one, make sure the description mentions the Purchasing Guide so
search and social previews surface it:

```yaml
---
title: Teacher's Guide
description: Teaching notes for {Book}, including a Purchasing Guide with every kit part, single, classroom and district prices, and where to buy each one.
---
```

Part photos and image briefs live in that same directory,
`docs/learning-graph/teachers-guide/`, and are referenced as `./name.png`.
Images that already exist in the book's `docs/img/` stay where they are and are
referenced as `../../img/name.png` (two levels up from the guide).

A model example to match for tone and depth lives in the moving-rainbow repo
at `~/Documents/ws/moving-rainbow/docs/kits/moving-rainbow-base/purchasing-guide/index.md`.
It predates both the search-link requirement and the move into the Teacher's
Guide, so it is the right register but an outdated structure and location —
read it for voice, follow this skill for structure and placement.

## Audience and register

Purchasing guides are teacher-facing and live in the Teacher's Guide. Write
them the way the book's `CONTENT-GENERATION-GUIDE.md` (if present) describes
the Teacher's Guide register: professional, collegial, peer-to-peer,
technically precise. **The book's mascot never appears in a purchasing guide**
(Pixel, in Moving Rainbow) — nobody wants a mascot cheering while they
reconcile a purchase order. Use "we" for house practice ("We buy ours in
packs of ten"), third person for students.

## Workflow

### 1. Pin down the parts list and split it

Get the list from the user, or read each kit's `index.md` — most kits already
have a "Parts" or "What you'll need" section, and reusing it keeps the pages
consistent. Merge the kits' lists into one deduplicated list, recording which
kits use each part and how many per kit. Then split it in two:

- **Required** — the kit does not function without it.
- **Optional** — durability, convenience, or enrichment (screw headers, acrylic
  bases, battery packs, spare buttons).

Required parts come first in both the summary list and the body sections. A
teacher on a tight budget should be able to stop reading halfway down the page
and still have ordered a working kit.

If a part in the list is ambiguous ("LED strip"), resolve it against the kit's
code and wiring before writing — 60 pixels/meter and 144 pixels/meter are
different orders, and a purchasing guide that gets that wrong costs real money.

### 2. Source a photo for every part

Order of preference, best first:

1. **An image already in this workspace.** Run the finder — it searches this
   repo and every sibling repo's `docs/img/`:

   ```bash
   python3 .claude/skills/purchasing-guide-generator/scripts/find_part_image.py momentary push button
   ```

   Run it from the book's repo root (the `.claude/skills/` link resolves
   there). Images from sibling repos are already license-clean and match the
   house look. Copy the file into `docs/learning-graph/teachers-guide/` rather
   than linking across repos.

2. **Wikimedia Commons** or another explicitly free source, when nothing local
   fits. See `references/image-sourcing.md` for the license rules, the
   attribution line, and the watermark check.

3. **A generation brief.** If you cannot find a high-quality image that is
   unwatermarked and free of copyright restrictions, do not settle for a bad
   one and do not silently omit the picture. Write
   `docs/learning-graph/teachers-guide/{part-slug}-image-description.md` from
   `assets/image-description-template.md`, and leave a clearly-marked
   placeholder in the page so it is obvious what still needs art.

Never hotlink a product photo from eBay, Amazon, or AliExpress. Those are
copyrighted seller assets, they rot within weeks, and a broken image on a
purchasing page reads as an abandoned page.

### 3. Write each part section

Start from `assets/purchasing-guide-template.md` — it is the section skeleton
with one fully worked part section (the WS2812B strip) showing the target depth.
Copy it, then replace. Working from the skeleton is faster than assembling the
page from the fragments in this file, and it keeps guides consistent across
kits.

Use the section template below, in order, with no sections skipped. The order
matters: a reader scanning for the part they are unsure about recognizes it by
the photo, confirms it by the description, and then commits by the price and
the link.

### 4. Price it at three levels

Every part gets a single-unit price, a classroom price (20+), and — when a
distributor genuinely offers one — a **district / distributor** price (100+
units, typically Alibaba or a direct-from-factory listing with a minimum order
and a flat shipping fee, e.g. "breadboards at $0.40 each, MOQ 20, $20
shipping"). Leave the district level off a part when no such tier exists
rather than inventing one. See
`references/sourcing-strategy.md` for how to build the bands honestly, and
`references/part-catalog.md` for house-observed bands on the parts that recur
across Moving Rainbow kits.

### 5. Generate the search links

Do not hand-write marketplace URLs; the query syntax differs per site and typos
are invisible until a teacher clicks. Run:

```bash
python3 .claude/skills/purchasing-guide-generator/scripts/make_search_urls.py "WS2812B LED strip 60/m 5V IP20"
```

Add `--sites ebay,aliexpress,amazon,microcenter` for parts where a specialty
retailer genuinely beats the marketplaces (the Pico at Micro Center is the
standing example), `alibaba` for parts with a real district-scale bulk tier,
and `--alt "alternate phrasing"` when the part is sold under two different
names. Allowed sources are eBay, AliExpress, Amazon, **Micro Center**,
**Alibaba**, and the authorized specialty retailers the script knows
(Adafruit, SparkFun, Digi-Key).

**Search links only.** Every buy link is a *search* URL. Never link a specific
listing — no eBay `/itm/` links, no Amazon `/dp/` links, no AliExpress or
Alibaba `/item/` or `product-detail` links. Specific listings end, change
seller, or change product within weeks, and a teacher who clicks a dead or
swapped listing stops trusting the page. The one exception is a manufacturer
or authorized-retailer product page with a stable price (the Micro Center
Pico page), and even then add a search link beside it. If a specific
listing is worth showing, use a screenshot as an illustration, not a link.

### 6. Wire the page in

- Add a link from each kit's `index.md`, near the top of its parts section,
  to the guide's anchor — a relative path ending in
  `learning-graph/teachers-guide/index.md#purchasing-guide`.
- Make sure `mkdocs.yml` has a nav entry for `learning-graph/teachers-guide/index.md`
  (titled `Teacher's Guide` or `Instructor's Guide`, matching the page). The
  Purchasing Guide is a section of that page, not its own nav entry.
- Verify every image path resolves from `docs/learning-graph/teachers-guide/`
  and that the summary-list anchors match the actual heading slugs.

## Page structure

Follow this shape exactly — teachers move between books, and a predictable
section means they learn the layout once. The Purchasing Guide is a `##`
section of the Teacher's Guide page, so parts and closing sections are `###`.

````markdown
# Teacher's Guide            <!-- or "Instructor's Guide"; existing page title -->

...existing Teacher's Guide content, untouched...

## Purchasing Guide

![{Book name} kit parts laid out](./kit-parts.jpg)

{One paragraph: which kits the book uses, the all-in cost for one of each kit
and the per-student cost at a class of 20, and how long the slow-shipping route
takes.
This paragraph is the whole page in miniature — a teacher who reads only this
should know whether the kit fits their budget and their calendar.}

!!! note "Prices checked {Month Year}"
    Component prices move, and marketplace listings turn over constantly.
    Treat every figure here as a planning estimate, not a quote.

!!! warning "Don't order the wrong one: {the costly mistake}"
    {One or two sentences naming the near-identical part that will not work
    and how to tell them apart in a listing — e.g. "A Pico 2 (RP2350) is
    required; the original Pico (RP2040) has no FPU and cannot run Labs
    30–34. Check the listing title, sellers often list both side by side."}
    <!-- Optional: include only when one wrong order would break labs. -->

### Summary of Parts List

**Required**

- [{Part name}](#part-anchor) — {one clause on what it does} — {kits} ({qty-1 price})
- ...

**Optional**

- [{Part name}](#part-anchor) — {what it adds} — {kits} ({qty-1 price})
- ...

**Estimated total per kit:**

| Kit | One kit | Per student, class of 20 |
|-----|---------|--------------------------|
| {Kit name} | ${X} | ${Y} |

{If the one-kit total differs from the kit price quoted elsewhere in the book,
one or two sentences explaining why — usually single-unit shipping and
packaging on the small modules, and shared items excluded from the per-student
figure — and which order size lands on the quoted price.}

### {Required Part 1}

...one section per part, required parts first, in the order they appear above...

### Purchasing Strategy

{The lead-time and bulk-buying guidance — see the section below.}

### Classroom Order Worksheet

| Part | Required? | Used in kits | Qty per student | Qty for 20 students | Est. cost for 20 |
|------|-----------|--------------|-----------------|---------------------|------------------|
| ...  | Required  | {kits}       | 1               | 20                  | $XX              |
| **Total** | | | | | **$XXX** |
````

**The "Don't order the wrong one" box is optional.** Include it only when one
part has a near-twin that looks the same in listings but breaks the labs (Pico
vs Pico 2, 12V vs 5V LED strip, I2C vs SPI display). One box, at the top, for
the single most expensive mistake; smaller variant traps go in that part's own
section as a `!!! tip` callout.

**Explain the price gap.** Readers compare the guide's total to the "about $20
per student" quoted in the course description. If they differ, say why rather
than leaving a discrepancy that looks like an error.

## Part section template

````markdown
### {Part Name}

![{descriptive alt text}](./{image}.png)

**Used in:** {Kit A} (×{n}), {Kit B} (×{n})

**Used for:** [{Lab or lesson title}]({relative link to the lab}), [{...}](...)
— {one clause on what the part does in those labs}

{Two to four sentences: what the part is, what job it does *in this kit*, and
what a buyer needs to get right when choosing between listings — voltage,
pixel density, pin pitch, tactile-switch lead spacing. Name the specific
failure: "the 12V version of this strip will not work with the Pico's 5V
supply" is worth more than "make sure you get the right one".}

**Requirements:** {Costly or easy-to-overbuy items only — a computer, GPU,
display, chassis, anything over ~$20. State what it must *do* so nobody
overbuys: "must train a 20K-image model in 5–10 minutes; no overclocking or
water cooling needed", "must run MicroPython (≥16 KB RAM), so not an Arduino
Uno". Omit this line for commodity parts.}

!!! tip "{Variant trap, if any — e.g. Confirm SPI, not I2C}"
    {How to tell the right variant from a near-twin in the listing photos.
    Omit the callout when there is no such trap.}

**Prep work:** {What has to happen between the box arriving and a student
using it — soldering 22-gauge solid-core leads to the strip's pads so it
seats in a breadboard, cutting a 1-meter strip at the 30-pixel mark, marking
rails with a permanent marker, tinning stranded wire. Say roughly how long it
takes per kit, since that is prep time a teacher has to schedule. Write "None
— it is breadboard-ready as shipped." when there genuinely is none, because
the absence of prep work is itself useful information.}

**Cost:** ~${X} each in quantity 1 · ~${Y} each in a classroom order of 20+
· ~${Z} each at district scale (100+, {distributor, MOQ, shipping}) —
{what drives the difference: pack sizes, free-shipping thresholds, origin}.
Drop the district figure when no distributor tier exists.

**Trusted sellers:** {Only for parts that get counterfeited or relabeled —
genuine Raspberry Pi boards, branded sensors, lithium cells. Name the
authorized resellers (Micro Center, Adafruit, SparkFun, Digi-Key, PiShop.us)
and the tell-tale signs of a fake. Omit for commodity parts.}

**Spotting a bad batch:** {For cheap commodity parts (breadboards, buttons,
jumpers, LED strips): the common factory-second defect, ideally with a photo
— "bus-bar clips that are not bent, so wires will not seat" — and the house
advice: test on arrival, discard the odd bad unit rather than returning it,
and contact the seller only if more than a few fail. Omit when not relevant.}

**Search keywords:** `{primary phrase}`, `{alias}`, `{part number}`

**Where to buy:**

- [Search eBay for "..."](...)
- [Search AliExpress for "..."](...)
- [Search Amazon for "..."](...)
- {Optional: [Search Micro Center for "..."](...), [Search Alibaba for "..."](...)}
````

The optional lines — Requirements, the tip callout, Trusted sellers, Spotting
a bad batch, the district price — are there to be **used where they apply and
deleted where they do not.** A breadboard needs a bad-batch note and no
counterfeit warning; a Pico needs the reverse.

Two judgment calls worth making deliberately:

**Alt text.** Describe the part, not the file. `![Momentary push button with
four leads](...)` helps a screen-reader user and helps anyone whose image
failed to load. `![](...)` helps no one.

**Keywords.** The point is to give the reader the phrase that *works*, which is
often not the formal name. "WS2812B" finds the strip; "NeoPixel" mostly finds
Adafruit-branded product at three times the price; "addressable RGB LED strip"
finds a mix. Say so when the distinction costs money. Include part numbers
(`2N2222`, `PCF8574`) — they are the highest-signal search term there is.

## Purchasing strategy section

Every guide closes with this guidance. Adapt the specifics, keep the substance:

- **Lead time is the real tradeoff.** Direct-from-China listings on AliExpress
  and many eBay sellers run roughly 40–70% cheaper than Amazon Prime for the
  same commodity part, at 2–3 weeks of transit — sometimes 4–6 weeks around
  Lunar New Year, when Chinese factories and shipping largely stop for two
  weeks or more. Order a semester ahead and the savings are free; order the
  week before the unit starts and you pay the Amazon premium for the privilege.
- **Buy one, then buy twenty.** Order a single unit from a seller first,
  confirm it is the right part, *then* place the classroom order — ideally with
  the same seller, since listings for commodity parts vary in quality far more
  than the photos suggest.
- **Order spares.** 10–15% over the class count. Buttons get lost, strips get
  cut short, someone reverses power and ground. Spares are cheaper than a
  dead station in the middle of a lesson.
- **Watch the pack sizes.** Much of the classroom savings comes from pack
  breakpoints (breadboards in tens, buttons in hundreds) rather than negotiated
  per-unit discounts. Round the class order up to the pack, not to the roster.
- **Buy boards from authorized resellers.** Counterfeit and relabeled
  microcontroller boards turn up on general marketplaces; Raspberry Pi keeps a
  fixed retail price, so an authorized reseller (Micro Center, Adafruit,
  SparkFun, PiShop.us) is usually both cheaper and safer.
- **Expect the odd bad unit, not a bad order.** The cheapest commodity parts
  are sometimes factory seconds. Test on arrival and discard the occasional
  dud — at $1 a board, returns are not worth the time.
- **District-scale orders.** For 100+ units, a distributor such as Alibaba can
  cut the unit price by half again, at the cost of a minimum order, a flat
  shipping fee, and longer lead time.
- **Check the school's purchasing rules before promising the cheap route.**
  Many districts cannot reimburse AliExpress or direct international orders and
  require a domestic vendor with a W-9. If that is the constraint, the Amazon
  price is the real price — say so rather than quoting a number the teacher
  cannot actually use.

## Reference material

- `references/part-catalog.md` — house-observed price bands, search keywords,
  prep work, and known images for parts recurring across Moving Rainbow kits.
  **Read this before pricing anything** — it saves rediscovering the same
  numbers and keeps guides consistent with each other.
- `references/sourcing-strategy.md` — how to build a defensible price band,
  which marketplace wins for which part class, and the failure modes worth
  warning teachers about.
- `references/image-sourcing.md` — the license rules, the Wikimedia workflow,
  and when to write a generation brief instead.
- `assets/purchasing-guide-template.md` — the section skeleton to copy, with one
  worked part section showing the target depth.
- `assets/image-description-template.md` — the text-to-image brief to fill in
  when no usable photo of a part exists.

## Before you call it done

- Required parts appear before optional parts in the summary *and* the body.
- Every part section has the core pieces: image, **Used in** kits, a
  **Used for** line linking the labs, description, prep work, single and
  classroom prices, keywords, and search links. Optional lines (Requirements,
  variant tip, Trusted sellers, Spotting a bad batch, district price) appear
  where they apply and are deleted, not left as placeholders, where they do not.
- Every **Used for** lab link resolves.
- Costly items (over ~$20, or easy to overbuy) have a **Requirements** line.
- Parts prone to counterfeits name authorized resellers; cheap commodity parts
  that come in bad batches have a **Spotting a bad batch** note.
- **Search links only:** no buy link points at a specific listing — no eBay
  `/itm/`, Amazon `/dp/`, AliExpress `/item/`, or Alibaba `product-detail`
  URLs. (`grep -nE '/itm/|/dp/|/item/|product-detail'` on the page returns
  nothing.)
- Sources are limited to eBay, AliExpress, Amazon, Micro Center, Alibaba, and
  authorized specialty retailers.
- The Teacher's Guide page has front matter with a `title` and a
  `description` that mentions the Purchasing Guide.
- If one wrong order would break labs, the top-of-section "Don't order the
  wrong one" warning box is present.
- If the one-kit total differs from the kit price quoted elsewhere in the
  book, the gap is explained.
- Every summary bullet's anchor matches a real heading on the page.
- The guide is the `## Purchasing Guide` section of
  `docs/learning-graph/teachers-guide/index.md`, and the page uses one name
  consistently: Teacher's Guide, or Instructor's Guide for college and
  professional-development books.
- Every part used by any kit in the book appears exactly once.
- Every image path resolves from `docs/learning-graph/teachers-guide/`, and new
  part photos are stored in that directory.
- No image is hotlinked from a marketplace; anything sourced externally carries
  its license and attribution.
- Any part still missing art has a companion `*-image-description.md`.
- The page carries a "Prices checked {Month Year}" note.
- The order worksheet totals actually add up.
- The book's mascot does not appear anywhere in the Purchasing Guide.
