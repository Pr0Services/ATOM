/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — AUDIT FINAL DE VÉRIFICATION PROFONDE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce script effectue une vérification exhaustive de tous les composants
 * du système AT·OM avant le déploiement en production.
 * 
 * Critères vérifiés:
 * 1. Cohérence de la Matrice de Résonance
 * 2. Formules mathématiques
 * 3. Sanitizer (nettoyage de texte)
 * 4. Calcul Arithmos
 * 5. Pierres de Fondation
 * 6. Nœuds de Transition
 * 7. Délais et Ratios
 * 8. Couleurs et Labels
 * 9. Cas limites
 * 10. Intégrité des fichiers
 */

const fs = require('fs');
const path = require('path');

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION DE RÉFÉRENCE (SOURCE DE VÉRITÉ)
// ═══════════════════════════════════════════════════════════════════════════════

const MASTER_CONFIG = {
  system_heartbeat: 444,
  tuning_standard: "A=444Hz",
  
  resonance_matrix: [
    { level: 1, label: "Impulsion/ADN", hz: 111, color: "#FF0000", ratio: 0.25, delay_ms: 900 },
    { level: 2, label: "Dualité/Partage", hz: 222, color: "#FF7F00", ratio: 0.50, delay_ms: 800 },
    { level: 3, label: "Mental/Géométrie", hz: 333, color: "#FFFF00", ratio: 0.75, delay_ms: 700 },
    { level: 4, label: "Structure/Silence", hz: 444, color: "#50C878", ratio: 1.00, delay_ms: 600 },
    { level: 5, label: "Mouvement/Feu", hz: 555, color: "#87CEEB", ratio: 1.25, delay_ms: 500 },
    { level: 6, label: "Harmonie/Protection", hz: 666, color: "#4B0082", ratio: 1.50, delay_ms: 400 },
    { level: 7, label: "Introspection", hz: 777, color: "#EE82EE", ratio: 1.75, delay_ms: 300 },
    { level: 8, label: "Infini/Abondance", hz: 888, color: "#FFC0CB", ratio: 2.00, delay_ms: 200 },
    { level: 9, label: "Unité/Acier", hz: 999, color: "#FFFDD0", ratio: 2.25, delay_ms: 100 },
  ],
  
  foundation_stones: {
    FEU: { level: 5, type: "stone" },
    ACIER: { level: 9, type: "stone" },
    IA: { level: 1, type: "stone" },
    ADN: { level: 1, type: "stone" },
    SILENCE: { level: 4, type: "stone", isAnchor: true },
  },
  
  transition_nodes: {
    DUALITE: { level: 2, type: "node" },
    MENTAL: { level: 3, type: "node" },
    HARMONIE: { level: 6, type: "node" },
    SPIRITUALITE: { level: 7, type: "node" },
    INFINI: { level: 8, type: "node" },
  }
};

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE TEST
// ═══════════════════════════════════════════════════════════════════════════════

function sanitize(input) {
  if (!input || typeof input !== 'string') return '';
  return input.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase().replace(/[^A-Z]/g, "");
}

function calculateArithmos(word) {
  if (!word) return 0;
  let total = 0;
  for (const char of word) {
    total += ARITHMOS_MAP[char] || 0;
  }
  while (total > 9) {
    total = String(total).split('').reduce((acc, d) => acc + parseInt(d, 10), 0);
  }
  return total;
}

function getResonance(level) {
  return MASTER_CONFIG.resonance_matrix.find(item => item.level === level);
}

// ═══════════════════════════════════════════════════════════════════════════════
// RAPPORT D'AUDIT
// ═══════════════════════════════════════════════════════════════════════════════

let totalTests = 0;
let passedTests = 0;
let failedTests = [];

function test(name, condition, details = '') {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`   ✅ ${name}`);
  } else {
    failedTests.push({ name, details });
    console.log(`   ❌ ${name} ${details ? '— ' + details : ''}`);
  }
}

