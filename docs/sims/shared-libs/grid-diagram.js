// grid-diagram.js — Interactive Grid-Overlay MicroSim
// Loads data.json defining rectangular zones over an infographic image.
// Modes: explore (hover + click details) | quiz (click correct zone) | edit (?edit=true)
//
// data.json schema:
// {
//   "title":   "Poster Title",
//   "image":   "../../chapters/.../image.png",
//   "layout":  "grid",
//   "palette": ["#hex", ...],          // optional accent colors
//   "zones": [
//     { "id": "zone-id", "label": "Label", "color": "#hex",
//       "x1": 5, "y1": 10, "x2": 37, "y2": 90,  // % of image
//       "summary": "One-line summary",
//       "facts": ["fact 1", "fact 2", ...] }
//   ],
//   "quiz": [
//     { "question": "...", "correct_zone": "zone-id", "explanation": "..." }
//   ]
// }

class GridDiagramSim {
  constructor() {
    this.data        = null;
    this.mode        = 'explore';
    this.editMode    = false;
    this.zoneEls     = new Map();   // id → zone <div>
    this.activeId    = null;

    // Quiz state
    this.quizQueue   = [];
    this.quizIndex   = 0;
    this.quizCorrect = 0;
    this.quizLocked  = false;

    // Edit state
    this.editTarget  = null;   // { zoneId, corner: 'tl'|'tr'|'bl'|'br' }
    this.editJSON    = {};
  }

  // ── Boot ──────────────────────────────────────────────────────────────────

  async init() {
    const params = new URLSearchParams(window.location.search);
    this.editMode = params.get('edit') === 'true';

    try {
      const res = await fetch('data.json');
      if (!res.ok) throw new Error('HTTP ' + res.status);
      this.data = await res.json();
      // Comparison infographics already print column titles in the image, so the
      // overlay label chip is hidden by default (it would overlap the real title).
      // Set "showLabels": true in data.json only for images with no built-in titles.
      this.showLabels = this.data.showLabels === true;
    } catch (err) {
      this._fatalError('Could not load data.json: ' + err.message);
      return;
    }

    this._buildImageWrapper();

    // Wait for image to load so dimensions are valid
    await new Promise(resolve => {
      if (this.imgEl.complete && this.imgEl.naturalWidth > 0) resolve();
      else this.imgEl.addEventListener('load', resolve, { once: true });
    });

    this._renderZones();
    this._buildDetailPanel();
    this._buildControls();

    if (this.editMode) {
      this._activateEditMode();
    } else {
      this.setMode('explore');
    }

    // Report height after a short settle so the iframe parent can resize
    requestAnimationFrame(() => {
      this._reportHeight();
      this.resizeObserver = new ResizeObserver(() => this._reportHeight());
      this.resizeObserver.observe(document.body);
    });
  }

  // ── DOM Construction ──────────────────────────────────────────────────────

  _buildImageWrapper() {
    const wrapper = document.getElementById('image-wrapper');
    if (!wrapper) { this._fatalError('Missing #image-wrapper in HTML.'); return; }
    this.wrapper = wrapper;

    this.imgEl = document.createElement('img');
    this.imgEl.src       = this.data.image;
    this.imgEl.alt       = this.data.title || 'Infographic';
    this.imgEl.className = 'grid-image';
    this.imgEl.draggable = false;
    wrapper.appendChild(this.imgEl);

    // Overlay container — same size as image via CSS
    this.overlayEl = document.createElement('div');
    this.overlayEl.id = 'zone-overlay';
    wrapper.appendChild(this.overlayEl);

    this._buildCorrectModal();
  }

