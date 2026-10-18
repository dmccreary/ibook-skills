# Part Catalog

> **Paths:** every `docs/...` path in this catalog is in the moving-rainbow
> repo (`~/Documents/ws/moving-rainbow/`). From another book, copy the image
> into `docs/learning-graph/teachers-guide/` rather than linking across repos.

House-observed data for the parts that recur across Moving Rainbow kits. Read
the rows you need before pricing a guide — reusing these numbers is what keeps
one kit's purchasing guide consistent with the next one's, and it saves
rediscovering the same figures every time.

**These are planning bands, not quotes.** They come from this repo's own
documentation and from the project's buying history. Commodity electronics
prices drift, and marketplace listings turn over constantly. If web search is
available, spot-check anything that will drive a big classroom order before
publishing, and stamp the guide with the month you checked.

## Contents

- [Microcontrollers](#microcontrollers)
- [LEDs and strips](#leds-and-strips)
- [Breadboards and wiring](#breadboards-and-wiring)
- [Inputs and switches](#inputs-and-switches)
- [Discrete components](#discrete-components)
- [Power](#power)
- [Enclosure and mounting](#enclosure-and-mounting)
- [Tools a classroom needs once](#tools-a-classroom-needs-once)

## Microcontrollers

### Raspberry Pi Pico / Pico 2

- **Qty 1:** $3.99 at Micro Center (the project's standing source; seen as low
  as $2.99 on sale). $4–6 elsewhere. **Qty 20+:** $3.99 each — Micro Center
  does not discount further, but it also does not need to.
- **Prep:** Boards ship with headers unsoldered unless the listing says "with
  headers" or "H" — for breadboard use, buy the pre-soldered "H" variant or
  budget ~5 minutes of soldering per board. This is the single most common
  purchasing mistake on this part.
- **Keywords:** `Raspberry Pi Pico`, `Raspberry Pi Pico 2`, `Pico H` (headers
  pre-soldered), `Pico W` (WiFi, ~$6), `RP2040`, `RP2350`
- **Sites:** Micro Center first, then Adafruit/SparkFun. Marketplace listings
  are frequently clones — fine for classroom use but verify before bulk buying.
- **Images:** `docs/img/raspberry-pi-pico.png`,
  `docs/img/raspberry-pi-pico-pinout.png`, `docs/img/pico-2-r4-pinout.svg`
- **Source:** `~/Documents/ws/moving-rainbow/docs/getting-started/dev-boards.md`

## LEDs and strips

### WS2812B addressable LED strip (NeoPixel)

- **Qty 1:** ~$3–6 per meter at 60 pixels/m, IP20, from eBay/AliExpress;
  $10–15/m for the same thing on Amazon. **Qty 20+:** ~$3/meter direct from
  China. 144 pixels/m runs roughly double 60 pixels/m.
- **Prep:** Solder 22-gauge solid-core leads to the strip's pads so it seats
  in a breadboard — stranded wire will not. The base kit cuts a 1-meter strip
  at the 30-pixel mark to yield two kits. Budget ~10 minutes per strip end.
- **Keywords:** `WS2812B LED strip`, `WS2812B 60 LED/m 5V`, `addressable RGB
  LED strip`. Note in the guide that **"NeoPixel" is Adafruit's brand name** —
  searching it returns Adafruit product at a large premium for an electrically
  identical part.
- **Buying gotchas worth stating explicitly:** get **5V**, not 12V (the 12V
  WS2815 will not run from the Pico's VBUS); choose **IP20** for indoor
  classroom use, IP65 for take-home and costumes, IP67 for outdoors; check
  whether the listing price is per meter or per 5-meter reel.
- **Images:** `docs/img/led-strip-60-pixels-per-meter.png`,
  `docs/img/led-strip-cut-point.jpg`, `docs/img/wires-on-led-strip.jpg`,
  `docs/img/led-strip-ebay-listing.png`, `docs/img/neopixel-types.jpg`
- **Source:** `~/Documents/ws/moving-rainbow/docs/getting-started/parts.md`

### 5V LED noodle (flexible filament)

- **Qty 1:** $1–3, available in five colors. **Qty 20+:** ~$1 each.
- **Prep:** Leads are fine and fragile; tin them before breadboard use.
- **Keywords:** `5V LED filament`, `LED noodle flexible`, `COB LED filament 5V`
- **Source:** `~/Documents/ws/moving-rainbow/docs/kits/analog-nightlight/index.md`

## Breadboards and wiring

### Solderless breadboard, 400 tie points (half size)

- **Qty 1:** ~$2–4. **Qty 20+:** ~$1–2 each in packs of 10 or 20 — this part
  has one of the steepest pack discounts in the kit.
- **Prep:** House practice is to mark the rails with permanent marker — black
  for GND, red for power, yellow for the GPIO 0 data pin. Two minutes per
  board and it eliminates a whole category of wiring mistakes.
- **Keywords:** `400 tie point breadboard`, `half size solderless breadboard`,
  `MB-102 breadboard` (the 830-point full size, if a kit needs the room)
- **Images:** `docs/img/breadboard.jpg`, `docs/img/breadboard-with-marks.jpg`,
  `docs/img/solderless-breadboards.png`, `docs/img/pico-on-breadboard-marks-led.jpg`

### 22-gauge solid-core hookup wire

- **Qty 1:** ~$8–15 for a multi-color spool set. **Qty 20+:** one spool set
  serves a whole classroom — price it per classroom, not per student, and say
  so.
- **Prep:** Cut to length and strip ~1/4". Solid core is not optional: stranded
  wire frays and will not enter a breadboard tie point.
- **Keywords:** `22 AWG solid core hookup wire kit`, `22 gauge solid wire
  breadboard`, `jumper wire kit solid core`
- **Images:** `docs/img/22-gage-solid-wires-for-breadboard.jpg`

### Heat shrink tubing

- **Qty 1:** ~$6–12 for an assorted multi-color, multi-diameter box.
  **Qty 20+:** one assortment box prepares a whole classroom's strips — price
  it per classroom, not per student.
- **Prep:** House practice is to slide colored heat shrink over each soldered
  strip lead before soldering, then shrink it with a heat gun. It strain-relieves
  the joint (the pads on a WS2812B strip lift easily) and color-codes the three
  wires so students wire power, ground and data correctly without tracing.
- **Keywords:** `heat shrink tubing assortment kit`, `3:1 adhesive lined heat
  shrink`, `colored heat shrink tubing 2mm 3mm`
- **Images:** `docs/img/heat-gun-on-shrink-wrap.jpg`
- A heat gun ($15–25) or the side of a soldering iron does the shrinking; a
  hair dryer generally will not get hot enough.

### Dupont jumper wires (pre-made)

- **Qty 1:** ~$2–5 for 40–120 wires. **Qty 20+:** ~$1.50–3 per bundle.
- **Keywords:** `dupont jumper wires male to male`, `breadboard jumper wire kit`
- Specify the gender combination the kit needs; M-M, M-F and F-F are different
  orders and a mismatched bundle is useless.

## Inputs and switches

### Momentary push button (tactile switch, 6mm)

- **Qty 1:** ~$0.10–0.25. **Qty 20+:** effectively free — packs of 100 run
  $5–10, so buy the pack and stop thinking about it.
- **Prep:** The 4-pin 6mm tactile switch straddles a breadboard's center
  channel as-is. Optional colored caps make mode buttons easier to teach.
- **Keywords:** `6x6mm tactile push button switch`, `momentary tactile switch
  4 pin breadboard`, `12x12mm tactile switch with cap` (the larger, easier
  variant), `tactile switch caps`
- **Buying gotcha:** the 4 pins are two pairs internally connected; wiring
  across the wrong pair makes the button appear permanently pressed.
- **Images:** `docs/img/momentary-push-button.png`,
  `docs/img/tactile-switch-on-breadboard.jpg`, `docs/img/button-caps.png`,
  `docs/img/momentary-push-buttons-ebay.png`

### Rotary encoder (KY-040)

- **Qty 1:** ~$1–2. **Qty 20+:** ~$0.60–1 each in packs of 5–10.
- **Prep:** Module versions are breadboard-ready; bare encoders need leads.
- **Keywords:** `KY-040 rotary encoder module`, `rotary encoder with push button`

### Photoresistor (LDR / CdS cell)

- **Qty 1:** ~$0.20. **Qty 20+:** packs of 20–100 for a few dollars.
- **Keywords:** `photoresistor LDR 5mm`, `GL5528 photoresistor`, `light
  dependent resistor assortment`
- **Images:** `~/Documents/ws/moving-rainbow/docs/kits/analog-nightlight/photoresistor.png`
- **Source:** `~/Documents/ws/moving-rainbow/docs/kits/analog-nightlight/index.md`

## Discrete components

### 2N2222 NPN transistor

- **Qty 1:** ~$0.20. **Qty 20+:** packs of 50–100 for $5–8.
- **Keywords:** `2N2222 NPN transistor TO-92`, `PN2222A transistor pack`
- **Buying gotcha:** pinout differs between TO-92 packages from different
  makers — tell readers to check the datasheet for their marking.

### Resistor assortment

- **Qty 1:** ~$0.10 per resistor, but nobody buys one. **Classroom:** a 600-
  to 1000-piece assortment kit runs $8–15 and covers every kit in the series.
  Price it per classroom.
- **Keywords:** `1/4W resistor assortment kit`, `10K ohm resistor 1/4 watt`,
  `resistor kit 600 pcs`

### Potentiometer (100K)

- **Qty 1:** ~$0.30–1. **Qty 20+:** ~$0.20–0.40 each in packs of 10–20.
- **Keywords:** `100K linear potentiometer breadboard`, `B100K potentiometer
  3 pin`, `10K trimmer potentiometer` (the small board-mount version)

## Power

Full comparison table lives in
`~/Documents/ws/moving-rainbow/docs/getting-started/batteries.md` —
link to it rather than duplicating it.

| Source | Qty 1 | Notes for classroom orders |
|--------|-------|----------------------------|
| USB wall adapter (5V) | ~$2 | Cheapest reliable classroom power; check it is 5V and ≥1A |
| USB power pack | $10–30 | Some auto-shut-off at low draw — a real problem with dim LED patterns |
| 3× AA battery pack | $1.50–6 for the cells | 4.5V; safest option for younger students |
| Flat LiPo | $5–15 | Medium-high risk; needs a charge manager. Check school policy first |
| 18650 cell | $5–10 each | Medium-high risk; counterfeit capacity claims are rampant |
| Coin cell CR2032 | $1–2 | 1–3 LED projects only |

- **USB cable:** confirm the connector the board actually uses — micro-USB on
  the original Pico, USB-C on several clones. Getting this wrong is a common
  and entirely avoidable ordering error. Keywords: `micro USB data cable`
  (must be a **data** cable, not charge-only), `USB-C data cable`.
- **Images:** `docs/img/3-aa-battery-pack.png`, `docs/img/lipo-battery.jpg`,
  `docs/img/battery-collection.jpg`, `docs/img/micro-usb.png`

## Enclosure and mounting

### 3-screw terminal header

- **Qty 1:** ~$0.30–0.80. **Qty 20+:** ~$0.20–0.40 each in packs of 10–20.
- **Prep:** Lets students swap strips and rings without re-soldering, and
  survives a backpack. Match the pitch (5.08mm is the common breadboard-
  friendly size) — this is the spec people get wrong.
- **Keywords:** `3 pin screw terminal block 5.08mm`, `PCB screw terminal
  connector 3 way`
- **Images:** `docs/img/3-terminal-screw-header.png`,
  `docs/img/screw-header-near-breadboard.png`, `docs/img/screw-header-blue.png`

### Acrylic / plexiglass base

- **Qty 1:** $2–5 cut to size. **Qty 20+:** cheapest by far as one large sheet
  cut down locally, or as scrap from a maker space.
- **Prep:** Drill mounting holes; peel the protective film only at the end.
- **Keywords:** `acrylic sheet 3mm clear`, `plexiglass sheet cut to size`

### Pin headers

- **Qty 1:** ~$0.20 per strip. **Qty 20+:** a 40-pin strip pack for a few
  dollars covers a class.
- **Keywords:** `2.54mm pin header male 40 pin`, `female header strip 2.54mm`
- **Images:** `docs/img/headers.png`

## Tools a classroom needs once

These are not per-student costs and should be listed separately from the
per-kit bill of materials so they do not inflate the per-student figure.

| Tool | Cost | Notes |
|------|------|-------|
| Soldering iron | $15–40 | One per 4–6 students; check school policy on irons in the classroom |
| Solder (60/40 or lead-free) | $8–15 | One spool per classroom |
| Wire strippers | $8–15 | One per pair of students |
| Flush cutters | $5–10 | For trimming leads |
| Hot glue gun | $5–15 | Kits with craft enclosures |
| Multimeter | $10–25 | One or two per classroom for debugging |

The repo documents the project's soldering-party approach for prepping kits in
bulk (`docs/img/solder-party-*.jpeg`) — worth linking from any guide whose
parts need lead soldering, since prepping 20 strips is a social event, not a
solo evening.