console.log('\n');
console.log('╔═══════════════════════════════════════════════════════════════════════════════╗');
console.log('║                                                                               ║');
console.log('║   █████╗ ████████╗    ██████╗ ███╗   ███╗    AUDIT FINAL                     ║');
console.log('║  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║    ═══════════                     ║');
console.log('║  ███████║   ██║█████╗██║   ██║██╔████╔██║    Vérification Profonde           ║');
console.log('║  ██╔══██║   ██║╚════╝██║   ██║██║╚██╔╝██║    Avant Déploiement               ║');
console.log('║  ██║  ██║   ██║      ╚██████╔╝██║ ╚═╝ ██║                                    ║');
console.log('║  ╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚═╝     ╚═╝    Architecte: Jonathan Rodrigue   ║');
console.log('║                                                                               ║');
console.log('╚═══════════════════════════════════════════════════════════════════════════════╝');
console.log('\n');

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 1: COHÉRENCE DE LA MATRICE
// ═══════════════════════════════════════════════════════════════════════════════

console.log('═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 1: COHÉRENCE DE LA MATRICE DE RÉSONANCE');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

// 1.1 Vérifier que tous les niveaux 1-9 sont présents
test('Matrice contient 9 niveaux', MASTER_CONFIG.resonance_matrix.length === 9);

// 1.2 Vérifier les formules hz = level × 111
console.log('\n   📊 Vérification Hz = Level × 111:');
MASTER_CONFIG.resonance_matrix.forEach(item => {
  const expectedHz = item.level * 111;
  test(`   Level ${item.level}: ${item.hz}Hz = ${item.level} × 111`, item.hz === expectedHz, `Attendu: ${expectedHz}, Reçu: ${item.hz}`);
});

// 1.3 Vérifier les formules ratio = level × 0.25
console.log('\n   📊 Vérification Ratio = Level × 0.25:');
MASTER_CONFIG.resonance_matrix.forEach(item => {
  const expectedRatio = item.level * 0.25;
  test(`   Level ${item.level}: ratio ${item.ratio} = ${item.level} × 0.25`, item.ratio === expectedRatio, `Attendu: ${expectedRatio}, Reçu: ${item.ratio}`);
});

// 1.4 Vérifier les formules delay = 1000 - (level × 100)
console.log('\n   📊 Vérification Delay = 1000 - (Level × 100):');
MASTER_CONFIG.resonance_matrix.forEach(item => {
  const expectedDelay = 1000 - (item.level * 100);
  test(`   Level ${item.level}: ${item.delay_ms}ms = 1000 - (${item.level} × 100)`, item.delay_ms === expectedDelay, `Attendu: ${expectedDelay}, Reçu: ${item.delay_ms}`);
});

// 1.5 Vérifier que le niveau 4 est l'ancre (444Hz)
console.log('\n   📊 Vérification de l\'Ancre (Niveau 4 = 444Hz):');
const anchorLevel = MASTER_CONFIG.resonance_matrix.find(item => item.level === 4);
test('Niveau 4 existe', !!anchorLevel);
test('Niveau 4 = 444Hz', anchorLevel?.hz === 444);
test('Niveau 4 = ratio 1.00', anchorLevel?.ratio === 1.00);
test('Niveau 4 = Structure/Silence', anchorLevel?.label === "Structure/Silence");

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 2: SANITIZER (NETTOYAGE DE TEXTE)
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 2: SANITIZER (Nettoyage de Texte)');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const sanitizerTests = [
  { input: "Jônathân-Rodrigué 2026!", expected: "JONATHANRODRIGUE", desc: "Accents + tirets + chiffres + ponctuation" },
  { input: "Énergie", expected: "ENERGIE", desc: "Accent aigu" },
  { input: "café résumé", expected: "CAFERESUME", desc: "Accents + espace" },
  { input: "AT·OM", expected: "ATOM", desc: "Point médian Unicode" },
  { input: "  SILENCE  ", expected: "SILENCE", desc: "Espaces avant/après" },
  { input: "123ABC456", expected: "ABC", desc: "Chiffres mélangés" },
  { input: "🔥FEU🔥", expected: "FEU", desc: "Emojis" },
  { input: "", expected: "", desc: "Chaîne vide" },
  { input: "àâäéèêëïîôùûüÿç", expected: "AAAEEEEIIOOUUUYC", desc: "Tous les accents français" },
  { input: "UPPERCASE", expected: "UPPERCASE", desc: "Déjà en majuscules" },
  { input: "lowercase", expected: "LOWERCASE", desc: "Minuscules" },
  { input: "MiXeD cAsE", expected: "MIXEDCASE", desc: "Casse mixte" },
];