  // "Correct!" celebration modal — shown over the image when a quiz answer is
  // right. The student clicks OK to advance, so the positive feedback is explicit
  // and unmissable. Overlaid on the image (where the student just clicked) so it
  // is always in view regardless of how the parent page is scrolled.
  _buildCorrectModal() {
    const modal = document.createElement('div');
    modal.id = 'correct-modal';
    modal.innerHTML =
      '<div class="correct-modal-panel" role="dialog" aria-modal="true" aria-label="Correct answer">' +
        '<div class="correct-star" aria-hidden="true">★</div>' +
        '<div class="correct-heading">Correct!</div>' +
        '<button type="button" class="correct-ok-btn">OK</button>' +
      '</div>';
    this.wrapper.appendChild(modal);
    this.correctModal = modal;
    this.correctOkBtn = modal.querySelector('.correct-ok-btn');
    this.correctOkBtn.addEventListener('click', () => this._advanceQuiz());
  }

  _renderZones() {
    this.overlayEl.innerHTML = '';
    this.zoneEls.clear();

    for (const zone of (this.data.zones || [])) {
      const el = document.createElement('div');
      el.className      = 'grid-zone';
      el.dataset.id     = zone.id;
      el.style.left     = zone.x1 + '%';
      el.style.top      = zone.y1 + '%';
      el.style.width    = (zone.x2 - zone.x1) + '%';
      el.style.height   = (zone.y2 - zone.y1) + '%';
      el.style.setProperty('--zone-color', zone.color || '#1389A6');

      // Optional label chip — only when the image has no built-in column titles
      // (see showLabels in init). Comparison posters leave this off so the chip
      // does not overlap the title already printed in the infographic.
      if (this.showLabels) {
        const chip = document.createElement('span');
        chip.className   = 'zone-chip';
        chip.textContent = zone.label;
        el.appendChild(chip);
      }

      el.addEventListener('pointerenter', () => this._onZoneHover(zone.id));
      el.addEventListener('pointerleave', () => this._onZoneLeave(zone.id));
      el.addEventListener('click',        () => this._onZoneClick(zone.id));

      this.overlayEl.appendChild(el);
      this.zoneEls.set(zone.id, el);
    }
  }

  _buildDetailPanel() {
    this.panelEl = document.getElementById('detail-panel');
    if (!this.panelEl) return;

    this.promptEl = document.getElementById('panel-prompt');
    // Keep the explore instruction written in main.html ({PROMPT_TEXT} in the
    // template) instead of replacing it with a generic one in setMode().
    this.explorePrompt = (this.promptEl && this.promptEl.textContent.trim()) ||
      'Click on any column to learn about it.';
    this.contentEl = document.getElementById('panel-content');
    this.panelLabelEl = document.getElementById('panel-label');
    this.panelSummaryEl = document.getElementById('panel-summary');
    this.panelFactsEl = document.getElementById('panel-facts');
    this.quizQuestionEl = document.getElementById('quiz-question');
  }

  _buildControls() {
    this.btnExplore = document.getElementById('btn-explore');
    this.btnQuiz    = document.getElementById('btn-quiz');
    this.scoreEl    = document.getElementById('quiz-score');
    this.scoreVal   = document.getElementById('score-val');
    this.scoreTotal = document.getElementById('score-total');

    if (this.btnExplore) this.btnExplore.addEventListener('click', () => this.setMode('explore'));
    if (this.btnQuiz)    this.btnQuiz.addEventListener('click',    () => this.setMode('quiz'));
  }

  // ── Mode switching ─────────────────────────────────────────────────────────

  setMode(mode) {
    this.mode = mode;

    // Update button states
    if (this.btnExplore) this.btnExplore.classList.toggle('active', mode === 'explore');
    if (this.btnQuiz)    this.btnQuiz.classList.toggle('active',    mode === 'quiz');

    // Reset zone appearances
    for (const el of this.zoneEls.values()) {
      el.classList.remove('zone-correct', 'zone-incorrect', 'zone-dimmed', 'zone-revealed');
    }

    if (mode === 'explore') {
      this._showPrompt(this.explorePrompt);
      if (this.scoreEl) this.scoreEl.style.display = 'none';
    } else if (mode === 'quiz') {
      this._startQuiz();
    }
  }

  // ── Explore mode ───────────────────────────────────────────────────────────

