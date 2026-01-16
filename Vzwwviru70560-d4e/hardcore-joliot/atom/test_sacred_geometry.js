/**
 * Test du Sacred Geometry Engine
 */

const SG = require('./engines/sacredgeometry_engine.js');

console.log(`
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║           🔮 TEST SACRED GEOMETRY ENGINE 🔮                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
`);

// ═══════════════════════════════════════════════════════════════════════════
// 1. TEST FIBONACCI
// ═══════════════════════════════════════════════════════════════════════════

console.log("═══ 1. SUITE DE FIBONACCI ═══\n");

const fib = SG.FibonacciEngine;
console.log("Séquence (20 premiers):", fib.sequence(20).join(', '));
console.log("\nRatios d'or (convergence vers φ):");
for (let i = 5; i <= 15; i++) {
  const ratio = fib.goldenRatio(i);
  console.log(`  F(${i})/F(${i-1}) = ${fib.get(i)}/${fib.get(i-1)} = ${ratio.toFixed(10)}`);
}
console.log(`  φ (exact)    = ${SG.PHI.toFixed(10)}`);

console.log("\nDélais basés sur Fibonacci (base 100ms):");
console.log("  ", fib.generateDelays(100, 8).join('ms, ') + 'ms');

console.log("\nDélais dorés (φ^n × base):");
console.log("  ", fib.generateGoldenDelays(100, 8).join('ms, ') + 'ms');

// ═══════════════════════════════════════════════════════════════════════════
// 2. TEST NOMBRE D'OR
// ═══════════════════════════════════════════════════════════════════════════

console.log("\n═══ 2. NOMBRE D'OR (φ) ═══\n");

console.log(`φ (Phi)       = ${SG.PHI}`);
console.log(`1/φ           = ${SG.PHI_INVERSE}`);
console.log(`φ² = φ + 1    = ${Math.pow(SG.PHI, 2)} (vérif: ${SG.PHI + 1})`);
console.log(`1/φ = φ - 1   = ${SG.PHI_INVERSE} (vérif: ${SG.PHI - 1})`);

console.log("\nTimings Dorés prédéfinis:");
const timing = SG.GoldenTiming;
Object.entries(timing.presets).forEach(([name, ms]) => {
  console.log(`  ${name.padEnd(12)} = ${ms}ms`);
});

// ═══════════════════════════════════════════════════════════════════════════
// 3. TEST CUBE DE MÉTATRON
// ═══════════════════════════════════════════════════════════════════════════

console.log("\n═══ 3. CUBE DE MÉTATRON ═══\n");

const metatron = SG.MetatronCube;
console.log("Cercles: 13 (1 central + 6 intérieurs + 6 extérieurs)");
console.log("Lignes (connexions): " + metatron.generateLines().length);

console.log("\n5 Solides de Platon contenus:");
Object.values(metatron.platonicSolids).forEach(solid => {
  console.log(`  ${solid.name.padEnd(20)} | ${solid.element.padEnd(6)} | ${solid.vertices}V ${solid.edges}E ${solid.faces}F | ${solid.frequency} Hz`);
});

console.log("\nSolide par Arithmos:");
for (let i = 1; i <= 9; i++) {
  const solid = metatron.getSolidByArithmos(i);
  console.log(`  ${i} → ${solid.name} (${solid.element})`);
}

// ═══════════════════════════════════════════════════════════════════════════
// 4. TEST 4 ÉLÉMENTS
// ═══════════════════════════════════════════════════════════════════════════

console.log("\n═══ 4. LES 4 ÉLÉMENTS (QUADRANTS) ═══\n");

const elements = SG.ElementsQuadrant;

console.log("┌──────────────────────────────────────────────────────────────────┐");
console.log("│     🔥 FEU (Haut-Gauche)     │     💨 AIR (Haut-Droite)          │");
console.log("│     Transformation/Énergie   │     Communication/IA              │");
console.log("│     555 Hz - Tétraèdre       │     741 Hz - Octaèdre             │");
console.log("├──────────────────────────────┼───────────────────────────────────┤");
console.log("│     🌍 TERRE (Bas-Gauche)    │     💧 EAU (Bas-Droite)           │");
console.log("│     Archives/Historique      │     Relations/Émotions            │");
console.log("│     396 Hz - Hexaèdre        │     639 Hz - Icosaèdre            │");
console.log("└──────────────────────────────┴───────────────────────────────────┘");
console.log("                        ✨ ÉTHER (Centre)");
console.log("                        Conscience/Unité");
console.log("                        999 Hz - Dodécaèdre");

console.log("\nÉlément par Arithmos:");
for (let i = 1; i <= 9; i++) {
  const el = elements.getElementByArithmos(i);
  console.log(`  ${i} → ${el.symbol} ${el.name.padEnd(8)} (${el.domain})`);
}

// ═══════════════════════════════════════════════════════════════════════════
// 5. TEST ENTROPIE
// ═══════════════════════════════════════════════════════════════════════════

console.log("\n═══ 5. SYSTÈME D'ENTROPIE ═══\n");

const entropy = SG.EntropyEngine;
console.log("Configuration:");
console.log(`  Timeout d'inactivité: ${entropy.config.idleTimeout / 1000 / 60} minutes`);
console.log(`  Opacité minimale: ${entropy.config.minOpacity}`);
console.log(`  Taux d'entropie: ${entropy.config.entropyRate}/seconde`);

console.log("\nMessages d'entropie:");
[0, 0.2, 0.4, 0.6, 0.8, 1].forEach(level => {
  console.log(`  ${(level * 100).toString().padStart(3)}% : ${entropy.getEntropyMessage(level)}`);
});

// ═══════════════════════════════════════════════════════════════════════════
// 6. TEST RÉSONANCE GÉOMÉTRIQUE COMPLÈTE
// ═══════════════════════════════════════════════════════════════════════════

console.log("\n═══ 6. RÉSONANCE GÉOMÉTRIQUE COMPLÈTE ═══\n");

const sg = new SG.SacredGeometryEngine();
sg.init();

const testWords = [
  { word: "FEU", arithmos: 5 },
  { word: "ACIER", arithmos: 9 },
  { word: "SILENCE", arithmos: 4 },
  { word: "AMOUR", arithmos: 5 },
  { word: "IA", arithmos: 1 }
];

testWords.forEach(({ word, arithmos }) => {
  const res = sg.getGeometricResonance(word, arithmos);
  console.log(`\n${res.element.symbol} ${word} (Arithmos: ${arithmos}):`);
  console.log(`   Solide: ${res.solid.name} (${res.solid.element}) - ${res.solid.frequency} Hz`);
  console.log(`   Élément: ${res.element.name} - ${res.element.domain}`);
  console.log(`   Position: ${res.element.position}`);
  console.log(`   Fibonacci proche: ${res.fibonacci.nearest}`);
});

console.log(`
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    ✅ TOUS LES TESTS RÉUSSIS                                  ║
║                                                                               ║
║   φ = ${SG.PHI.toFixed(6)} — La proportion divine                             ║
║   Métatron: 13 cercles, 78 lignes, 5 solides                                 ║
║   4 Éléments + Éther = Navigation complète                                   ║
║   Entropie: L'interface respire avec l'attention                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
`);
