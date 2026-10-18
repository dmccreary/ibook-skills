# Image Brief: {Part Name}

Written for a text-to-image model because no suitably licensed photograph of
this part could be found. Replace every `{placeholder}` and delete this note
once the image exists.

## Prompt

> A single {part name}, {physical description — package type, body color,
> material, number and arrangement of leads or pins, any markings}, resting on
> a plain white seamless background. Soft, even product-photography lighting
> with no harsh shadows. Shot from a {low three-quarter / directly overhead /
> straight-on} angle. The part fills roughly 60% of the frame. Sharp focus
> throughout, high detail, no text overlay, no watermark, no hands, no
> packaging, no other objects.

## Physical details that must be right

A teacher will use this image to identify a part in their hand, so these are
the features that carry the recognition:

- **Size:** {approximate real dimensions, e.g. "6mm × 6mm × 5mm tall"}
- **Package / form factor:** {TO-92, 5mm radial, 2.54mm pitch DIP, etc.}
- **Color:** {body color and lead color}
- **Leads/pins:** {count, arrangement, spacing}
- **Distinguishing marks:** {printed part number, color bands, polarity notch,
  a flat face — whatever tells this part apart from its near-neighbors}

## What it must not look like

{The near-neighbor parts a reader could confuse it with, and how this one
differs. This is often the most valuable section of the brief — it is what
stops the generator producing a plausible-looking part that is subtly the
wrong component.}

## Aspect ratio and size

- Aspect ratio: {1:1 square / 4:3 landscape}
- Target: at least 800px on the long edge

## Where it goes

- File: `docs/learning-graph/teachers-guide/{part-slug}.png`
- Referenced from: the `## Purchasing Guide` section of
  `docs/learning-graph/teachers-guide/index.md` as `./{part-slug}.png`
- Alt text to use: `{descriptive alt text}`