  _onZoneHover(id) {
    if (this.mode !== 'explore') return;
    const el = this.zoneEls.get(id);
    if (el) el.classList.add('zone-hover');
  }

  _onZoneLeave(id) {
    const el = this.zoneEls.get(id);
    if (el) el.classList.remove('zone-hover');
  }

  _onZoneClick(id) {
    if (this.mode === 'explore') {
      this._showZoneDetail(id);
    } else if (this.mode === 'quiz') {
      this._checkQuizAnswer(id);
    } else if (this.editMode) {
      // In edit mode, clicks handled by corner handles
    }
  }

  _showZoneDetail(id) {
    const zone = this.data.zones.find(z => z.id === id);
    if (!zone) return;

    this.activeId = id;

    // Highlight active zone
    for (const [zid, el] of this.zoneEls) {
      el.classList.toggle('zone-active', zid === id);
    }

    if (!this.panelEl) return;
    if (this.promptEl)  this.promptEl.style.display  = 'none';
    if (this.contentEl) this.contentEl.style.display = 'block';

    if (this.panelLabelEl)   this.panelLabelEl.textContent   = zone.label;
    if (this.panelSummaryEl) this.panelSummaryEl.textContent = zone.summary || '';

    if (this.panelFactsEl) {
      this.panelFactsEl.innerHTML = '';
      for (const fact of (zone.facts || [])) {
        const li = document.createElement('li');
        li.textContent = fact;
        this.panelFactsEl.appendChild(li);
      }
    }

    if (this.quizQuestionEl) this.quizQuestionEl.style.display = 'none';

    this._reportHeight();
  }

  _showPrompt(text) {
    if (this.promptEl)  { this.promptEl.textContent = text; this.promptEl.style.display = 'block'; }
    if (this.contentEl)   this.contentEl.style.display = 'none';
    if (this.quizQuestionEl) this.quizQuestionEl.style.display = 'none';

    // Clear active highlights
    for (const el of this.zoneEls.values()) {
      el.classList.remove('zone-active');
    }
    this.activeId = null;
  }

  // ── Quiz mode ─────────────────────────────────────────────────────────────

  _startQuiz() {
    const questions = this.data.quiz || [];
    if (questions.length === 0) {
      this._showPrompt('No quiz questions defined for this infographic.');
      return;
    }

    // Shuffle questions
    this.quizQueue   = [...questions].sort(() => Math.random() - 0.5);
    this.quizIndex   = 0;
    this.quizCorrect = 0;
    this.quizLocked  = false;

    // Dim all zones — correct ones revealed as answered
    for (const el of this.zoneEls.values()) {
      el.classList.add('zone-dimmed');
      el.classList.remove('zone-correct', 'zone-incorrect', 'zone-revealed');
    }

    if (this.scoreEl) {
      this.scoreEl.style.display = 'inline';
      if (this.scoreVal)   this.scoreVal.textContent   = '0';
      if (this.scoreTotal) this.scoreTotal.textContent = questions.length;
    }

    if (this.promptEl)  this.promptEl.style.display  = 'none';
    if (this.contentEl) this.contentEl.style.display = 'none';

    this._askQuestion();
  }

  _askQuestion() {
    if (this.quizIndex >= this.quizQueue.length) {
      this._quizComplete();
      return;
    }

    const q = this.quizQueue[this.quizIndex];
    if (this.quizQuestionEl) {
      this.quizQuestionEl.style.display = 'block';
      this.quizQuestionEl.innerHTML =
        '<span class="quiz-prompt-label">Question ' + (this.quizIndex + 1) +
        ' of ' + this.quizQueue.length + ':</span> ' +
        this._escHtml(q.question);
    }
    if (this.contentEl) this.contentEl.style.display = 'none';
    this._reportHeight();
  }

