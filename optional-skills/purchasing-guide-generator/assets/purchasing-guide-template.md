<!-- ==================================================================
     This is the "## Purchasing Guide" section of
     docs/learning-graph/teachers-guide/index.md (titled "Instructor's
     Guide" in college and professional-development books). Paste it into
     that page as a section; do not replace the rest of the page. Part
     photos and image briefs live in docs/learning-graph/teachers-guide/.
     The page itself should carry front matter, e.g.
       ---
       title: Teacher's Guide
       description: Teaching notes for {Book}, including a Purchasing Guide
         with every kit part, prices, and where to buy each one.
       ---
     ================================================================== -->

## Purchasing Guide

![{Book name} kit parts laid out](./kit-parts.jpg)

{One paragraph. Which kits the book uses, what one of each kit costs all-in,
what it costs per student for a class of 20, and how far ahead a teacher needs
to order to get the cheap price. A teacher who reads only this paragraph should
know whether these kits fit their budget and their calendar.}

!!! note "Prices checked {Month Year}"
    Component prices move and marketplace listings turn over constantly. Treat
    every figure here as a planning estimate, not a quote.

<!-- Optional: keep only when one wrong order would break labs. -->
!!! warning "Don't order the wrong one: {the costly mistake}"
    {One or two sentences naming the near-identical part that will not work
    and how to tell them apart in a listing — e.g. "A Pico 2 (RP2350) is
    required; the original Pico (RP2040) has no FPU and cannot run Labs
    30–34. Check the listing title, sellers often list both side by side."}

### Summary of Parts List

**Required**

- [{Part name}](#anchor-slug) — {one clause on the job it does} — {kits} (~${X})
- [{Part name}](#anchor-slug) — {one clause on the job it does} — {kits} (~${X})

**Optional**

- [{Part name}](#anchor-slug) — {what it adds} — {kits} (~${X})
- [{Part name}](#anchor-slug) — {what it adds} — {kits} (~${X})

**Estimated total per kit:**

| Kit | One kit | Per student, class of 20 |
|-----|---------|--------------------------|
| {Kit name} | ~${X} | ~${Y} |

{If this differs from the kit price quoted elsewhere in the book, explain why:
single-unit shipping and packaging on small modules, shared tools excluded,
and which order size lands on the quoted price.}

---

<!-- ==================================================================
     One `###` section per part, each part listed once even when several
     kits use it. Required parts first, in the same order as the summary
     list above. The worked example below shows the
     target depth — match it, do not just fill the slots.
     ================================================================== -->

### Addressable LED Strip (WS2812B)

![WS2812B LED strip at 60 pixels per meter](./led-strip-60-pixels-per-meter.png)

**Used in:** {Kit name} (×1)

**Used for:** [{Lab title}]({relative link to lab}) — the strip is the output
for every animation lab.

The LED strip is what makes this kit worth building — a chain of WS2812B
"addressable" pixels, each containing a red, green and blue LED plus a small
controller that reads its own color off the data line and passes the rest
along. That single-wire chaining is why 30 pixels need only one GPIO pin.

We buy 1-meter strips at **60 pixels per meter** and cut each one in half, so
one strip yields two kits. Buy the **5V** version — the 12V WS2815 looks
identical in listing photos and will not run from the Pico's VBUS pin. **IP20**
(uncoated) is right for indoor classroom use; choose IP65 for take-home
projects and costumes.

**Prep work:** Cut the strip at the 30-pixel mark, following the copper pad
line. Solder 22-gauge **solid-core** wire to the three pads at the input end —
stranded wire will not seat in a breadboard. Slide colored heat shrink over
each lead before soldering and shrink it afterward; it strain-relieves the
joint, since WS2812B pads lift easily, and it color-codes power, ground and
data so students wire it correctly without tracing. Budget about 10 minutes per
strip.

![Where to cut the 1-meter strip at the 30-pixel mark](./led-strip-cut-point.jpg)

![22-gauge solid-core wire soldered to the strip pads](./wires-on-led-strip.jpg)

**Cost:** ~$3–6 per meter from eBay or AliExpress · ~$3 per meter in a
classroom order direct from China · ~$2 per meter at district scale from an
Alibaba reel listing (5 m reels, minimum order, flat shipping). The same strip runs $10–15 per meter on
Amazon, so this part is where ordering ahead saves the most money.

**Search keywords:** `WS2812B LED strip 60 LED/m 5V`, `addressable RGB LED
strip`, `WS2812B IP20 1m`. Note that **"NeoPixel" is Adafruit's brand name** for
this part — searching it returns Adafruit product at several times the price for
an electrically identical strip.

**Spotting a bad batch:** Test every strip with a simple rainbow sketch on
arrival. The usual defect is one dead pixel that stops the data chain, so
every pixel after it stays dark — cut the strip past the dead pixel and use
the shorter piece, rather than returning it.

**Where to buy:**

- [Search eBay for "WS2812B LED strip 60 LED/m 5V"](https://www.ebay.com/sch/i.html?_nkw=WS2812B+LED+strip+60+LED%2Fm+5V)
- [Search AliExpress for "WS2812B LED strip 60 LED/m 5V"](https://www.aliexpress.com/w/wholesale-ws2812b-led-strip-60-led-m-5v.html)
- [Search Amazon for "WS2812B LED strip 60 LED/m 5V"](https://www.amazon.com/s?k=WS2812B+LED+strip+60+LED%2Fm+5V)

---

### {Next Part}

![{descriptive alt text}](./{image}.png)

**Used in:** {Kit A} (×{n}), {Kit B} (×{n})

**Used for:** [{Lab title}]({relative link to lab}), [{...}](...) — {what the
part does in those labs}

{Two to four sentences: what it is, what job it does in this kit, and what a
buyer has to get right when choosing between listings.}

<!-- Optional lines below: keep where they apply, delete where they do not. -->

**Requirements:** {Costly items only: what it must do, so nobody overbuys.}

!!! tip "{Variant trap, e.g. Confirm SPI, not I2C}"
    {How to tell the right variant from its near-twin in listing photos.}

**Prep work:** {What happens between the box arriving and a student using it,
and roughly how long per kit. Write "None — it is breadboard-ready as shipped."
when there is none; that is useful information too.}

**Cost:** ~${X} each in quantity 1 · ~${Y} each in a classroom order of 20+
· ~${Z} each at district scale ({distributor, MOQ, shipping}) — {what drives
the difference}.

**Trusted sellers:** {Counterfeit-prone parts only: authorized resellers and
how to spot a fake.}

**Spotting a bad batch:** {Cheap commodity parts only: the usual defect, a
photo if possible, and "discard the odd dud rather than returning it".}

**Search keywords:** `{primary phrase}`, `{alias}`, `{part number}`

**Where to buy:**

- [Search eBay for "..."](...)
- [Search AliExpress for "..."](...)
- [Search Amazon for "..."](...)
- {Optional: Micro Center or Alibaba search link — search URLs only, never a
  specific `/itm/`, `/dp/`, `/item/` or `product-detail` listing}

---

### Purchasing Strategy

**Lead time is the real tradeoff.** Direct-from-China listings on AliExpress and
many eBay sellers run 40–70% cheaper than Amazon for the same commodity part,
at 2–3 weeks of transit — sometimes 4–6 weeks around Lunar New Year, when
Chinese factories and shipping largely stop. Order a semester ahead and the
savings are free; order the week before the unit starts and you pay the Amazon
premium for the privilege.

**Buy one, then buy twenty.** Order a single unit from a seller, confirm it is
the right part, then place the classroom order with that same seller. Listings
for commodity parts vary in quality far more than the photos suggest.

**Order spares.** Add 10–15% over the class count. Buttons get lost, strips get
cut short, someone reverses power and ground. Spares are cheaper than a dead
station in the middle of a lesson.

**Watch the pack sizes.** Most of the classroom savings comes from pack
breakpoints — breadboards in tens, buttons in hundreds — not from negotiated
discounts. Round the order up to the pack, not to the roster.

**Buy boards from authorized resellers.** Counterfeit and relabeled
microcontroller boards turn up on general marketplaces. Micro Center, Adafruit,
SparkFun and PiShop.us sell genuine boards at the fixed retail price.

**Expect the odd bad unit, not a bad order.** The cheapest commodity parts are
sometimes factory seconds. Test on arrival and discard the occasional dud; at
$1 a part, a return costs more time than it saves.

**District-scale orders.** For 100+ units, a distributor such as Alibaba can
halve the unit price again, at the cost of a minimum order quantity, a flat
shipping fee and a longer lead time.

**Check your district's purchasing rules first.** Many districts cannot
reimburse AliExpress or direct international orders and require a domestic
vendor with a W-9. If that is your constraint, the Amazon column is your real
price.

### Classroom Order Worksheet

| Part | Required? | Used in kits | Qty per student | Qty for 20 students | Est. cost for 20 |
|------|-----------|--------------|-----------------|---------------------|------------------|
<!-- For district orders, add a "Qty for 100+" and "Est. cost (distributor)" column. -->
| {Part} | Required | {Kit A} | 1 | 20 (2 packs of 10) | $XX |
| {Part} | Required | {Kit A}, {Kit B} | 2 | 40 (1 pack of 100) | $XX |
| {Part} | Optional | {Kit B} | 1 | 20 | $XX |
| | | | | **Required subtotal** | **$XXX** |
| | | | | **With optional parts** | **$XXX** |

**Per student:** ~${X} required · ~${Y} with optional parts

#### Shared classroom tools

Bought once and reused for years, so keep them out of the per-student figure.

| Tool | Cost | How many |
|------|------|----------|
| Soldering iron | $15–40 | 1 per 4–6 students |
| Solder | $8–15 | 1 spool per classroom |
| Wire strippers | $8–15 | 1 per pair |
| Heat gun | $15–25 | 1 per classroom |
