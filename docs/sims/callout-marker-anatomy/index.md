---
title: Callout Marker Anatomy
description: Drag numbered markers on an annotation-free illustration and watch each marker's stored x and y coordinate change in a table, with leader lines that can be turned on and off.
image: /sims/callout-marker-anatomy/callout-marker-anatomy.png
og:image: /sims/callout-marker-anatomy/callout-marker-anatomy.png
twitter:image: /sims/callout-marker-anatomy/callout-marker-anatomy.png
social:
   cards: false
quality_score: 100
---

# Callout Marker Anatomy

<iframe src="main.html" height="452px" width="100%" scrolling="no"></iframe>

[Run the Callout Marker Anatomy MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

An interactive infographic overlay has three parts that work together, and
this MicroSim shows all three at once:

1. **An annotation-free illustration.** The picture on the left stands in for
   a generated image. It contains shapes only: a sun, a mountain, and a lake.
   There is no text in the pixels.
2. **Callout markers with stored coordinates.** The three numbered circles are
   drawn by code on top of the picture. Each marker's position is a pair of
   numbers stored in data, shown in the table.
3. **Leader lines and labels.** Each label sits outside the illustration, and
   a leader line connects it to its marker so nobody has to guess which label
   belongs to which point.

The coordinates use the same convention as the `data.json` file read by this
book's callout overlay engine: **x** is a percentage of the image width
measured from the left edge, and **y** is a percentage of the image height
measured from the top edge. Because the values are percentages rather than
pixels, a marker stays on its feature when the image is shown at a different
size.

| Marker | Label | Default x | Default y |
|:------:|-------|----------:|----------:|
| 1 | Sun | 78.0 | 22.0 |
| 2 | Mountain | 38.0 | 50.0 |
| 3 | Lake | 64.0 | 82.0 |

The picture is a placeholder drawn with shapes. It is not a generated image,
because the point here is the relationship between the marker, its
coordinate, and its leader line.

## How to Use

1. Look at the three markers, their leader lines, and the table of stored
   coordinates.
2. Drag marker **1** off the sun. Watch its x and y change in the table while
   you drag. The picture does not change at all.
3. Read the message under the table. It tells you when a marker is no longer
   sitting on the feature its label names.
4. Drag the marker back onto the sun. You have just corrected a label by
   editing data, without regenerating the picture.
5. Uncheck **Show leader lines**. The labels are now disconnected from their
   markers. Check the box again.
6. Click a label to select its marker without moving it.
7. Select **Reset Positions** to restore the default coordinates.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/callout-marker-anatomy/main.html"
        height="452px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who build labeled
diagrams for intelligent textbooks. No programming background is needed.

### Learning Objective

Explain how a stored marker coordinate, a leader line, and a label work
together on an annotation-free illustration. (Bloom's Taxonomy: Understand)

### Duration

10 minutes

### Prerequisites

- Knows what an interactive infographic overlay and an annotation-free
  illustration are (Chapter 25)
- Can read a small table of numbers

### Activities

1. **Exploration** (3 min): Drag each marker to a corner of the illustration
   and read its x and y. Work out which corner is (0, 0) and which is
   (100, 100).
2. **Guided Practice** (4 min): Select **Reset Positions**. Without dragging,
   predict the x and y you would store to put marker 2 on the mountain's snow
   cap. Drag the marker there and compare.
3. **Assessment** (3 min): Explain to a partner, in three sentences, what the
   marker, the stored coordinate, and the leader line each contribute.

### Assessment

- The learner states that a marker's position is stored as data and is not
  part of the picture.
- The learner explains that x and y are percentages of the image width and
  height, measured from the top-left corner.
- The learner explains what a leader line adds when a label sits outside the
  illustration.
- The learner describes how to fix a misplaced marker without regenerating the
  illustration.

### Discussion Questions

1. Why store a marker position as a percentage of the image size instead of a
   pixel count?
2. A marker sits slightly off the feature it labels. Give two ways to fix it,
   and say which one is cheaper and why.
3. What would a reader lose if the labels were printed inside the picture
   instead of drawn by code?

## References

1. [Callout](https://en.wikipedia.org/wiki/Callout) - Wikipedia - Describes callouts and the leader lines that connect a label to a feature in an illustration.
2. [Technical illustration](https://en.wikipedia.org/wiki/Technical_illustration) - Wikipedia - Background on labeled illustrations and their conventions.
3. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the drawing and mouse functions used in this MicroSim.