  _checkQuizAnswer(clickedId) {
    if (this.quizLocked) return;

    const q  = this.quizQueue[this.quizIndex];
    const el = this.zoneEls.get(clickedId);
    if (!el) return;

    if (clickedId === q.correct_zone) {
      // Correct
      this.quizCorrect++;
      if (this.scoreVal) this.scoreVal.textContent = this.quizCorrect;

      el.classList.remove('zone-dimmed');
      el.classList.add('zone-correct', 'zone-revealed');

      // Lock interaction and show the "Correct!" modal; its OK button
      // (→ _advanceQuiz) moves on to the next question.
      this.quizLocked = true;
      this._showCorrectModal();

    } else {
      // Wrong
      el.classList.add('zone-incorrect');
      el.addEventListener('animationend', () => el.classList.remove('zone-incorrect'), { once: true });

      // Show brief feedback
      if (this.quizQuestionEl) {
        const orig = this.quizQuestionEl.innerHTML;
        const wrongZone = this.data.zones.find(z => z.id === clickedId);
        this.quizQuestionEl.innerHTML = orig +
          '<div class="quiz-wrong-msg">That\'s <strong>' +
          this._escHtml(wrongZone ? wrongZone.label : clickedId) +
          '</strong> — try again.</div>';
        setTimeout(() => { this.quizQuestionEl.innerHTML = orig; }, 1200);
      }
    }
  }

  _showCorrectModal() {
    if (!this.correctModal) { this._advanceQuiz(); return; }
    this.correctModal.classList.add('show');
    // Focus OK so Enter/Space also advances (keyboard-friendly).
    if (this.correctOkBtn) this.correctOkBtn.focus();
  }

  _advanceQuiz() {
    if (this.correctModal) this.correctModal.classList.remove('show');
    this.quizLocked = false;
    this.quizIndex++;
    this._askQuestion();
  }

  _quizComplete() {
    const total = this.quizQueue.length;
    const pct   = Math.round((this.quizCorrect / total) * 100);

    // Reveal all zones
    for (const el of this.zoneEls.values()) {
      el.classList.remove('zone-dimmed');
      el.classList.add('zone-revealed');
    }

    if (this.quizQuestionEl) {
      this.quizQuestionEl.innerHTML =
        '<div class="quiz-complete">' +
        '<strong>Quiz complete!</strong> You correctly identified ' +
        this.quizCorrect + ' of ' + total + ' (' + pct + '%).' +
        '<br><button class="mode-btn" onclick="sim.setMode(\'quiz\')" style="margin-top:8px">Try Again</button>' +
        '</div>';
      this.quizQuestionEl.style.display = 'block';
    }

    this._confetti();
    this._reportHeight();
  }

  // ── Edit mode ─────────────────────────────────────────────────────────────

  _activateEditMode() {
    const badge = document.getElementById('edit-badge');
    if (badge) badge.style.display = 'inline-block';

    const editPanel = document.getElementById('edit-panel');
    if (editPanel) editPanel.style.display = 'block';

    this.coordDisplay = document.getElementById('coord-display');
    this.jsonOutput   = document.getElementById('json-output');
    this._syncEditJSON();

    // Add draggable corner handles to each zone
    for (const zone of (this.data.zones || [])) {
      const el = this.zoneEls.get(zone.id);
      if (!el) continue;

      el.classList.add('edit-zone');

      for (const corner of ['tl', 'tr', 'bl', 'br']) {
        const handle = document.createElement('div');
        handle.className   = 'corner-handle corner-' + corner;
        handle.dataset.id  = zone.id;
        handle.dataset.corner = corner;
        handle.setAttribute('aria-label', corner + ' corner of ' + zone.label);

        handle.addEventListener('pointerdown', (e) => {
          e.stopPropagation();
          this._startCornerDrag(e, zone.id, corner);
        });

        el.appendChild(handle);
      }
    }
  }