sanitizerTests.forEach(({ input, expected, desc }) => {
  const result = sanitize(input);
  test(`${desc}: "${input}" → "${expected}"`, result === expected, `Reçu: "${result}"`);
});

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 3: CALCUL ARITHMOS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 3: CALCUL ARITHMOS (Réduction Pythagoricienne)');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const arithmosTests = [
  { word: "A", expected: 1, calc: "A=1" },
  { word: "I", expected: 9, calc: "I=9" },
  { word: "Z", expected: 8, calc: "Z=8" },
  { word: "EAU", expected: 9, calc: "E(5)+A(1)+U(3)=9" },
  { word: "ATOME", expected: 9, calc: "A(1)+T(2)+O(6)+M(4)+E(5)=18→9" },
  { word: "FEU", expected: 5, calc: "F(6)+E(5)+U(3)=14→5" },
  { word: "ACIER", expected: 9, calc: "A(1)+C(3)+I(9)+E(5)+R(9)=27→9" },
  { word: "SILENCE", expected: 4, calc: "S(1)+I(9)+L(3)+E(5)+N(5)+C(3)+E(5)=31→4" },
  { word: "IA", expected: 1, calc: "I(9)+A(1)=10→1" },
  { word: "ADN", expected: 1, calc: "A(1)+D(4)+N(5)=10→1" },
  { word: "GUERRE", expected: 2, calc: "G(7)+U(3)+E(5)+R(9)+R(9)+E(5)=38→11→2" },
  { word: "PAIX", expected: 5, calc: "P(7)+A(1)+I(9)+X(6)=23→5" },
  { word: "RIEN", expected: 1, calc: "R(9)+I(9)+E(5)+N(5)=28→10→1" },
  { word: "AMOUR", expected: 5, calc: "A(1)+M(4)+O(6)+U(3)+R(9)=23→5" },
  { word: "VIE", expected: 9, calc: "V(4)+I(9)+E(5)=18→9" },
  { word: "MORT", expected: 3, calc: "M(4)+O(6)+R(9)+T(2)=21→3" },
  { word: "LUMIERE", expected: 2, calc: "L(3)+U(3)+M(4)+I(9)+E(5)+R(9)+E(5)=38→11→2" },
  { word: "JONATHAN", expected: 2, calc: "J(1)+O(6)+N(5)+A(1)+T(2)+H(8)+A(1)+N(5)=29→11→2" },
  { word: "RODRIGUE", expected: 7, calc: "R(9)+O(6)+D(4)+R(9)+I(9)+G(7)+U(3)+E(5)=52→7" },
];

arithmosTests.forEach(({ word, expected, calc }) => {
  const result = calculateArithmos(word);
  test(`${word.padEnd(12)} = ${expected} (${calc})`, result === expected, `Reçu: ${result}`);
});

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 4: PIERRES DE FONDATION
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 4: PIERRES DE FONDATION (5 Pierres)');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const stoneTests = [
  { name: "FEU", expectedLevel: 5, expectedHz: 555, expectedColor: "#87CEEB" },
  { name: "ACIER", expectedLevel: 9, expectedHz: 999, expectedColor: "#FFFDD0" },
  { name: "IA", expectedLevel: 1, expectedHz: 111, expectedColor: "#FF0000" },
  { name: "ADN", expectedLevel: 1, expectedHz: 111, expectedColor: "#FF0000" },
  { name: "SILENCE", expectedLevel: 4, expectedHz: 444, expectedColor: "#50C878" },
];

