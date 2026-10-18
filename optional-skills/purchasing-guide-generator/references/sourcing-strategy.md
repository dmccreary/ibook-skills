# Sourcing Strategy

How to build price bands a teacher can actually plan against, and which
marketplace to point them at for which kind of part.

## Building an honest price band

A purchasing guide's credibility rests on its numbers. Three rules keep them
defensible:

**Quote ranges, not points.** `~$3–6 per meter` survives six months of price
drift. `$4.17` looks authoritative, is wrong within a week, and teaches readers
to distrust the rest of the page. The exception is a genuinely fixed, verified
price from a specific vendor — the Pico at Micro Center is $3.99 and has been
for years, so say $3.99 and name the vendor.

**Say what drives the classroom price.** "$1–2 each in packs of 10" tells a
teacher *why* the number dropped and lets them do their own arithmetic when the
pack sizes differ. Bare per-unit numbers with no mechanism read as guesses.

**Stamp the date.** Every guide carries a "Prices checked {Month Year}" note.
This is the single cheapest thing you can do for a page that will be read for
years. It converts "these prices are wrong" into "these prices are old", which
is a completely different reader experience.

If web search is available, verify anything that will drive a large classroom
order before publishing. If it is not available, use the bands in
`part-catalog.md` and say plainly that they are planning estimates.

## The price tiers

Most commodity electronics parts land in a predictable spread, and naming the
tiers helps teachers understand the tradeoff rather than just seeing numbers:

| Tier | Typical multiplier | Lead time | When it is the right call |
|------|-------------------|-----------|---------------------------|
| Direct from China (AliExpress, most cheap eBay sellers) | 1× (baseline) | 2–3 weeks, occasionally 6 | Planned a semester ahead; large classroom orders |
| Domestic marketplace (Amazon, US-warehouse eBay) | 2–3× | 1–3 days | Replacements mid-unit; districts that cannot buy internationally |
| Specialty retailer (Adafruit, SparkFun, Digi-Key, Micro Center) | 1.5–4× | 2–5 days | Boards, anything where authenticity matters, anything needing support |
| Distributor / factory direct (Alibaba) | 0.4–0.7× | 3–6 weeks | District-scale orders (100+); minimum order quantity and a flat shipping fee |

The exception worth remembering: Micro Center's $3.99 Pico beats every other
channel including AliExpress. Loss-leader pricing on flagship boards means the
tiers do not always hold — check rather than assume.

## Which site for which part

- **eBay** — best default for commodity passives, strips, breadboards, and
  buttons. Mixed domestic and international sellers, so a teacher can choose
  their own lead time from one search. Filter to "Buy It Now".
- **AliExpress** — cheapest for bulk classroom orders of anything commodity.
  Sold in pack sizes that suit a class of 20. Slowest. Many districts cannot
  reimburse it, so never present it as the only option.
- **Amazon** — the reliable fallback, and often the *only* option a school's
  purchasing system accepts. Always include it even when it is the most
  expensive, because for many readers it is the real price.
- **Alibaba** — the district tier. Factory-direct listings with a minimum
  order (often 20–100) and a flat shipping fee, e.g. 400-tie breadboards at
  about $0.40 each with $20 shipping. Worth a line only for parts a district
  buys by the hundred. Link a search, never a `product-detail` listing.
- **Micro Center** — Raspberry Pi boards, and only worth linking when there is
  a store in reach or the online price justifies shipping.
- **Adafruit / SparkFun** — link when the part genuinely benefits from vetted
  quality, good documentation, or a tutorial a teacher can hand to students.
  Note the premium honestly rather than pretending it does not exist.
- **Digi-Key / Mouser** — for a district buying in real quantity with a
  purchase order, exact part numbers, and a need for authentic components.

## Failure modes worth warning teachers about

Each of these has cost this project money or class time. When a part is
vulnerable to one, put the warning directly in that part's description — not in
a general caveats section nobody reads.

- **Voltage mismatch.** 12V LED strips look identical to 5V strips in listing
  photos. The 12V part will not run from a Pico.
- **Charge-only USB cables.** A cable that powers the board but carries no data
  produces a board that appears completely dead to Thonny. Specify "data cable".
- **Headers not included.** Bare boards need soldering; "H" variants do not.
- **Per-meter vs. per-reel pricing.** A $15 listing may be five meters or one.
- **Stranded where solid is required.** Stranded wire will not enter a
  breadboard tie point, and stranded strip leads will not either.
- **Counterfeit or overstated capacity.** Rampant on 18650 cells and power
  banks. Buy a sample before the classroom order.
- **Pack size mismatch.** Buying 20 of something sold in packs of 10 sometimes
  costs more than buying two packs of 10 plus shipping. Round to the pack.

## Classroom arithmetic

When computing the per-student figure for a class of 20:

1. Round every part up to its next pack breakpoint. Twenty students needing 40
   buttons means one pack of 100, not 40 buttons.
2. Add 10–15% spares on anything consumable or losable.
3. Keep shared tools (irons, strippers, glue guns, multimeters) in a separate
   table. Folding a $30 soldering iron into a per-student number makes a $12
   kit look like a $14 kit and misrepresents the recurring cost — the iron is
   bought once and used for years.
4. State both totals: cost for one kit, and cost per student at 20. Teachers
   pitching a purchase need the second; parents building one at home need the
   first.