  _startCornerDrag(e, zoneId, corner) {
    e.preventDefault();
    const zone = this.data.zones.find(z => z.id === zoneId);
    if (!zone) return;

    const rect     = this.imgEl.getBoundingClientRect();

    const onMove = (ev) => {
      const clientX = ev.touches ? ev.touches[0].clientX : ev.clientX;
      const clientY = ev.touches ? ev.touches[0].clientY : ev.clientY;
      const px = Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width)  * 100));
      const py = Math.max(0, Math.min(100, ((clientY - rect.top)  / rect.height) * 100));

      if (corner === 'tl') { zone.x1 = px; zone.y1 = py; }
      if (corner === 'tr') { zone.x2 = px; zone.y1 = py; }
      if (corner === 'bl') { zone.x1 = px; zone.y2 = py; }
      if (corner === 'br') { zone.x2 = px; zone.y2 = py; }

      // Live-update zone element
      const el = this.zoneEls.get(zoneId);
      if (el) {
        el.style.left   = zone.x1 + '%';
        el.style.top    = zone.y1 + '%';
        el.style.width  = (zone.x2 - zone.x1) + '%';
        el.style.height = (zone.y2 - zone.y1) + '%';
      }

      if (this.coordDisplay) {
        this.coordDisplay.textContent =
          zone.label + ' [' + corner + ']: x=' + px.toFixed(1) + '% y=' + py.toFixed(1) + '%';
      }
      this._syncEditJSON();
    };

    const onUp = () => {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup',   onUp);
    };

    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup',   onUp);
  }

  _syncEditJSON() {
    if (!this.jsonOutput) return;
    const out = {
      title:  this.data.title,
      image:  this.data.image,
      layout: this.data.layout,
      zones:  (this.data.zones || []).map(z => ({
        id:      z.id,
        label:   z.label,
        color:   z.color,
        x1: parseFloat(z.x1.toFixed(1)),
        y1: parseFloat(z.y1.toFixed(1)),
        x2: parseFloat(z.x2.toFixed(1)),
        y2: parseFloat(z.y2.toFixed(1)),
        summary: z.summary,
        facts:   z.facts
      })),
      quiz: this.data.quiz
    };
    this.jsonOutput.value = JSON.stringify(out, null, 2);
  }

  copyJSON() {
    if (!this.jsonOutput) return;
    navigator.clipboard.writeText(this.jsonOutput.value).then(() => {
      const confirm = document.getElementById('copy-confirm');
      if (confirm) { confirm.textContent = 'Copied!'; setTimeout(() => { confirm.textContent = ''; }, 2000); }
    });
  }

  // ── iframe auto-height ────────────────────────────────────────────────────

  _reportHeight() {
    if (window.self === window.top) return;
    const height = document.body.scrollHeight + 30;
    window.parent.postMessage({ type: 'microsim-resize', height }, '*');
  }

  // ── Confetti celebration ──────────────────────────────────────────────────

  _confetti() {
    const colors = (this.data.palette || ['#2D8A4E', '#6A3FB5', '#E07B39', '#1389A6']);
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
    document.body.appendChild(canvas);
    const ctx    = canvas.getContext('2d');
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = Array.from({ length: 80 }, () => ({
      x:    Math.random() * canvas.width,
      y:    canvas.height + 10,
      vx:   (Math.random() - 0.5) * 4,
      vy:   -(Math.random() * 6 + 4),
      r:    Math.random() * 5 + 3,
      color: colors[Math.floor(Math.random() * colors.length)],
      rot:  Math.random() * Math.PI * 2,
      spin: (Math.random() - 0.5) * 0.2
    }));

    let frame = 0;
    const tick = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const p of particles) {
        p.x  += p.vx; p.y += p.vy; p.vy += 0.15; p.rot += p.spin;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.r, -p.r / 2, p.r * 2, p.r);
        ctx.restore();
      }
      frame++;
      if (frame < 100) requestAnimationFrame(tick);
      else canvas.remove();
    };
    requestAnimationFrame(tick);
  }

  // ── Utility ───────────────────────────────────────────────────────────────

  _escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  _fatalError(msg) {
    document.body.innerHTML = '<p style="color:red;padding:20px;font-family:monospace">' +
      'GridDiagram error: ' + msg + '</p>';
  }
}

// Auto-boot
const sim = new GridDiagramSim();
document.addEventListener('DOMContentLoaded', () => sim.init());