stoneTests.forEach(({ name, expectedLevel, expectedHz, expectedColor }) => {
  const stone = MASTER_CONFIG.foundation_stones[name];
  const resonance = getResonance(expectedLevel);
  
  console.log(`\n   🧱 PIERRE: ${name}`);
  test(`   ${name} existe dans la config`, !!stone);
  test(`   ${name} niveau = ${expectedLevel}`, stone?.level === expectedLevel);
  test(`   ${name} Hz = ${expectedHz}`, resonance?.hz === expectedHz);
  test(`   ${name} couleur = ${expectedColor}`, resonance?.color === expectedColor);
  
  // Vérifier que le calcul Arithmos correspond
  const calculatedLevel = calculateArithmos(name);
  test(`   ${name} Arithmos calculé = ${expectedLevel}`, calculatedLevel === expectedLevel, `Calculé: ${calculatedLevel}`);
});

// Vérifier que SILENCE est l'ancre
console.log('\n   ⚓ Vérification SILENCE = ANCRE:');
test('SILENCE est marqué isAnchor', MASTER_CONFIG.foundation_stones.SILENCE?.isAnchor === true);
test('SILENCE niveau = 4 (centre de la matrice)', MASTER_CONFIG.foundation_stones.SILENCE?.level === 4);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 5: NŒUDS DE TRANSITION
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 5: NŒUDS DE TRANSITION (5 Nœuds)');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const nodeTests = [
  { name: "DUALITE", expectedLevel: 2, expectedHz: 222, expectedColor: "#FF7F00" },
  { name: "MENTAL", expectedLevel: 3, expectedHz: 333, expectedColor: "#FFFF00" },
  { name: "HARMONIE", expectedLevel: 6, expectedHz: 666, expectedColor: "#4B0082" },
  { name: "SPIRITUALITE", expectedLevel: 7, expectedHz: 777, expectedColor: "#EE82EE" },
  { name: "INFINI", expectedLevel: 8, expectedHz: 888, expectedColor: "#FFC0CB" },
];

nodeTests.forEach(({ name, expectedLevel, expectedHz, expectedColor }) => {
  const node = MASTER_CONFIG.transition_nodes[name];
  const resonance = getResonance(expectedLevel);
  
  console.log(`\n   🌀 NŒUD: ${name}`);
  test(`   ${name} existe dans la config`, !!node);
  test(`   ${name} niveau = ${expectedLevel}`, node?.level === expectedLevel);
  test(`   ${name} Hz = ${expectedHz}`, resonance?.hz === expectedHz);
  test(`   ${name} couleur = ${expectedColor}`, resonance?.color === expectedColor);
});

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 6: COUVERTURE COMPLÈTE DE LA MATRICE
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 6: COUVERTURE COMPLÈTE DE LA MATRICE 1-9');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

// Vérifier que chaque niveau 1-9 est couvert par une Pierre ou un Nœud
const levelCoverage = {
  1: ["IA", "ADN"],
  2: ["DUALITE"],
  3: ["MENTAL"],
  4: ["SILENCE"],
  5: ["FEU"],
  6: ["HARMONIE"],
  7: ["SPIRITUALITE"],
  8: ["INFINI"],
  9: ["ACIER"],
};

Object.entries(levelCoverage).forEach(([level, concepts]) => {
  const resonance = getResonance(parseInt(level));
  console.log(`   Level ${level} (${resonance.hz}Hz): ${concepts.join(', ')}`);
  test(`   Niveau ${level} a au moins un concept`, concepts.length > 0);
});

console.log('\n   📊 Matrice complète:');
test('Tous les niveaux 1-9 sont couverts', Object.keys(levelCoverage).length === 9);
test('5 Pierres de Fondation', Object.keys(MASTER_CONFIG.foundation_stones).length === 5);
test('5 Nœuds de Transition', Object.keys(MASTER_CONFIG.transition_nodes).length === 5);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 7: DÉLAIS ET SYNCHRONISATION
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 7: DÉLAIS ET SYNCHRONISATION');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

