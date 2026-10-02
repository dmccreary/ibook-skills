---
title: Breadboard Tie Points and Animated Current Flow
description: Click any hole on a simplified solderless breadboard to see which holes share its internal strip, then complete a battery, resistor, and LED circuit and watch current flow around the closed loop.
image: /sims/breadboard-tie-points-current-flow/breadboard-tie-points-current-flow.png
og:image: /sims/breadboard-tie-points-current-flow/breadboard-tie-points-current-flow.png
twitter:image: /sims/breadboard-tie-points-current-flow/breadboard-tie-points-current-flow.png
social:
   cards: false
quality_score: 100
---

# Breadboard Tie Points and Animated Current Flow

<iframe src="main.html" height="522px" width="100%" scrolling="no"></iframe>

[Run the Breadboard Tie Points and Animated Current Flow MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

A **solderless breadboard** looks like a plain grid of holes. The connections
that matter are metal strips hidden under the plastic. Each hole is a
**tie point**, and every hole on the same strip belongs to the same tie point
group. Two holes that sit side by side can be on completely different strips.

This MicroSim uses a simplified board with three kinds of strip:

| Part of the board | Which holes are joined |
|-------------------|------------------------|
| Top power rail (+) | Every hole in the rail, lengthwise |
| Bottom power rail (&minus;) | Every hole in the rail, lengthwise |
| A numbered column, rows a to e | The 5 holes in that column above the center gap |
| A numbered column, rows f to j | The 5 holes in that column below the center gap |

The center gap separates rows a to e from rows f to j, so the two halves of a
column are not connected to each other.

A small circuit is already placed on the board:

1. The battery's + lead goes to the + rail.
2. An orange jumper wire runs from the + rail to hole a3.
3. A resistor runs from c3 to c7. It limits the current through the LED.
4. An LED straddles the center gap, with one leg in e7 and the other in f7.
5. The battery's &minus; lead goes to the &minus; rail.

One connection is missing. Nothing joins column 7 (rows f to j) to the
&minus; rail, so the loop is open and no current flows. The **Complete the
Circuit** button adds the final jumper wire, from j7 to the &minus; rail. The
loop closes, moving dots show the current, and the LED lights.

The dots show conventional current, which runs from the battery's + terminal
around the loop to its &minus; terminal. Orange bands mark the parts of the
path that run through strips inside the board.

!!! note "Simplifications"
    A real breadboard usually has a + and a &minus; rail on each long edge,
    and some boards split their rails at the middle. This board has one rail
    at the top and one at the bottom. The component values are not modeled:
    the LED is either dark or lit.

## How to Use

1. Click any hole. Every hole joined to it under the board is highlighted, and
   the panel names the **same tie point group**. Click the same group again to
   clear the highlight.
2. Click a hole in the next column. Notice that the highlight moves to a
   different group: adjacent does not mean connected.
3. Click hole e7, then hole f7. They are in the same column but on opposite
   sides of the center gap, so they are in different groups. That is why the
   LED can sit across the gap without being shorted out.
4. Click a hole in the + rail to see a whole rail light up.
5. Read the red message. It names the connection that is missing.
6. Select **Complete the Circuit**. Follow the dots from the battery, through
   the jumper, the resistor, and the LED, and back to the battery.
7. Select **Reset** to remove the final jumper and try again.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/breadboard-tie-points-current-flow/main.html"
        height="522px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers studying how a
domain-specific skill extends a general skill library. The MicroSim also suits
beginning electronics students. No electronics background is needed.

### Learning Objective

Demonstrate which breadboard holes are electrically connected, and how current
flows once a simple LED circuit is completed. (Bloom's Taxonomy: Apply)

### Duration

15 minutes

### Prerequisites

- Knows that a battery has a positive and a negative terminal
- Has read the definitions of *solderless breadboard* and *breadboard tie
  points* in Chapter 28

### Activities

1. **Exploration** (4 min): Click at least ten holes in different parts of the
   board. State the rule for the rails and the rule for the columns in your
   own words.
2. **Guided Practice** (6 min): Before selecting **Complete the Circuit**,
   trace the circuit with your finger from the battery's + terminal and find
   the place where the path stops. Then complete the circuit and check.
3. **Assessment** (5 min): Answer the questions below.

### Assessment

- The learner predicts correctly, for any two holes, whether they are
  connected.
- The learner explains why the LED's two legs are not connected to each other
  through the board.
- The learner names the missing connection before completing the circuit.
- The learner states that current flows only when the loop is closed.

### Discussion Questions

1. If both legs of the resistor were pushed into holes c3 and d3, what would
   happen, and why?
2. The orange jumper enters the + rail one hole away from the battery's lead.
   Why does that still work?
3. A general MicroSim generator does not know what a tie point is. What would
   a simulation built without that knowledge get wrong?

## References

1. [Breadboard](https://en.wikipedia.org/wiki/Breadboard) - Wikipedia - Describes solderless breadboards, their terminal strips and bus strips, and how the holes are connected internally.
2. [Light-emitting diode](https://en.wikipedia.org/wiki/Light-emitting_diode) - Wikipedia - Background on LEDs, including polarity and the need for a current-limiting resistor.
3. [Electric current](https://en.wikipedia.org/wiki/Electric_current) - Wikipedia - Explains conventional current and why a closed circuit is needed for current to flow.
4. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the drawing and mouse functions used in this MicroSim.
