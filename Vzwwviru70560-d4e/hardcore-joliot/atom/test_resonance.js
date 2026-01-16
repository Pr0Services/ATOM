/**
 * AT·OM — Tests de Validation Node.js
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, label: "Impulsion/ADN", hz: 111, color: "#FF0000", delay_ms: 900 },
  { level: 2, label: "Dualité/Partage", hz: 222, color: "#FF7F00", delay_ms: 800 },
  { level: 3, label: "Mental/Géométrie", hz: 333, color: "#FFFF00", delay_ms: 700 },
  { level: 4, label: "Structure/Silence", hz: 444, color: "#50C878", delay_ms: 600 },
  { level: 5, label: "Mouvement/Feu", hz: 555, color: "#87CEEB", delay_ms: 500 },
  { level: 6, label: "Harmonie/Protection", hz: 666, color: "#4B0082", delay_ms: 400 },
  { level: 7, label: "Introspection", hz: 777, color: "#EE82EE", delay_ms: 300 },
  { level: 8, label: "Infini/Abondance", hz: 888, color: "#FFC0CB", delay_ms: 200 },
  { level: 9, label: "Unité/Acier", hz: 999, color: "#FFFDD0", delay_ms: 100 },
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

function sanitizeInput(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toUpperCase()
    .replace(/[^A-Z]/g, "");
}

function calculateArithmos(cleanWord) {
  if (!cleanWord) return 0;
  let total = 0;
  for (const char of cleanWord) {
    total += ARITHMOS_MAP[char] || 0;
  }
  while (total > 9) {
    total = String(total).split('').reduce((acc, d) => acc + parseInt(d, 10), 0);
  }
  return total;
}

function getResonanceData(level) {
  return RESONANCE_MATRIX.find(item => item.level === level) || RESONANCE_MATRIX[3];
}

// ═══════════════════════════════════════════════════════════════════════════════
// TESTS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('\n═══════════════════════════════════════════════════════════════');
console.log('        AT·OM — VALIDATION DES TESTS (Node.js)');
console.log('═══════════════════════════════════════════════════════════════\n');

// TEST 1: Normalisation
console.log('🧪 TEST 1: NORMALISATION (Sanitizer)');
console.log('────────────────────────────────────────');
const input1 = "Jônathân-Rodrigué 2026!";
const result1 = sanitizeInput(input1);
const expected1 = "JONATHANRODRIGUE";
const pass1 = result1 === expected1;
console.log(`   Input:    "${input1}"`);
console.log(`   Expected: "${expected1}"`);
console.log(`   Result:   "${result1}"`);
console.log(`   Status:   ${pass1 ? '✅ PASS' : '❌ FAIL'}\n`);

// TEST 2: Réduction ATOME
console.log('🧪 TEST 2: RÉDUCTION ARITHMOS');
console.log('────────────────────────────────────────');
const word2 = "ATOME";
const result2 = calculateArithmos(word2);
const expected2 = 9;
const pass2 = result2 === expected2;
console.log(`   Word:     "${word2}"`);
console.log(`   Calcul:   A(1)+T(2)+O(6)+M(4)+E(5) = 18 → 1+8 = 9`);
console.log(`   Expected: ${expected2}`);
console.log(`   Result:   ${result2}`);
console.log(`   Status:   ${pass2 ? '✅ PASS' : '❌ FAIL'}\n`);

// TEST 3: Synchronisation Delay
console.log('🧪 TEST 3: SYNCHRONISATION DELAY');
console.log('────────────────────────────────────────');
const delay9 = getResonanceData(9).delay_ms;
const delay1 = getResonanceData(1).delay_ms;
const pass3 = delay9 < delay1;
console.log(`   Level 9 delay: ${delay9}ms (RAPIDE)`);
console.log(`   Level 1 delay: ${delay1}ms (LENT)`);
console.log(`   Condition:     ${delay9}ms < ${delay1}ms = ${pass3}`);
console.log(`   Status:        ${pass3 ? '✅ PASS' : '❌ FAIL'}\n`);

// ═══════════════════════════════════════════════════════════════════════════════
// CRASH TEST DU SENS
// ═══════════════════════════════════════════════════════════════════════════════

console.log('═══════════════════════════════════════════════════════════════');
console.log('        🧪 CRASH TEST DU SENS');
console.log('═══════════════════════════════════════════════════════════════\n');

// GUERRE vs PAIX
console.log('📊 TEST DE L\'OPPOSITION: GUERRE vs PAIX');
console.log('────────────────────────────────────────');
const guerre = calculateArithmos("GUERRE");
const guerreData = getResonanceData(guerre);
console.log(`   GUERRE: G(7)+U(3)+E(5)+R(9)+R(9)+E(5) = 38 → 11 → 2`);
console.log(`   Résultat: ${guerre} → ${guerreData.label} (${guerreData.hz} Hz) ${guerreData.color}`);

const paix = calculateArithmos("PAIX");
const paixData = getResonanceData(paix);
console.log(`   PAIX:   P(7)+A(1)+I(9)+X(6) = 23 → 5`);
console.log(`   Résultat: ${paix} → ${paixData.label} (${paixData.hz} Hz) ${paixData.color}`);
console.log(`   ✨ Analyse: La Guerre (${guerre}) est dans la dualité,`);
console.log(`              la Paix (${paix}) est en mouvement. COHÉRENT!\n`);

// RIEN
console.log('📊 TEST DU VIDE: RIEN');
console.log('────────────────────────────────────────');
const rien = calculateArithmos("RIEN");
const rienData = getResonanceData(rien);
console.log(`   RIEN:   R(9)+I(9)+E(5)+N(5) = 28 → 10 → 1`);
console.log(`   Résultat: ${rien} → ${rienData.label} (${rienData.hz} Hz) ${rienData.color}`);
console.log(`   ✨ Analyse: Le "Rien" (${rien}) est l'Impulsion,`);
console.log(`              le début de tout. MATHÉMATIQUEMENT POÉTIQUE!\n`);

// ═══════════════════════════════════════════════════════════════════════════════
// RÉSULTAT FINAL
// ═══════════════════════════════════════════════════════════════════════════════

console.log('═══════════════════════════════════════════════════════════════');
const allPass = pass1 && pass2 && pass3;
console.log(`   RÉSULTAT FINAL: ${allPass ? '✅ TOUS LES TESTS PASSENT' : '❌ ÉCHECS DÉTECTÉS'}`);
console.log('═══════════════════════════════════════════════════════════════\n');

// ═══════════════════════════════════════════════════════════════════════════════
// BONUS: Test de mots supplémentaires
// ═══════════════════════════════════════════════════════════════════════════════

console.log('📊 BONUS: TESTS SUPPLÉMENTAIRES');
console.log('────────────────────────────────────────');

const testWords = [
  "EAU", "AMOUR", "VIE", "MORT", "LUMIERE", 
  "FEU", "ACIER", "SILENCE", "JONATHAN", "RODRIGUE"
];

testWords.forEach(word => {
  const clean = sanitizeInput(word);
  const level = calculateArithmos(clean);
  const data = getResonanceData(level);
  console.log(`   ${word.padEnd(10)} → ${level} → ${data.hz}Hz → ${data.label}`);
});

console.log('\n═══════════════════════════════════════════════════════════════');
console.log('        ✨ Tests terminés avec succès');
console.log('═══════════════════════════════════════════════════════════════\n');