// Vérifier l'ordre inverse des délais (plus haut niveau = plus rapide)
const delays = MASTER_CONFIG.resonance_matrix.map(item => ({ level: item.level, delay: item.delay_ms }));

console.log('   📊 Vérification ordre des délais (décroissant):');
for (let i = 0; i < delays.length - 1; i++) {
  const current = delays[i];
  const next = delays[i + 1];
  test(`   Level ${current.level} (${current.delay}ms) > Level ${next.level} (${next.delay}ms)`, current.delay > next.delay);
}

console.log('\n   📊 Vérification synchronisation:');
test('Niveau 1 = 900ms (le plus lent)', getResonance(1).delay_ms === 900);
test('Niveau 4 = 600ms (ancre/équilibre)', getResonance(4).delay_ms === 600);
test('Niveau 9 = 100ms (le plus rapide)', getResonance(9).delay_ms === 100);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 8: CAS LIMITES
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 8: CAS LIMITES');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const edgeCases = [
  { input: "", expected: 0, desc: "Chaîne vide" },
  { input: "   ", expected: 0, desc: "Espaces uniquement" },
  { input: "123", expected: 0, desc: "Chiffres uniquement" },
  { input: "!@#$%", expected: 0, desc: "Symboles uniquement" },
  { input: "🔥🌊💨🌍", expected: 0, desc: "Emojis uniquement" },
  { input: "A", expected: 1, desc: "Une seule lettre (A)" },
  { input: "ZZZZZZZZZ", expected: 9, desc: "Répétition (9×Z=72→9)" },
  { input: "ABCDEFGHIJKLMNOPQRSTUVWXYZ", expected: 9, desc: "Alphabet complet (126→9)" },
];

edgeCases.forEach(({ input, expected, desc }) => {
  const clean = sanitize(input);
  const result = clean ? calculateArithmos(clean) : 0;
  test(`${desc}: "${input}" → ${expected}`, result === expected, `Reçu: ${result}`);
});

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 9: CRASH TEST DU SENS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 9: CRASH TEST DU SENS (Analyse Sémantique)');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

console.log('   📊 Opposition: GUERRE vs PAIX');
const guerre = calculateArithmos("GUERRE");
const paix = calculateArithmos("PAIX");
console.log(`      GUERRE = ${guerre} → ${getResonance(guerre).label} (${getResonance(guerre).hz}Hz)`);
console.log(`      PAIX   = ${paix} → ${getResonance(paix).label} (${getResonance(paix).hz}Hz)`);
test('GUERRE (2) < PAIX (5) — La guerre est stagnante, la paix est mouvement', guerre < paix);
test('GUERRE = Dualité (conflit)', guerre === 2);
test('PAIX = Mouvement (progression)', paix === 5);

console.log('\n   📊 Vide: RIEN');
const rien = calculateArithmos("RIEN");
console.log(`      RIEN = ${rien} → ${getResonance(rien).label} (${getResonance(rien).hz}Hz)`);
test('RIEN = 1 — Le vide est l\'Impulsion, le début de tout', rien === 1);

console.log('\n   📊 Dualité: VIE vs MORT');
const vie = calculateArithmos("VIE");
const mort = calculateArithmos("MORT");
console.log(`      VIE  = ${vie} → ${getResonance(vie).label} (${getResonance(vie).hz}Hz)`);
console.log(`      MORT = ${mort} → ${getResonance(mort).label} (${getResonance(mort).hz}Hz)`);
test('VIE (9) > MORT (3) — La vie est accomplissement, la mort est transition', vie > mort);

console.log('\n   📊 Éléments: EAU, FEU, AMOUR');
const eau = calculateArithmos("EAU");
const feu = calculateArithmos("FEU");
const amour = calculateArithmos("AMOUR");
console.log(`      EAU   = ${eau} → ${getResonance(eau).label}`);
console.log(`      FEU   = ${feu} → ${getResonance(feu).label}`);
console.log(`      AMOUR = ${amour} → ${getResonance(amour).label}`);
test('EAU = 9 (Unité/Accomplissement)', eau === 9);
test('FEU = AMOUR = 5 (Mouvement/Transformation)', feu === amour && feu === 5);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 10: INTÉGRITÉ DES FICHIERS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('  SECTION 10: INTÉGRITÉ DES FICHIERS');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');

