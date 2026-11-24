---
title: {MASCOT_NAME} Mascot Image Test
description: Visual and pixel-level transparency and trim-border checks for all seven {MASCOT_NAME} mascot poses.
hide:
  toc
---

# {MASCOT_NAME} Mascot Image Test

This page tests every production mascot PNG in two ways:

1. Each image is drawn over checkerboard and dark backgrounds so opaque boxes,
   halos, and edge contamination are easy to spot.
2. A browser-side pixel test checks for an RGBA transparency region, transparent
   corners, and the **4 px content border** produced by
   `trim-padding-from-image.py` (using the script's alpha threshold of 10).

<div id="mascot-test-summary" class="mascot-test-summary" role="status">
  Running pixel checks…
</div>

<div class="mascot-test-grid">
  <article class="mascot-test-card" data-name="Neutral" data-src="../../img/mascot/neutral.png">
    <h2>Neutral</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/neutral.png" alt="{MASCOT_NAME} in a neutral pose on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/neutral.png" alt="{MASCOT_NAME} in a neutral pose on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Welcome" data-src="../../img/mascot/welcome.png">
    <h2>Welcome</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/welcome.png" alt="{MASCOT_NAME} waving on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/welcome.png" alt="{MASCOT_NAME} waving on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Thinking" data-src="../../img/mascot/thinking.png">
    <h2>Thinking</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/thinking.png" alt="{MASCOT_NAME} thinking on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/thinking.png" alt="{MASCOT_NAME} thinking on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Tip" data-src="../../img/mascot/tip.png">
    <h2>Tip</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/tip.png" alt="{MASCOT_NAME} pointing upward on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/tip.png" alt="{MASCOT_NAME} pointing upward on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Warning" data-src="../../img/mascot/warning.png">
    <h2>Warning</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/warning.png" alt="{MASCOT_NAME} warning the reader on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/warning.png" alt="{MASCOT_NAME} warning the reader on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Encouraging" data-src="../../img/mascot/encouraging.png">
    <h2>Encouraging</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/encouraging.png" alt="{MASCOT_NAME} giving a thumbs-up on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/encouraging.png" alt="{MASCOT_NAME} giving a thumbs-up on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>

  <article class="mascot-test-card" data-name="Celebration" data-src="../../img/mascot/celebration.png">
    <h2>Celebration</h2>
    <div class="mascot-test-swatches">
      <div class="mascot-test-swatch checker"><img src="../../img/mascot/celebration.png" alt="{MASCOT_NAME} celebrating on a checkerboard transparency test"></div>
      <div class="mascot-test-swatch dark"><img src="../../img/mascot/celebration.png" alt="{MASCOT_NAME} celebrating on a dark transparency test"></div>
    </div>
    <p class="mascot-test-result">Waiting for pixel test…</p>
  </article>
</div>

<noscript>
JavaScript is required for the pixel-level checks. The visual transparency
swatches above still work without it.
</noscript>

## Mascot admonitions

!!! mascot-neutral "General Note"
    ![{MASCOT_NAME} neutral pose](../img/mascot/neutral.png){ class="mascot-admonition-img" }
    This is the neutral style, used for general sidebars or introductions.

!!! mascot-welcome "Welcome!"
    ![{MASCOT_NAME} waving welcome](../img/mascot/welcome.png){ class="mascot-admonition-img" }
    This is the welcome style, used at chapter openings.

!!! mascot-thinking "Key Insight"
    ![{MASCOT_NAME} thinking](../img/mascot/thinking.png){ class="mascot-admonition-img" }
    This is the thinking style, used for key concepts.

!!! mascot-tip "Helpful Tip"
    ![{MASCOT_NAME} giving a tip](../img/mascot/tip.png){ class="mascot-admonition-img" }
    This is the tip style, used for hints and advice.

!!! mascot-warning "Watch Out!"
    ![{MASCOT_NAME} warning](../img/mascot/warning.png){ class="mascot-admonition-img" }
    This is the warning style, used for common mistakes.

!!! mascot-encourage "Keep Going!"
    ![{MASCOT_NAME} encouraging](../img/mascot/encouraging.png){ class="mascot-admonition-img" }
    This is the encouraging style, used for difficult content.

!!! mascot-celebration "Well Done!"
    ![{MASCOT_NAME} celebrating](../img/mascot/celebration.png){ class="mascot-admonition-img" }
    This is the celebration style, used for achievements.

<style>
.mascot-test-summary {
  margin: 1rem 0;
  padding: .75rem 1rem;
  border: 2px solid #546e7a;
  border-radius: .4rem;
  font-weight: 700;
}
.mascot-test-summary.pass { border-color: #2e7d32; background: #e8f5e9; color: #1b5e20; }
.mascot-test-summary.fail { border-color: #c62828; background: #ffebee; color: #b71c1c; }
.mascot-test-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
  gap: 1rem;
}
.mascot-test-card {
  margin: 0;
  padding: .8rem;
  border: 2px solid #90a4ae;
  border-radius: .5rem;
}
.mascot-test-card.pass { border-color: #43a047; }
.mascot-test-card.fail { border-color: #e53935; }
.mascot-test-card h2 { margin: 0 0 .6rem; }
/* Swatches shrink-wrap each pose: the checkerboard ends where the PNG ends,
   so there is no empty space beside the bird and the 4 px trim border is
   visible against the swatch outline. */
.mascot-test-swatches {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: .5rem;
}
.mascot-test-swatch {
  flex: 0 0 auto;
  max-width: 100%;
  padding: 0;
  line-height: 0;
  border: 1px solid rgba(127, 127, 127, .5);
}
.mascot-test-swatch.checker {
  background-color: #fff;
  background-image:
    linear-gradient(45deg, #cfd8dc 25%, transparent 25%),
    linear-gradient(-45deg, #cfd8dc 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #cfd8dc 75%),
    linear-gradient(-45deg, transparent 75%, #cfd8dc 75%);
  background-position: 0 0, 0 8px, 8px -8px, -8px 0;
  background-size: 16px 16px;
}
.mascot-test-swatch.dark { background: #17131f; }
/* Height is fixed and width follows each pose's aspect ratio (same rule as
   .md-typeset img.mascot-admonition-img in css/mascot.css), so the image box
   never letterboxes the pose. */
.md-typeset .mascot-test-swatch img {
  display: block;
  width: auto;
  height: auto;
  max-height: 12rem;
  max-width: 100%;
}
.mascot-test-result { margin: .7rem 0 0; font-size: .82rem; line-height: 1.45; }
.mascot-test-result strong { display: inline-block; margin-right: .25rem; }
</style>

<script>
(() => {
  const threshold = 10;
  const expectedBorder = 4;
  const cards = [...document.querySelectorAll('.mascot-test-card[data-src]')];
  const summary = document.getElementById('mascot-test-summary');

  function inspect(card) {
    return new Promise((resolve) => {
      const image = new Image();
      image.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        const context = canvas.getContext('2d', { willReadFrequently: true });
        context.drawImage(image, 0, 0);
        const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
        let minX = canvas.width;
        let minY = canvas.height;
        let maxX = -1;
        let maxY = -1;
        let transparent = 0;

        for (let y = 0; y < canvas.height; y += 1) {
          for (let x = 0; x < canvas.width; x += 1) {
            const alpha = pixels[((y * canvas.width + x) * 4) + 3];
            if (alpha === 0) transparent += 1;
            if (alpha > threshold) {
              minX = Math.min(minX, x);
              minY = Math.min(minY, y);
              maxX = Math.max(maxX, x);
              maxY = Math.max(maxY, y);
            }
          }
        }

        const cornerOffsets = [
          3,
          ((canvas.width - 1) * 4) + 3,
          (((canvas.height - 1) * canvas.width) * 4) + 3,
          ((((canvas.height - 1) * canvas.width) + canvas.width - 1) * 4) + 3
        ];
        const cornersTransparent = cornerOffsets.every((offset) => pixels[offset] === 0);
        const margins = [minX, minY, canvas.width - 1 - maxX, canvas.height - 1 - maxY];
        const trimPass = maxX >= 0 && margins.every((margin) => margin === expectedBorder);
        const alphaPass = transparent > 0 && cornersTransparent;
        const pass = alphaPass && trimPass;
        const result = card.querySelector('.mascot-test-result');

        card.classList.add(pass ? 'pass' : 'fail');
        result.innerHTML = `<strong>${pass ? 'PASS' : 'FAIL'}</strong> ` +
          `${canvas.width}×${canvas.height}px · RGBA transparency: ${alphaPass ? 'pass' : 'fail'} · ` +
          `content margins L/T/R/B: ${margins.join('/')}px (${trimPass ? 'pass' : 'expected 4/4/4/4'})`;
        resolve(pass);
      };
      image.onerror = () => {
        card.classList.add('fail');
        card.querySelector('.mascot-test-result').innerHTML = '<strong>FAIL</strong> Image could not be loaded.';
        resolve(false);
      };
      image.src = card.dataset.src;
    });
  }

  Promise.all(cards.map(inspect)).then((results) => {
    const passed = results.filter(Boolean).length;
    const allPass = passed === results.length;
    summary.classList.add(allPass ? 'pass' : 'fail');
    summary.textContent = allPass
      ? `PASS — all ${passed} mascot PNGs have transparency and the expected 4 px trim border.`
      : `FAIL — ${passed} of ${results.length} mascot PNGs passed. Review the failed cards below.`;
  });
})();
</script>
