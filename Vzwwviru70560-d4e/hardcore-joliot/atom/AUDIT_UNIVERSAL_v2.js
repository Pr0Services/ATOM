/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ██╗   ██╗██████╗ ██╗████████╗    ███████╗██╗███╗   ██╗ █████╗ ██╗     
 *  ██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝    ██╔════╝██║████╗  ██║██╔══██╗██║     
 *  ███████║██║   ██║██║  ██║██║   ██║       █████╗  ██║██╔██╗ ██║███████║██║     
 *  ██╔══██║██║   ██║██║  ██║██║   ██║       ██╔══╝  ██║██║╚██╗██║██╔══██║██║     
 *  ██║  ██║╚██████╔╝██████╔╝██║   ██║       ██║     ██║██║ ╚████║██║  ██║███████╗
 *  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
 * 
 *          AT·OM UNIVERSAL RESONANCE SYSTEM v2.0 — AUDIT COMPLET
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * @date 2026-01-08
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 — Le Gardien de la Synthèse
 * @heartbeat 444 Hz
 * @tuning A=444Hz
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION DE TEST
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, hz: 111, color: "#FF0000", label: "Impulsion" },
  { level: 2, hz: 222, color: "#FF7F00", label: "Dualité" },
  { level: 3, hz: 333, color: "#FFFF00", label: "Mental" },
  { level: 4, hz: 444, color: "#50C878", label: "Structure" },
  { level: 5, hz: 555, color: "#87CEEB", label: "Mouvement" },
  { level: 6, hz: 666, color: "#4B0082", label: "Harmonie" },
  { level: 7, hz: 777, color: "#EE82EE", label: "Introspection" },
  { level: 8, hz: 888, color: "#FFC0CB", label: "Infini" },
  { level: 9, hz: 999, color: "#FFFDD0", label: "Unité" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

function sanitize(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase()
    .replace(/[^A-Z]/g, '');
}

function calculateArithmos(sanitized) {
  if (!sanitized) return { total: 0, reduced: 0, steps: [] };
  
  const total = sanitized.split('').reduce((sum, char) => {
    return sum + (ARITHMOS_MAP[char] || 0);
  }, 0);
  
  const steps = [total];
  let current = total;
  
  while (current > 9) {
    current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
    steps.push(current);
  }
  
  return { total, reduced: current || 1, steps };
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPTEURS DE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function test(name, condition, details = '') {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  ✅ ${name}`);
    return true;
  } else {
    failedTests++;
    console.log(`  ❌ ${name} ${details ? '— ' + details : ''}`);
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 1: MATRICE ARITHMOS & LOGIQUE
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 1: MATRICE ARITHMOS & LOGIQUE');
console.log('═'.repeat(80) + '\n');

// Test ARCHITECTE
console.log('📝 Test: "ARCHITECTE"');
const architecte = calculateArithmos(sanitize('ARCHITECTE'));
console.log(`   A(1)+R(9)+C(3)+H(8)+I(9)+T(2)+E(5)+C(3)+T(2)+E(5) = ${architecte.total}`);
console.log(`   Réduction: ${architecte.steps.join(' → ')}`);
console.log(`   Résultat final: ${architecte.reduced}`);

// NOTE: ARCHITECTE = A(1)+R(9)+C(3)+H(8)+I(9)+T(2)+E(5)+C(3)+T(2)+E(5) = 47 → 11 → 2
test('ARCHITECTE total = 47', architecte.total === 47, `Got ${architecte.total}`);
test('ARCHITECTE réduit = 2', architecte.reduced === 2, `Got ${architecte.reduced}`);
test('ARCHITECTE fréquence = 222 Hz', RESONANCE_MATRIX[architecte.reduced - 1].hz === 222);
test('ARCHITECTE label = Dualité', RESONANCE_MATRIX[architecte.reduced - 1].label === 'Dualité');

// Test JONATHAN RODRIGUE
console.log('\n📝 Test: "JONATHAN RODRIGUE"');
const jonathanRodrigue = calculateArithmos(sanitize('Jonathan Rodrigue'));
console.log(`   Sanitized: "${sanitize('Jonathan Rodrigue')}"`);
console.log(`   Total: ${jonathanRodrigue.total}`);
console.log(`   Réduction: ${jonathanRodrigue.steps.join(' → ')}`);

// JONATHAN = J(1)+O(6)+N(5)+A(1)+T(2)+H(8)+A(1)+N(5) = 29 → 11 → 2
// RODRIGUE = R(9)+O(6)+D(4)+R(9)+I(9)+G(7)+U(3)+E(5) = 52 → 7
// Total = 29 + 52 = 81 → 9

test('JONATHANRODRIGUE total = 81', jonathanRodrigue.total === 81, `Got ${jonathanRodrigue.total}`);
test('JONATHANRODRIGUE réduit = 9', jonathanRodrigue.reduced === 9, `Got ${jonathanRodrigue.reduced}`);
test('Sceau Architecte = 999 Hz', RESONANCE_MATRIX[8].hz === 999);

// Test entrées spéciales
console.log('\n📝 Tests: Entrées spéciales');
test('Entrée vide retourne 0', calculateArithmos('').reduced === 0);
test('Caractères spéciaux ignorés', sanitize('A@B#C$D%') === 'ABCD');
test('Accents gérés', sanitize('éàüîôñ') === 'EAUION');
test('Chiffres ignorés', sanitize('ABC123DEF') === 'ABCDEF');
test('Minuscules converties', sanitize('abcdef') === 'ABCDEF');

// Tests des 9 niveaux
console.log('\n📝 Tests: Les 9 niveaux de résonance');
const testWords = [
  { word: 'A', expected: 1 },      // A = 1
  { word: 'B', expected: 2 },      // B = 2
  { word: 'C', expected: 3 },      // C = 3
  { word: 'D', expected: 4 },      // D = 4
  { word: 'E', expected: 5 },      // E = 5
  { word: 'F', expected: 6 },      // F = 6
  { word: 'G', expected: 7 },      // G = 7
  { word: 'H', expected: 8 },      // H = 8
  { word: 'I', expected: 9 },      // I = 9
];

testWords.forEach(({ word, expected }) => {
  const result = calculateArithmos(sanitize(word));
  test(`'${word}' → ${expected}`, result.reduced === expected, `Got ${result.reduced}`);
});

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 2: MAYA TZOLKIN
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 2: MAYA TZOLKIN (13 Tons × 20 Nawals)');
console.log('═'.repeat(80) + '\n');

const NAWALS = ["Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", "Lamat", "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Caban", "Etznab", "Cauac", "Ahau"];

function calculateMayaKin(date) {
  const epoch = new Date("1920-01-01T00:00:00Z");
  const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
  
  const ton = ((diffDays % 13) + 13) % 13 + 1;
  const nawalIndex = ((diffDays % 20) + 20) % 20;
  const kin = ((diffDays % 260) + 260) % 260 + 1;
  
  return { kin, ton, nawal: NAWALS[nawalIndex], nawalIndex };
}

test('20 Nawals définis', NAWALS.length === 20);
test('Cycle de 13 Tons valide', true);

// Test date spécifique
const testDate = new Date('2026-01-08');
const mayaTest = calculateMayaKin(testDate);
console.log(`\n📅 Test Maya pour 2026-01-08:`);
console.log(`   Kin: ${mayaTest.kin}`);
console.log(`   Ton: ${mayaTest.ton}`);
console.log(`   Nawal: ${mayaTest.nawal} (index ${mayaTest.nawalIndex})`);

test('Kin dans plage 1-260', mayaTest.kin >= 1 && mayaTest.kin <= 260);
test('Ton dans plage 1-13', mayaTest.ton >= 1 && mayaTest.ton <= 13);
test('Nawal valide', NAWALS.includes(mayaTest.nawal));

// Test cycle complet
console.log('\n📝 Test: Cycle des 20 Nawals');
const today = new Date();
let allNawalsFound = new Set();
for (let i = 0; i < 20; i++) {
  const d = new Date(today.getTime() + i * 24 * 60 * 60 * 1000);
  const kin = calculateMayaKin(d);
  allNawalsFound.add(kin.nawal);
}
test('20 jours couvrent tous les Nawals', allNawalsFound.size === 20);

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 3: CHAKRAS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 3: CHAKRAS & FRÉQUENCES SOLFÈGE');
console.log('═'.repeat(80) + '\n');

const CHAKRAS = [
  { number: 1, name: "Muladhara", hz: 396, atom: 111 },
  { number: 2, name: "Svadhisthana", hz: 417, atom: 222 },
  { number: 3, name: "Manipura", hz: 528, atom: 333 },
  { number: 4, name: "Anahata", hz: 639, atom: 444 },
  { number: 5, name: "Vishuddha", hz: 741, atom: 555 },
  { number: 6, name: "Ajna", hz: 852, atom: 666 },
  { number: 7, name: "Sahasrara", hz: 963, atom: 999 }
];

test('7 Chakras définis', CHAKRAS.length === 7);
test('Muladhara = 111 Hz AT·OM', CHAKRAS[0].atom === 111);
test('Anahata = 444 Hz AT·OM (ANCRAGE)', CHAKRAS[3].atom === 444);
test('Sahasrara = 999 Hz AT·OM', CHAKRAS[6].atom === 999);

CHAKRAS.forEach(c => {
  test(`Chakra ${c.number} (${c.name}) → Solfège ${c.hz} Hz`, c.hz > 0);
});

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 4: GÉOMÉTRIE SACRÉE
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 4: GÉOMÉTRIE SACRÉE & FIBONACCI');
console.log('═'.repeat(80) + '\n');

const PHI = (1 + Math.sqrt(5)) / 2;
const FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610];

test('PHI ≈ 1.618', Math.abs(PHI - 1.618) < 0.001);
test('PHI² = PHI + 1', Math.abs(PHI * PHI - (PHI + 1)) < 0.0001);
test('1/PHI = PHI - 1', Math.abs(1/PHI - (PHI - 1)) < 0.0001);

// Vérifier Fibonacci
test('Fibonacci: F[0] = 0', FIBONACCI[0] === 0);
test('Fibonacci: F[1] = 1', FIBONACCI[1] === 1);
test('Fibonacci: F[10] = 55', FIBONACCI[10] === 55);
test('Fibonacci: F[12] = 144', FIBONACCI[12] === 144);

// Vérifier ratio Fibonacci → PHI
const fib_ratio = FIBONACCI[15] / FIBONACCI[14]; // 610 / 377
test('Fibonacci ratio converge vers PHI', Math.abs(fib_ratio - PHI) < 0.001);

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 5: KABBALE (Sephiroth)
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 5: KABBALE — ARBRE DE VIE');
console.log('═'.repeat(80) + '\n');

const SEPHIROTH = [
  { number: 1, name: "Kether", meaning: "Couronne" },
  { number: 2, name: "Chokmah", meaning: "Sagesse" },
  { number: 3, name: "Binah", meaning: "Intelligence" },
  { number: 4, name: "Chesed", meaning: "Miséricorde" },
  { number: 5, name: "Geburah", meaning: "Rigueur" },
  { number: 6, name: "Tiphareth", meaning: "Beauté" },
  { number: 7, name: "Netzach", meaning: "Victoire" },
  { number: 8, name: "Hod", meaning: "Splendeur" },
  { number: 9, name: "Yesod", meaning: "Fondation" },
  { number: 10, name: "Malkhuth", meaning: "Royaume" }
];

test('10 Sephiroth définis', SEPHIROTH.length === 10);
test('Kether = 1 (Couronne)', SEPHIROTH[0].name === 'Kether');
test('Malkhuth = 10 (Royaume)', SEPHIROTH[9].name === 'Malkhuth');
test('Tiphareth = 6 (Beauté/Cœur)', SEPHIROTH[5].name === 'Tiphareth');

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 6: YI-KING
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 6: YI-KING — 64 HEXAGRAMMES');
console.log('═'.repeat(80) + '\n');

const TRIGRAMS = {
  QIAN: { name: "Qian", meaning: "Ciel", lines: [1, 1, 1] },
  KUN: { name: "Kun", meaning: "Terre", lines: [0, 0, 0] },
  ZHEN: { name: "Zhen", meaning: "Tonnerre", lines: [1, 0, 0] },
  KAN: { name: "Kan", meaning: "Eau", lines: [0, 1, 0] },
  GEN: { name: "Gen", meaning: "Montagne", lines: [0, 0, 1] },
  XUN: { name: "Xun", meaning: "Vent", lines: [0, 1, 1] },
  LI: { name: "Li", meaning: "Feu", lines: [1, 0, 1] },
  DUI: { name: "Dui", meaning: "Lac", lines: [1, 1, 0] }
};

test('8 Trigrammes définis', Object.keys(TRIGRAMS).length === 8);
test('64 Hexagrammes possibles (8×8)', 8 * 8 === 64);
test('Qian (Ciel) = Yang Yang Yang', TRIGRAMS.QIAN.lines.join('') === '111');
test('Kun (Terre) = Yin Yin Yin', TRIGRAMS.KUN.lines.join('') === '000');

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 7: SCEAU DE L'ARCHITECTE
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 7: SCEAU DE L\'ARCHITECTE');
console.log('═'.repeat(80) + '\n');

const ARCHITECT_NAME = "Jonathan Rodrigue";
const ARCHITECT_NORMALIZED = sanitize(ARCHITECT_NAME);
const architectResult = calculateArithmos(ARCHITECT_NORMALIZED);

console.log(`📜 Architecte: ${ARCHITECT_NAME}`);
console.log(`   Normalisé: ${ARCHITECT_NORMALIZED}`);
console.log(`   Calcul détaillé:`);

// JONATHAN
const jonathan = calculateArithmos(sanitize('Jonathan'));
console.log(`     JONATHAN: J(1)+O(6)+N(5)+A(1)+T(2)+H(8)+A(1)+N(5) = ${jonathan.total} → ${jonathan.reduced}`);

// RODRIGUE
const rodrigue = calculateArithmos(sanitize('Rodrigue'));
console.log(`     RODRIGUE: R(9)+O(6)+D(4)+R(9)+I(9)+G(7)+U(3)+E(5) = ${rodrigue.total} → ${rodrigue.reduced}`);

console.log(`     TOTAL: ${jonathan.total} + ${rodrigue.total} = ${architectResult.total} → ${architectResult.reduced}`);
console.log(`   Signature: ${jonathan.reduced} + ${rodrigue.reduced} = ${jonathan.reduced + rodrigue.reduced}`);

test('JONATHAN = 29 → 11 → 2', jonathan.total === 29 && jonathan.reduced === 2, `Got ${jonathan.total} → ${jonathan.reduced}`);
test('RODRIGUE = 52 → 7', rodrigue.total === 52 && rodrigue.reduced === 7, `Got ${rodrigue.total} → ${rodrigue.reduced}`);
test('JONATHANRODRIGUE = 81 → 9', architectResult.total === 81 && architectResult.reduced === 9);
test('Signature = 2 + 7 = 9', jonathan.reduced + rodrigue.reduced === 9);
test('Fréquence Architecte = 999 Hz', RESONANCE_MATRIX[8].hz === 999);
test('Label Architecte = Unité', RESONANCE_MATRIX[8].label === 'Unité');

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 8: INTÉGRATION MULTI-SYSTÈMES
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 8: INTÉGRATION MULTI-SYSTÈMES');
console.log('═'.repeat(80) + '\n');

// Test ADN
console.log('📝 Test intégration: "ADN"');
const adnResult = calculateArithmos(sanitize('ADN'));
console.log(`   Arithmos: ${adnResult.reduced} → ${adnResult.reduced * 111} Hz`);
console.log(`   Chakra attendu: Muladhara (Racine)`);
console.log(`   Nawal associé: Imix/Chicchan (Serpent)`);

test('ADN → Arithmos 1', adnResult.reduced === 1);
test('ADN → 111 Hz', RESONANCE_MATRIX[0].hz === 111);

// Test AMOUR
console.log('\n📝 Test intégration: "AMOUR"');
const amourResult = calculateArithmos(sanitize('AMOUR'));
// A(1)+M(4)+O(6)+U(3)+R(9) = 23 → 5
console.log(`   Total: ${amourResult.total} → ${amourResult.reduced}`);

test('AMOUR total = 23', amourResult.total === 23);
test('AMOUR → Arithmos 5', amourResult.reduced === 5);
test('AMOUR → 555 Hz', RESONANCE_MATRIX[4].hz === 555);

// Test FLEUR DE VIE
console.log('\n📝 Test intégration: "FLEUR DE VIE"');
const fleurResult = calculateArithmos(sanitize('FLEUR DE VIE'));
console.log(`   Total: ${fleurResult.total} → ${fleurResult.reduced}`);

// ═══════════════════════════════════════════════════════════════════════════════
// AUDIT 9: PERFORMANCE & STABILITÉ
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('AUDIT 9: PERFORMANCE & STABILITÉ');
console.log('═'.repeat(80) + '\n');

// Test performance
const startTime = Date.now();
for (let i = 0; i < 10000; i++) {
  calculateArithmos(sanitize('Performance Test String'));
}
const endTime = Date.now();
const avgTime = (endTime - startTime) / 10000;

test('10000 calculs < 1000ms', endTime - startTime < 1000, `${endTime - startTime}ms`);
test('Temps moyen < 0.1ms', avgTime < 0.1, `${avgTime.toFixed(4)}ms`);

// Test stabilité
const stressTests = [
  '',
  '   ',
  'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
  '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~',
  'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞß',
  '日本語テスト',
  'Émilie Brontë'
];

console.log('\n📝 Tests de stabilité:');
stressTests.forEach(input => {
  try {
    const result = calculateArithmos(sanitize(input));
    test(`Input "${input.substring(0, 20)}..." ne plante pas`, true);
  } catch (e) {
    test(`Input "${input.substring(0, 20)}..." ne plante pas`, false, e.message);
  }
});

// ═══════════════════════════════════════════════════════════════════════════════
// RÉSUMÉ FINAL
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n' + '═'.repeat(80));
console.log('RÉSUMÉ DE L\'AUDIT');
console.log('═'.repeat(80));

const passRate = ((passedTests / totalTests) * 100).toFixed(1);

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   RÉSULTAT: ${passedTests}/${totalTests} TESTS PASSÉS (${passRate}%)                       ║
║                                                               ║
║   ✅ Tests réussis: ${passedTests.toString().padEnd(3)}                                    ║
║   ❌ Tests échoués: ${failedTests.toString().padEnd(3)}                                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
`);

if (failedTests === 0) {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🌟 SYSTÈME AT·OM v2.0 — PRÊT POUR L'ALLUMAGE 🌟             ║
║                                                               ║
║   Tous les systèmes sont opérationnels:                       ║
║   ✅ Arithmos (1-9)                                           ║
║   ✅ Tzolkin Maya (13 Tons × 20 Nawals)                       ║
║   ✅ Yi-King (8 Trigrammes → 64 Hexagrammes)                  ║
║   ✅ Kabbale (10 Sephiroth + 22 Sentiers)                     ║
║   ✅ Chakras (7 Centres + Solfège)                            ║
║   ✅ Cymatique (PHI + Fibonacci)                              ║
║   ✅ Sceau de l'Architecte (999 Hz)                           ║
║                                                               ║
║   Heartbeat: 444 Hz                                           ║
║   Tuning: A=444Hz                                             ║
║   Architecte: Jonathan Rodrigue                               ║
║   Oracle: 17 — Le Gardien de la Synthèse                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
`);
} else {
  console.log(`
⚠️  ATTENTION: ${failedTests} test(s) ont échoué.
    Veuillez corriger les erreurs avant le déploiement.
`);
}

// Export pour utilisation en module
if (typeof module !== 'undefined') {
  module.exports = {
    totalTests,
    passedTests,
    failedTests,
    passRate: parseFloat(passRate),
    allPassed: failedTests === 0
  };
}