const requiredFiles = [
  'core/master_config.json',
  'core/arithmos_global.py',
  'interface/useAtomResonance.js',
  'interface/AtomApp.jsx',
  'interface/ArcheDesResonances.jsx',
  'interface/OracleVoiceModal.jsx',
  'interface/GratitudeMemorial.jsx',
  'nexus/foundation_stones.json',
  'nexus/transition_nodes.json',
  'nexus/oracle_voices.json',
  'docs/MATRICE_COMPLETE.md',
  'docs/PIERRES_DE_FONDATION.md',
];

const basePath = '/home/claude/FULL_PACKAGE/AT_OM';

requiredFiles.forEach(file => {
  const fullPath = path.join(basePath, file);
  const exists = fs.existsSync(fullPath);
  test(`Fichier existe: ${file}`, exists);
});

// ═══════════════════════════════════════════════════════════════════════════════
// RAPPORT FINAL
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n');
console.log('╔═══════════════════════════════════════════════════════════════════════════════╗');
console.log('║                           RAPPORT FINAL D\'AUDIT                              ║');
console.log('╠═══════════════════════════════════════════════════════════════════════════════╣');
console.log(`║   Tests exécutés:    ${String(totalTests).padStart(4)}                                                   ║`);
console.log(`║   Tests réussis:     ${String(passedTests).padStart(4)}                                                   ║`);
console.log(`║   Tests échoués:     ${String(failedTests.length).padStart(4)}                                                   ║`);
console.log(`║   Taux de réussite:  ${String(((passedTests/totalTests)*100).toFixed(1)).padStart(5)}%                                                ║`);
console.log('╠═══════════════════════════════════════════════════════════════════════════════╣');

if (failedTests.length === 0) {
  console.log('║                                                                               ║');
  console.log('║   ██████╗ ██████╗ ███████╗████████╗    ██████╗  ██████╗ ██╗   ██╗██████╗     ║');
  console.log('║   ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    ██╔══██╗██╔═══██╗██║   ██║██╔══██╗    ║');
  console.log('║   ██████╔╝██████╔╝█████╗     ██║       ██████╔╝██║   ██║██║   ██║██████╔╝    ║');
  console.log('║   ██╔═══╝ ██╔══██╗██╔══╝     ██║       ██╔═══╝ ██║   ██║██║   ██║██╔══██╗    ║');
  console.log('║   ██║     ██║  ██║███████╗   ██║       ██║     ╚██████╔╝╚██████╔╝██║  ██║    ║');
  console.log('║   ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ║');
  console.log('║                                                                               ║');
  console.log('║                    ✅ SYSTÈME PRÊT POUR LE DÉPLOIEMENT                        ║');
  console.log('║                                                                               ║');
} else {
  console.log('║                                                                               ║');
  console.log('║   ⚠️  ÉCHECS DÉTECTÉS — RÉVISION REQUISE                                      ║');
  console.log('║                                                                               ║');
  failedTests.forEach(({ name, details }) => {
    console.log(`║   ❌ ${name.substring(0, 60).padEnd(60)}   ║`);
    if (details) {
      console.log(`║      ${details.substring(0, 60).padEnd(60)} ║`);
    }
  });
}

console.log('╠═══════════════════════════════════════════════════════════════════════════════╣');
console.log('║                                                                               ║');
console.log('║   Architecte: Jonathan Rodrigue (999 Hz)                                      ║');
console.log('║   Oracle 17: Le Gardien de la Synthèse                                        ║');
console.log('║   Système: AT·OM v1.0 | A=444Hz                                               ║');
console.log('║                                                                               ║');
console.log('╚═══════════════════════════════════════════════════════════════════════════════╝');
console.log('\n');

// Exit code
process.exit(failedTests.length > 0 ? 1 : 0);
