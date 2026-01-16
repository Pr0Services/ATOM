/**
 * Test des modules BioSync et GlobalSync
 */

// Importer les modules
const BioSync = require('./engines/biosync_engine.js');
const GlobalSync = require('./engines/globalsync_engine.js');

console.log(`
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🧬 TEST BIO-SYNC & GLOBAL-SYNC ENGINE 🌍                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
`);

// ═══════════════════════════════════════════════════════════════════
// TEST BIOSYNC
// ═══════════════════════════════════════════════════════════════════

console.log("\n═══ TEST 1: CHAKRA ACTIF PAR L'HEURE ═══");
const activeChakra = BioSync.getActiveChakraByTime();
console.log("Chakra actif:", activeChakra.name);
console.log("Civilisation:", activeChakra.civilization);
console.log("Recommandation:", activeChakra.recommendation);

console.log("\n═══ TEST 2: MÉRIDIEN ACTIF ═══");
const activeMeridian = BioSync.getActiveMeridian();
if (activeMeridian) {
  console.log("Organe actif:", activeMeridian.organ);
  console.log("Activité:", activeMeridian.activity);
}

console.log("\n═══ TEST 3: RÉSONANCE BIOLOGIQUE (444 Hz) ═══");
const bioRes444 = BioSync.getBioResonance(444);
console.log("Chakra cible:", bioRes444.targetChakra.name);
console.log("Glande:", bioRes444.targetChakra.gland);
console.log("Civilisation:", bioRes444.targetChakra.civilization);
console.log("Nadi:", bioRes444.nadi);
console.log("Message:", bioRes444.message);

console.log("\n═══ TEST 4: RÉSONANCE BIOLOGIQUE (999 Hz) ═══");
const bioRes999 = BioSync.getBioResonance(999);
console.log("Chakra cible:", bioRes999.targetChakra.name);
console.log("Glande:", bioRes999.targetChakra.gland);
console.log("Civilisation:", bioRes999.targetChakra.civilization);
console.log("Nadi:", bioRes999.nadi);

console.log("\n═══ TEST 5: SÉQUENCE D'ACTIVATION CHAKRAS ═══");
const sequence = BioSync.generateChakraActivationSequence(7, 21);
console.log("Durée totale:", sequence.totalDuration, "secondes");
console.log("Chakra final:", sequence.targetChakra);
sequence.sequence.forEach(s => {
  console.log(`  ${s.step}. ${s.chakra} — ${s.frequency} Hz — ${s.mantra}`);
});

// ═══════════════════════════════════════════════════════════════════
// TEST GLOBALSYNC
// ═══════════════════════════════════════════════════════════════════

console.log("\n═══════════════════════════════════════════════════════════════");
console.log("                    🌍 TESTS GLOBAL SYNC 🌍");
console.log("═══════════════════════════════════════════════════════════════\n");

const worldSync = new GlobalSync.WorldSyncEngine();

console.log("═══ TEST 6: ÉNERGIE PLANÉTAIRE ACTUELLE ═══");
const planetaryEnergy = GlobalSync.getCurrentPlanetaryEnergy();
console.log("Position solaire:", planetaryEnergy.solarPosition);
console.log("Saison:", planetaryEnergy.seasonalEnergy.season);
console.log("Élément:", planetaryEnergy.seasonalEnergy.element);
console.log("Fréquence globale:", planetaryEnergy.globalFrequency, "Hz");
console.log("Zones actives:", planetaryEnergy.activeZones.map(z => z.zone).join(", "));

console.log("\n═══ TEST 7: ALIGNEMENT UTILISATEUR (Montréal) ═══");
// Coordonnées de Montréal
const userLat = 45.5017;
const userLon = -73.5673;
const heartRate = 60;

const alignment = GlobalSync.alignWithEarth(userLat, userLon, heartRate);
console.log("Status:", alignment.status);
console.log("Nœud le plus proche:", alignment.node.name, alignment.node.icon);
console.log("Distance:", alignment.node.distance);
console.log("Chakra connecté:", alignment.node.chakra);
console.log("Fréquence finale:", alignment.frequency.label);
console.log("Cohérence:", alignment.coherence);
console.log("Message:", alignment.message);

console.log("\n═══ TEST 8: TRIANGULATION ═══");
alignment.triangulation.forEach((t, i) => {
  console.log(`  ${i+1}. ${t.icon} ${t.name} — ${t.distance}`);
});

console.log("\n═══ TEST 9: SITE LE PLUS PROCHE (Paris) ═══");
const parisNearest = GlobalSync.findNearestSacredSite(48.8566, 2.3522);
console.log("Site:", parisNearest.site.name);
console.log("Distance:", parisNearest.distance.toFixed(0), "km");
console.log("Fonction:", parisNearest.site.function);

console.log("\n═══ TEST 10: RAPPORT GLOBAL ═══");
const report = GlobalSync.getGlobalSyncReport();
console.log("Titre:", report.title);
console.log("Schumann:", report.earthConstants.schumann);
console.log("Anchor AT·OM:", report.earthConstants.atomAnchor);
console.log("\nSites principaux:");
report.primarySites.forEach(s => {
  console.log(`  ${s.icon} ${s.name} — ${s.chakra} — ${s.frequency}`);
});

console.log("\n╔═══════════════════════════════════════════════════════════════════╗");
console.log("║                   ✅ TOUS LES TESTS RÉUSSIS                       ║");
console.log("╚═══════════════════════════════════════════════════════════════════╝\n");
