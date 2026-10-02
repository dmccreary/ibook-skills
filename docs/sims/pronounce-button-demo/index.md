---
title: Pronounce Button and Streaming Playback
description: Select a pronounce button beside a glossary term and compare streaming playback, where sound starts as soon as the first part of the file arrives, with waiting for the whole file to download.
image: /sims/pronounce-button-demo/pronounce-button-demo.png
og:image: /sims/pronounce-button-demo/pronounce-button-demo.png
twitter:image: /sims/pronounce-button-demo/pronounce-button-demo.png
social:
   cards: false
quality_score: 100
---

# Pronounce Button and Streaming Playback

<iframe src="main.html" height="502px" width="100%" scrolling="no"></iframe>

[Run the Pronounce Button and Streaming Playback MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

A **pronounce button** is a small control beside a defined term that plays
its spoken pronunciation. **Audio streaming playback** is delivering that
sound so it begins playing before the whole file has downloaded.

This MicroSim shows three glossary terms, each with a pronounce button, and
two timelines of the same audio clip:

- **Streaming playback.** The *Playback Position* marker starts moving as soon
  as the first part of the file arrives. The *Downloaded* marker keeps running
  ahead of it while the rest of the file is still on its way.
- **Download first, then play.** Nothing plays until the *Downloaded* marker
  reaches the end of the bar. The listener waits in silence.

Each timeline reports its **time to first sound**. That number is the whole
point of streaming: the clip is the same length either way, but the listener
hears the first word much sooner.

One rule holds on both timelines: the playback position can never pass the
downloaded marker. A player can only play audio it has already received. On a
slow connection the streaming player may catch up with the download and pause
until more audio arrives.

!!! note "A timing simulation, not a recording"
    No sound is played and nothing is downloaded. The clip length (4 seconds)
    and the connection speeds are example values chosen so the behavior is
    slow enough to watch. They are not measurements of any text-to-speech
    service.

| Setting | Normal connection | Slow connection |
|---------|------------------:|----------------:|
| Delay before the first part of the file arrives | 0.2 s | 0.6 s |
| Audio received per second | 4.0 s of audio | 0.8 s of audio |
| Time to first sound, streaming | 0.2 s | 0.6 s |
| Time to first sound, download first | about 1.1 s | about 5.3 s |

## How to Use

1. The MicroSim opens on a frozen example frame, 0.9 seconds after a click.
   Compare the two timelines: one is already playing, the other is silent.
2. Select a term's pronounce button, either the speaker icon beside the term
   or the button with the term's name below the drawing.
3. Watch the two *Playback Position* markers. Read each timeline's
   **First sound after** time.
4. Check **Simulate slow connection**. The clip restarts. Compare the two
   times to first sound again.
5. On the slow connection, watch the streaming timeline for the moment the
   playback position catches the downloaded marker and the player pauses.
6. Hover over either progress bar to read how that delivery method works.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/pronounce-button-demo/main.html"
        height="502px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who add audio to
intelligent textbooks. No programming background is needed.

### Learning Objective

Demonstrate how clicking a pronounce button begins audio streaming playback
before the full narration has loaded. (Bloom's Taxonomy: Apply)

### Duration

10 minutes

### Prerequisites

- Has read the definitions of *text-to-speech narration*, *audio streaming
  playback*, and *pronounce button* in Chapter 27
- Knows that a file takes time to download

### Activities

1. **Exploration** (3 min): Select each of the three pronounce buttons on a
   normal connection. Record the two times to first sound.
2. **Guided Practice** (4 min): Before checking **Simulate slow connection**,
   predict which time to first sound will change more. Check the box and
   compare the result with your prediction.
3. **Assessment** (3 min): Using the slow connection, explain to a partner why
   the streaming player paused, and why it still finished before the other
   timeline.

### Assessment

- The learner starts playback and points to the moment the streaming timeline
  begins playing while the file is still downloading.
- The learner states that the playback position can never pass the downloaded
  marker.
- The learner explains why a slow connection hurts "download first" far more
  than it hurts streaming.

### Discussion Questions

1. A pronounce clip is only a second or two long. A narrated chapter can be
   many minutes. For which one does streaming matter more, and why?
2. What does a listener experience when the playback position catches the
   downloaded marker?
3. Narration is an alternative to reading, not a replacement. Which readers
   benefit most from a pronounce button beside an unfamiliar term?

## References

1. [Streaming media](https://en.wikipedia.org/wiki/Streaming_media) - Wikipedia - Explains how media can be played while it is still being delivered, and what buffering is.
2. [Speech synthesis](https://en.wikipedia.org/wiki/Speech_synthesis) - Wikipedia - Background on text-to-speech, the technology behind a pronounce button.
3. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the drawing and timing functions used in this MicroSim.
