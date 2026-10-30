/* An original SVG taxonomy barrel. Content comes from MkDocs, not a second catalog. */
const SVG_NS = 'http://www.w3.org/2000/svg';
const TAU = Math.PI * 2;
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
const wrapAngle = angle => ((angle + Math.PI) % TAU + TAU) % TAU - Math.PI;
const rows = [
  { id: 'overview', label: 'Explanation', hint: 'An introductory explanation has been written.' },
  { id: 'math', label: 'Mathematics', hint: 'The note contains mathematical notation or equations.' },
  { id: 'example', label: 'Worked example', hint: 'A numerical example or worked round is available.' },
  { id: 'sources', label: 'Sources', hint: 'The note links to research sources.' },
  { id: 'check', label: 'Self-check', hint: 'Questions and answers are included for checking understanding.' }
];
const colors = ['#416eaa', '#8864a4', '#ad7939', '#a66370', '#617e98'];
const groups = [];
let group;
for (const node of document.querySelector('#markdown-source').children) {
  if (node.tagName === 'H2') {
    group = { id: node.id, title: node.textContent, description: '', href: '', color: colors[groups.length % colors.length], concepts: [] };
    groups.push(group);
  } else if (group) {
    const link = node.querySelector('a');
    if (link) group.href = link.getAttribute('href');
    else group.description += node.outerHTML;
  }
}
for (const entry of groups) {
  const container = document.querySelector(`#concept-source [data-dimension="${entry.id}"]`);
  entry.concepts = [...(container?.children || [])].map(link => ({
    title: link.textContent, href: link.getAttribute('href'), summary: link.dataset.summary,
    coverage: JSON.parse(link.dataset.coverage), anchors: JSON.parse(link.dataset.anchors), group: entry
  }));
}
const concepts = groups.flatMap(entry => entry.concepts);
function svg(tag, attrs = {}, text) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attrs)) node.setAttribute(name, value);
  if (text !== undefined) node.textContent = text;
  return node;
}
class TaxonomyBarrel {
  constructor(root, { onGroup, onOpen, expanded = false }) {
    this.root = root;
    this.onGroup = onGroup;
    this.onOpen = onOpen;
    this.expanded = expanded;
    this.selected = 0;
    this.row = 0;
    this.rotation = 0;
    this.target = 0;
    this.frame = 0;
    this.active = !expanded;
    this.drag = null;
    this.total = Math.max(14, concepts.length);
    this.step = TAU / this.total;
    this.currentGroup = groups[0];
    root.className = 'barrel';
    root.innerHTML = `<header class="barrel-toolbar"><div><span class="eyebrow">FACING YOU</span><h2 class="barrel-title"></h2></div><div class="barrel-controls"><button class="turn-previous" aria-label="Previous concept">←</button><button class="turn-next" aria-label="Next concept">→</button>${expanded ? '' : '<button class="expand-map">Expand cylinder ↗</button>'}</div></header><div class="barrel-grid"><div class="barrel-scroll"></div><aside class="barrel-inspector"><div class="inspector-readout" aria-live="polite"></div><label>Concept<select class="concept-picker"></select></label><label>Reading section<select class="section-picker"></select></label><a class="read-note" href="#"></a><a class="all-notes" href="#">Explore all in this dimension ↗</a><div class="barrel-legend"><strong>Reading the map</strong><span><i class="written-swatch"></i> Written note section</span><span><i class="planned-swatch"></i> Planned section</span><p>Content coverage, not method ratings or proof of understanding.</p></div></aside></div><p class="barrel-hint">Drag to rotate · ← → concept · ↑ ↓ section · Enter to inspect</p>`;
    this.scroll = root.querySelector('.barrel-scroll');
    this.diagram = svg('svg', { class: 'barrel-diagram', tabindex: '0', role: 'group', 'aria-label': 'Rotating FL concept cylinder. Left and right choose a concept, up and down choose a reading section, Enter inspects. Dropdown controls are also available.' });
    this.scroll.append(this.diagram);
    this.outlineBack = svg('g', { class: 'barrel-outline-back', 'aria-hidden': 'true' });
    this.diagram.append(this.outlineBack);
    this.cells = [];
    this.headers = [];
    this.labels = [];
    for (const [index, concept] of concepts.entries()) {
      const column = svg('g');
      const cap = svg('path', { fill: concept.group.color, class: 'barrel-cap' });
      this.headers.push(cap);column.append(cap);
      const cells = rows.map((row, r) => {
        const path = svg('path', { class: `barrel-cell ${concept.coverage[row.id] ? 'has-note' : 'is-planned'}`, 'data-concept': index, 'data-row': r, role: 'button', 'aria-label': `${concept.title}: ${row.label}, ${concept.coverage[row.id] ? 'written' : 'planned'}` });
        path.append(svg('title', {}, `${concept.title} · ${row.label} · ${concept.coverage[row.id] ? 'Written' : 'Planned'}`));
        column.append(path);return path;
      });
      this.cells.push(cells);
      const text = svg('text', { class: 'barrel-column-label', 'text-anchor': 'start', 'aria-hidden': 'true' });
      const label = concept.title.length > 21 ? concept.title.slice(0, 19) + '…' : concept.title;
      text.append(document.createTextNode(label), svg('title', {}, concept.title));
      this.labels.push(text);column.append(text);
      this.diagram.append(column);
    }
    this.rowLabels = rows.map((row, index) => {
      const label = svg('g', { class: 'barrel-row-label' });
      label.append(svg('line'), svg('text', { 'data-label': index }, row.label));
      this.diagram.append(label);return label;
    });
    this.outlineFront = svg('g', { class: 'barrel-outline-front', 'aria-hidden': 'true' });
    this.diagram.append(this.outlineFront);
    const picker = root.querySelector('.concept-picker');
    for (const dimension of groups) {
      const optgroup = document.createElement('optgroup');optgroup.label = dimension.title;
      dimension.concepts.forEach(concept => optgroup.append(new Option(concept.title, concepts.indexOf(concept))));
      picker.append(optgroup);
    }
    root.querySelector('.section-picker').replaceChildren(...rows.map((row, i) => new Option(row.label, i)));
    picker.addEventListener('change', event => this.choose(Number(event.target.value), this.row, true));
    root.querySelector('.section-picker').addEventListener('change', event => this.choose(this.selected, Number(event.target.value), false));
    root.querySelector('.turn-previous').addEventListener('click', () => this.move(-1));
    root.querySelector('.turn-next').addEventListener('click', () => this.move(1));
    root.querySelector('.expand-map')?.addEventListener('click', () => this.onOpen(this.selected, this.row));
    this.diagram.addEventListener('keydown', event => {
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Enter'].includes(event.key)) event.preventDefault();
      if (event.key === 'ArrowLeft') this.move(-1);
      if (event.key === 'ArrowRight') this.move(1);
      if (event.key === 'ArrowUp') this.choose(this.selected, (this.row + rows.length - 1) % rows.length, false);
      if (event.key === 'ArrowDown') this.choose(this.selected, (this.row + 1) % rows.length, false);
      if (event.key === 'Enter' && concepts.length) this.onOpen(this.selected, this.row);
    });
    this.diagram.addEventListener('pointerdown', event => {
      if (event.button !== 0 || !this.active) return;
      this.stop();
      const cell = event.target.closest('[data-concept]');
      this.drag = { id: event.pointerId, x: event.clientX, y: event.clientY, rotation: this.rotation, moved: false, cell };
      this.diagram.setPointerCapture(event.pointerId);
      this.diagram.focus({ preventScroll: true });
    });
    this.diagram.addEventListener('pointermove', event => {
      if (!this.drag || this.drag.id !== event.pointerId) return;
      const dx = event.clientX - this.drag.x;
      if (Math.hypot(dx, event.clientY - this.drag.y) > 7) this.drag.moved = true;
      if (this.drag.moved) {
        this.rotation = this.drag.rotation + dx / Math.max(100, this.geometry.radius);
        this.target = this.rotation;
        this.render();
      }
    });
    this.diagram.addEventListener('pointerup', event => {
      if (!this.drag || this.drag.id !== event.pointerId) return;
      const drag = this.drag;this.drag = null;
      if (this.diagram.hasPointerCapture(event.pointerId)) this.diagram.releasePointerCapture(event.pointerId);
      if (drag.moved) {
        const nearest = Math.round(-this.rotation / this.step);
        let index = ((nearest % this.total) + this.total) % this.total;
        if (index >= concepts.length) index = concepts.length - 1;
        if (index >= 0) this.choose(index, this.row, true);
      } else if (drag.cell) {
        const index = Number(drag.cell.dataset.concept), row = Number(drag.cell.dataset.row);
        this.choose(index, row, false);
        this.onOpen(index, row);
      }
    });
    const cancelDrag = () => { this.drag = null; };
    this.diagram.addEventListener('pointercancel', cancelDrag);
    this.diagram.addEventListener('lostpointercapture', cancelDrag);
    this.observer = new ResizeObserver(() => this.layout());
    this.observer.observe(this.scroll);
    motionPreference.addEventListener('change', () => { if (motionPreference.matches) { this.stop();this.rotation = this.target;this.render(); } });
    this.layout();
    if (concepts.length) this.choose(0, 0, false);
  }
  layout() {
    const width = Math.max(700, this.scroll.clientWidth || 900);
    const left = width < 850 ? 142 : 175;
    this.geometry = { width, left, cx: (width + left - 24) / 2, radius: (width - left - 24) / 2, top: 163, rowHeight: 50, tilt: 15 };
    this.diagram.setAttribute('viewBox', `0 0 ${width} 510`);
    const { cx, radius, top, rowHeight, tilt } = this.geometry;
    const bottom = top + rowHeight * rows.length;
    this.outlineBack.replaceChildren();this.outlineFront.replaceChildren();
    [top, bottom].forEach(y => this.outlineBack.append(svg('ellipse', { cx, cy: y, rx: radius, ry: tilt })));
    this.outlineFront.append(svg('line', { x1: left, x2: left, y1: top, y2: bottom }), svg('line', { x1: cx + radius, x2: cx + radius, y1: top, y2: bottom }));
    this.outlineBack.append(svg('line', { x1: cx, x2: cx, y1: top - 40, y2: bottom + 35, class: 'barrel-meridian' }));
    this.rowLabels.forEach((label, i) => {
      const y = top + (i + .5) * rowHeight + tilt;
      const line = label.querySelector('line');
      Object.entries({ x1: 14, x2: left - 12, y1: top + (i + 1) * rowHeight + tilt, y2: top + (i + 1) * rowHeight + tilt }).forEach(([k, v]) => line.setAttribute(k, v));
      const text = label.querySelector('text');text.setAttribute('x', '14');text.setAttribute('y', y);
    });
    this.render();
  }
  point(angle, y) {
    const g = this.geometry;
    return [g.cx + g.radius * Math.sin(angle), y + g.tilt * Math.cos(angle)];
  }
  patch(angle, y, height) {
    const half = this.step / 2;
    const points = [];
    for (let i = 0; i <= 6; i++) points.push(this.point(angle - half + this.step * i / 6, y));
    for (let i = 6; i >= 0; i--) points.push(this.point(angle - half + this.step * i / 6, y + height));
    return points.map(([x, yy], i) => `${i ? 'L' : 'M'}${x.toFixed(2)},${yy.toFixed(2)}`).join(' ') + ' Z';
  }
  render() {
    if (!this.geometry) return;
    concepts.forEach((concept, i) => {
      const angle = wrapAngle(this.rotation + i * this.step);
      const visible = Math.abs(angle) < Math.PI / 2 - this.step / 2 + .001;
      const opacity = Math.max(.27, Math.min(1, Math.cos(angle) * 1.3));
      this.headers[i].setAttribute('d', this.patch(angle, this.geometry.top - 22, 6));
      this.headers[i].style.opacity = visible ? opacity : 0;
      this.cells[i].forEach((cell, row) => {
        cell.style.display = visible ? '' : 'none';
        if (!visible) return;
        cell.setAttribute('d', this.patch(angle, this.geometry.top + row * this.geometry.rowHeight, this.geometry.rowHeight));
        cell.style.opacity = opacity;
        cell.classList.toggle('is-selected', i === this.selected && row === this.row);
        cell.classList.toggle('is-column', i === this.selected);
      });
      const label = this.labels[i];
      const [x, y] = this.point(angle, this.geometry.top - 36);
      label.style.display = visible ? '' : 'none';
      label.setAttribute('transform', `translate(${x},${y}) rotate(-46)`);
      label.classList.toggle('is-selected', i === this.selected);
      label.setAttribute('fill', concept.group.color);
    });
    this.rowLabels.forEach((label, i) => label.classList.toggle('is-selected', i === this.row));
  }
  setGroup(dimension) {
    this.currentGroup = dimension;
    if (!dimension.concepts.length) {
      this.root.querySelector('.barrel-title').textContent = dimension.title;
      this.root.querySelector('.inspector-readout').textContent = 'No concept documents yet. Add a Markdown file to this dimension to populate the cylinder.';
      this.onGroup?.(dimension);return;
    }
    const first = concepts.indexOf(dimension.concepts[0]);
    this.choose(first, 0, false);
    const center = first + (dimension.concepts.length - 1) / 2;
    this.target = this.rotation + wrapAngle(-center * this.step - this.rotation);
    this.animate();
  }
  choose(index, row, reveal) {
    if (!concepts[index]) return;
    this.selected = index;this.row = row;this.currentGroup = concepts[index].group;
    if (reveal) this.target = this.rotation + wrapAngle(-index * this.step - this.rotation);
    this.refresh();this.render();
    if (reveal) this.animate();
    this.onGroup?.(this.currentGroup);
  }
  refresh() {
    const concept = concepts[this.selected], dimension = concept.group, row = rows[this.row];
    this.root.querySelector('.barrel-title').textContent = dimension.title;
    const readout = this.root.querySelector('.inspector-readout');
    readout.replaceChildren();
    const eyebrow = document.createElement('span');eyebrow.className = 'eyebrow';eyebrow.textContent = dimension.title;
    const title = document.createElement('h3');title.textContent = concept.title;
    const summary = document.createElement('p');summary.textContent = concept.summary;
    const state = document.createElement('span');state.className = `note-state ${concept.coverage[row.id] ? 'written' : 'planned'}`;state.textContent = `${row.label} · ${concept.coverage[row.id] ? 'Written' : 'Planned'}`;
    const hint = document.createElement('p');hint.className = 'section-hint';hint.textContent = concept.coverage[row.id] ? row.hint : 'This part of the note still needs to be developed.';
    readout.append(eyebrow, title, summary, state, hint);
    this.root.querySelector('.concept-picker').value = this.selected;
    this.root.querySelector('.section-picker').value = this.row;
    const read = this.root.querySelector('.read-note');read.href = this.href();read.textContent = concept.coverage[row.id] ? 'Read this section ↗' : 'Open the planned note ↗';
    this.root.querySelector('.all-notes').href = dimension.href;
  }
  href() {
    const concept = concepts[this.selected], row = rows[this.row];
    const anchor = concept.coverage[row.id] && concept.anchors[row.id];
    return concept.href + (anchor ? '#' + anchor : '');
  }
  move(direction) { if (concepts.length) this.choose((this.selected + direction + concepts.length) % concepts.length, this.row, true); }
  setActive(active) { this.active = active;if (!active) this.stop();else this.animate(); }
  stop() { cancelAnimationFrame(this.frame);this.frame = 0; }
  animate() {
    if (!this.active || this.frame || this.drag) return;
    if (motionPreference.matches || Math.abs(this.target - this.rotation) < .0005) { this.rotation = this.target;this.render();return; }
    this.frame = requestAnimationFrame(() => { this.frame = 0;this.rotation += (this.target - this.rotation) * .18;this.render();this.animate(); });
  }
}
const tabs = document.querySelector('#dimension-tabs');
const buttons = groups.map(dimension => {
  const button = document.createElement('button');button.textContent = dimension.title;button.style.setProperty('--group-color', dimension.color);button.addEventListener('click', () => { homeMap.setGroup(dimension);history.replaceState(null, '', '#' + dimension.id); });tabs.append(button);return button;
});
const highlight = dimension => buttons.forEach((button, i) => { button.classList.toggle('active', groups[i] === dimension);button.setAttribute('aria-pressed', String(groups[i] === dimension)); });
const dialog = document.querySelector('#dimension-view');
let focusMap;
const homeMap = new TaxonomyBarrel(document.querySelector('#taxonomy-home'), {
  onGroup: highlight,
  onOpen: (index, row) => {
    dialog.showModal();document.body.classList.add('dimension-open');homeMap.setActive(false);
    if (!focusMap) focusMap = new TaxonomyBarrel(document.querySelector('#taxonomy-focus'), { expanded: true, onGroup: dimension => { document.querySelector('#focus-heading').textContent = dimension.title; }, onOpen: () => location.assign(focusMap.href()) });
    focusMap.setActive(true);focusMap.choose(index, row, true);focusMap.layout();
    document.querySelector('#focus-heading').textContent = concepts[index].group.title;
    if (!motionPreference.matches) focusMap.root.animate([{ opacity: 0, transform: 'scale(.97)' }, { opacity: 1, transform: 'scale(1)' }], { duration: 300, easing: 'ease-out' });
  }
});
document.querySelector('#close-concepts').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => { document.body.classList.remove('dimension-open');focusMap?.setActive(false);homeMap.setActive(true);document.querySelector('#taxonomy-home .expand-map').focus(); });
const initial = groups.find(dimension => '#' + dimension.id === location.hash) || groups[0];
if (initial) homeMap.setGroup(initial);
