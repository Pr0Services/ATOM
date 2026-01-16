/* AT-OM / CHE-NU — Glyph Generator (prototype)

Goal
----
Procedurally generate an SVG "glyph" for a concept using:
- Arithmos reduced number (1-9 / 11 / 22 / 33)
- Resonance color (chromotherapy)

This is intentionally lightweight so Agent B can swap with Three.js later.
*/

// Pythagorean mapping per spec
const MAP = {
  A:1,J:1,S:1,
  B:2,K:2,T:2,
  C:3,L:3,U:3,
  D:4,M:4,V:4,
  E:5,N:5,W:5,
  F:6,O:6,X:6,
  G:7,P:7,Y:7,
  H:8,Q:8,Z:8,
  I:9,R:9
};

const MASTER = new Set([11,22,33]);

const COLOR = {
  1:'#FF0000',
  2:'#FFA500',
  3:'#FFFF00',
  4:'#00FF00',
  5:'#0000FF',
  6:'#4B0082',
  7:'#8A2BE2',
  8:'#B76E79',
  9:'#FFD700',
  11:'#FFFFFF',
  22:'#FFFFFF',
  33:'#FFFFFF'
};

function normalize(text){
  return (text||"").toUpperCase().replace(/[^A-Z]/g,'');
}

function rawGematria(text){
  const n = normalize(text);
  let sum = 0;
  for (const ch of n) sum += (MAP[ch] || 0);
  return sum;
}

function reduce(value){
  let r = value;
  while(true){
    if(r === 0) return 0;
    if(MASTER.has(r)) return r;
    if(r >= 1 && r <= 9) return r;
    r = String(r).split('').reduce((a,d)=>a+Number(d),0);
  }
}

export function analyzeConcept(text){
  const raw = rawGematria(text);
  const reduced = reduce(raw);
  const color = COLOR[reduced] || '#FFFFFF';
  const heartbeat = 444.0;
  // Keep frequency simple and explainable
  const mult = {
    1:1.000, 2:1.125, 3:1.250, 4:1.000, 5:1.333, 6:1.500, 7:1.575, 8:1.666, 9:1.777, 11:2.0, 22:3.0, 33:4.0
  }[reduced] || 1.0;
  const hz = heartbeat * mult;
  return { text, normalized: normalize(text), raw, reduced, color, hz };
}

function polar(cx, cy, r, angleDeg){
  const a = (angleDeg - 90) * Math.PI/180;
  return { x: cx + r*Math.cos(a), y: cy + r*Math.sin(a) };
}

export function renderGlyph(svgEl, analysis){
  const size = 280;
  const cx = size/2;
  const cy = size/2;

  svgEl.setAttribute('viewBox', `0 0 ${size} ${size}`);
  svgEl.innerHTML = '';

  // Outer circle (OM)
  const outer = document.createElementNS('http://www.w3.org/2000/svg','circle');
  outer.setAttribute('cx', cx);
  outer.setAttribute('cy', cy);
  outer.setAttribute('r', 120);
  outer.setAttribute('fill', 'none');
  outer.setAttribute('stroke', analysis.color);
  outer.setAttribute('stroke-width', '6');
  svgEl.appendChild(outer);

  // Center point (AT)
  const dot = document.createElementNS('http://www.w3.org/2000/svg','circle');
  dot.setAttribute('cx', cx);
  dot.setAttribute('cy', cy);
  dot.setAttribute('r', 6);
  dot.setAttribute('fill', analysis.color);
  svgEl.appendChild(dot);

  // Geometry shape based on reduced
  const reduced = analysis.reduced;
  const sides = (reduced === 4) ? 4 : (reduced === 7 ? 7 : (reduced === 3 ? 3 : (reduced === 6 ? 6 : (reduced === 8 ? 8 : 5))));
  const poly = document.createElementNS('http://www.w3.org/2000/svg','polygon');
  const pts = [];
  for(let i=0;i<sides;i++){
    const p = polar(cx,cy,70,(360/sides)*i);
    pts.push(`${p.x.toFixed(2)},${p.y.toFixed(2)}`);
  }
  poly.setAttribute('points', pts.join(' '));
  poly.setAttribute('fill', 'none');
  poly.setAttribute('stroke', analysis.color);
  poly.setAttribute('stroke-width', '2');
  poly.setAttribute('opacity', '0.85');
  svgEl.appendChild(poly);

  // Causal lines: number of spokes = reduced (cap at 12 for readability)
  const spokes = Math.min(12, (MASTER.has(reduced) ? 11 : reduced));
  for(let i=0;i<spokes;i++){
    const p = polar(cx,cy,120,(360/spokes)*i);
    const line = document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('x1', cx);
    line.setAttribute('y1', cy);
    line.setAttribute('x2', p.x);
    line.setAttribute('y2', p.y);
    line.setAttribute('stroke', analysis.color);
    line.setAttribute('stroke-width', '1.5');
    line.setAttribute('opacity', '0.55');
    svgEl.appendChild(line);
  }

  // Title text
  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x', cx);
  t.setAttribute('y', 262);
  t.setAttribute('text-anchor', 'middle');
  t.setAttribute('font-family', 'ui-sans-serif, system-ui, -apple-system, Segoe UI');
  t.setAttribute('font-size', '14');
  t.setAttribute('fill', '#111');
  t.textContent = `${analysis.text}  |  raw ${analysis.raw} → reduced ${analysis.reduced}  |  ${analysis.hz.toFixed(1)} Hz`;
  svgEl.appendChild(t);
}

export function initGlyphDemo(){
  const input = document.getElementById('conceptInput');
  const svg = document.getElementById('glyph');
  const meta = document.getElementById('meta');

  function refresh(){
    const a = analyzeConcept(input.value);
    renderGlyph(svg, a);
    meta.textContent = JSON.stringify(a, null, 2);
  }

  input.addEventListener('input', refresh);
  refresh();
}
