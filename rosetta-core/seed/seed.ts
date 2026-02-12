/**
 * AT·OM — Genesis Seed (Vision Complète)
 * Injection de la première donnée : le Genesis Node du Yucatán
 * + Données Genesis pour TOUTES les facettes du diamant
 *
 * Le Point Zéro — Cratère de Chicxulub
 * C'est le premier node de l'Arbre de Vie, la racine de tout.
 * Traduit par le RosettaParser dans les 3 dimensions.
 *
 * Le même flux circule à travers TOUTES les facettes :
 *   TECHNIQUE    → Genesis Node (Point Zéro)
 *   GOUVERNANCE  → Constitution de l'Arche (première proposition)
 *   ÉCONOMIE     → Minting initial (premiers jetons UR)
 *   IDENTITÉ     → DID Système (premier souverain)
 *   MAPPING      → Événement Chicxulub (première entrée historique)
 */

import { RosettaParser, TalentTemplate, SphereEventTemplate, AlchemyTemplate } from '../src/parser/RosettaParser';
import { PolishingEngine } from '../src/engines/PolishingEngine';
import { VibrationalMotor } from '../src/engines/VibrationalMotor';
import {
  type ATOMNode,
  type RosettaTranslation,
  SACRED_FREQUENCIES,
  POINT_ZERO,
  GOVERNANCE_DEFAULTS,
} from '../src/types/atom-types';

// ─── Templates des facettes ─────────────────────────────────
import { ChakraTemplate } from '../src/parser/templates/ChakraTemplate';
import { KabbaleTemplate } from '../src/parser/templates/KabbaleTemplate';
import { MayaTemplate } from '../src/parser/templates/MayaTemplate';
import { YiKingTemplate } from '../src/parser/templates/YiKingTemplate';
import { CosmicTemplate } from '../src/parser/templates/CosmicTemplate';
import { GovernanceTemplate } from '../src/parser/templates/GovernanceTemplate';
import { EconomyTemplate } from '../src/parser/templates/EconomyTemplate';
import { MappingTemplate } from '../src/parser/templates/MappingTemplate';
import { IdentityTemplate } from '../src/parser/templates/IdentityTemplate';
import { RedemptionTemplate } from '../src/parser/templates/RedemptionTemplate';

// ═══════════════════════════════════════════════════════════
// INITIALISATION DES MOTEURS
// ═══════════════════════════════════════════════════════════

const parser = new RosettaParser({
  system_frequency: SACRED_FREQUENCIES.SOURCE,  // 999Hz pour le Genesis
  mode: 'genesis',
});

const motor = new VibrationalMotor();
const polisher = new PolishingEngine();

// ─── Enregistrer TOUS les templates (13 domaines) ─────────
// Templates de base
parser.registerTemplate(TalentTemplate);
parser.registerTemplate(SphereEventTemplate);
parser.registerTemplate(AlchemyTemplate);

// Templates cosmologiques (Facette Spirituelle)
parser.registerTemplate(ChakraTemplate);
parser.registerTemplate(KabbaleTemplate);
parser.registerTemplate(MayaTemplate);
parser.registerTemplate(YiKingTemplate);
parser.registerTemplate(CosmicTemplate);

// Templates des facettes opérationnelles
parser.registerTemplate(GovernanceTemplate);
parser.registerTemplate(EconomyTemplate);
parser.registerTemplate(MappingTemplate);
parser.registerTemplate(IdentityTemplate);
parser.registerTemplate(RedemptionTemplate);

// ═══════════════════════════════════════════════════════════
// GENESIS NODE — Point Zéro
// ═══════════════════════════════════════════════════════════

/** Le premier Node de l'Arbre de Vie */
const genesisNode: ATOMNode = {
  id: 'genesis_chicxulub_001',
  parent_id: null,                              // Racine — pas de parent
  sphere_id: 'SPIRITUALITE',                    // Sphère 9 — La Source
  title: 'Point Zéro — Cratère de Chicxulub',
  status: 'genesis',
  depth: 0,                                     // Profondeur 0 — la racine
  spiral_position: 0,                           // Centre du Disque de Phaistos
  resonance_level: 9,                           // Niveau maximum — 999Hz
  rosetta: null as unknown as RosettaTranslation, // Sera rempli ci-dessous
  created_by: 'system',
  created_at: Date.now(),
  updated_at: Date.now(),
};

// ═══════════════════════════════════════════════════════════
// TRADUCTION ROSETTA DU GENESIS NODE
// ═══════════════════════════════════════════════════════════

const genesisTranslation = parser.translate(
  'sphere_event',
  {
    sphere: 'SPIRITUALITE',
    event_name: 'GENESIS',
    data: {
      location: POINT_ZERO.name,
      coordinates: {
        latitude: POINT_ZERO.latitude,
        longitude: POINT_ZERO.longitude,
      },
      significance: 'Point d\'impact qui a réinitialisé la vie sur Terre il y a 66 millions d\'années',
      activation: 'Ce point géographique active la fréquence maximale du système (999Hz)',
      message: 'Nous n\'inventons rien. Nous nous souvenons de tout.',
    },
  },
  'SPIRIT',
  genesisNode.id,
);

// Attacher la traduction au node
genesisNode.rosetta = genesisTranslation;

// ═══════════════════════════════════════════════════════════
// VALIDATION ALCHIMIQUE
// ═══════════════════════════════════════════════════════════

const genesisValidation = polisher.polishData({
  node: genesisNode,
  rosetta: genesisTranslation,
});

// ═══════════════════════════════════════════════════════════
// ACTIVATION VIBRATIONNELLE — Simulation au Point Zéro
// ═══════════════════════════════════════════════════════════

const vibrationalState = motor.updatePosition({
  latitude: POINT_ZERO.latitude,
  longitude: POINT_ZERO.longitude,
});

// ═══════════════════════════════════════════════════════════
// DONNÉES GENESIS — FACETTES DU DIAMANT
// ═══════════════════════════════════════════════════════════

/** Proposition constitutionnelle Genesis — "Constitution de l'Arche" */
const genesisProposal = {
  id: 'proposal_genesis_001',
  type: 'CONSTITUTIONNELLE' as const,
  title: 'Constitution de l\'Arche — Principes Fondateurs',
  description: 'Les 7 principes immuables qui gouvernent AT·OM : Souveraineté, Transparence, Non-extraction, Consentement, Droit de sortie, Équité, Vérité préservée.',
  sphere_id: 'SPIRITUALITE' as const,
  proposer_id: 'system',
  status: 'APPROVED' as const,
  stake_required: GOVERNANCE_DEFAULTS.proposal_stake_constitutionnelle,
  quorum_pct: 1.0,       // 100% — unanimité pour la constitution
  approval_pct: 1.0,     // 100%
  discussion_days: 7,
  votes_pour: 1,
  votes_contre: 0,
  votes_abstention: 0,
};

/** Transaction Genesis — Premier minting du système */
const genesisMinting = {
  id: 'tx_genesis_001',
  type: 'MINT_JT' as const,
  from_id: null,           // Système
  to_id: 'system',
  amount_ur: 999,          // 999 UR initiaux — fréquence Source
  sphere_id: 'ECONOMIE' as const,
  description: 'Genesis Minting — Création de la masse monétaire initiale d\'AT·OM',
};

/** Identité Genesis — DID Système */
const genesisIdentity = {
  did: 'did:atom:genesis',
  display_name: 'AT·OM Genesis',
  resonance_score: 100,
  rank: 'ARCHITECTE' as const,
  is_sovereign: true,
};

/** Mapping Genesis — Événement Chicxulub */
const genesisMapping = {
  id: 'map_genesis_001',
  layer: 'EVENEMENTS' as const,
  title: 'Impact de Chicxulub — Réinitialisation de la Vie',
  epoch_start: -66000000,  // Il y a 66 millions d'années
  epoch_end: -66000000,
  sphere_connections: ['SPIRITUALITE', 'ENVIRONNEMENT'] as const,
  resonance_frequency: 999,
  source: {
    type: 'archaeological' as const,
    reference: 'Hildebrand et al., 1991 — Chicxulub Crater: A possible Cretaceous/Tertiary boundary impact crater on the Yucatán Peninsula, Mexico',
    credibility_score: 95,
    verified_on_chain: false,
  },
};

// ═══════════════════════════════════════════════════════════
// SQL SEED — Script d'insertion pour Supabase
// ═══════════════════════════════════════════════════════════

export function generateSeedSQL(): string {
  const t = genesisTranslation;
  return `
-- ═══════════════════════════════════════════════════════════
-- AT·OM — GENESIS SEED (Vision Complète)
-- Premier node de l'Arbre de Vie + Données de toutes les facettes
-- Point Zéro : Cratère de Chicxulub, Yucatán
-- ═══════════════════════════════════════════════════════════

-- 1. Genesis Node
INSERT INTO nodes (id, parent_id, sphere_id, title, status, depth, spiral_position, spiral_ring, resonance_level)
VALUES (
  '${genesisNode.id}',
  NULL,
  'SPIRITUALITE',
  '${genesisNode.title}',
  'genesis',
  0,
  0,
  0,
  9
);

-- 2. Rosetta Mapping (3 dimensions)
INSERT INTO rosetta_mappings (node_id, tech_payload, people_narrative, people_explanation, people_tone, spirit_payload, source_dimension, integrity_hash)
VALUES (
  '${genesisNode.id}',
  '${JSON.stringify(t.tech)}'::jsonb,
  '${t.people.narrative.replace(/'/g, "''")}',
  '${t.people.explanation.replace(/'/g, "''")}',
  '${t.people.emotional_tone}',
  '${JSON.stringify(t.spirit)}'::jsonb,
  '${t.source_dimension}',
  '${t.integrity_hash}'
);

-- 3. Spiral Position (centre du Disque de Phaistos)
INSERT INTO spiral_positions (node_id, ring, angle, depth, essence_distance)
VALUES (
  '${genesisNode.id}',
  0,
  0,
  0,
  0
);

-- 4. Vibrational Log (activation initiale)
INSERT INTO vibrational_logs (frequency_hz, resonance_level, latitude, longitude, distance_to_zero, is_in_crater, mode, node_id, metadata)
VALUES (
  999,
  9,
  ${POINT_ZERO.latitude},
  ${POINT_ZERO.longitude},
  0,
  true,
  'genesis',
  '${genesisNode.id}',
  '{"event": "GENESIS", "message": "Nous n''inventons rien. Nous nous souvenons de tout."}'::jsonb
);

-- 5. Alchemy Validation (démarrage au niveau 7 — cristallisé d'origine)
INSERT INTO alchemy_validations (node_id, current_stage, stage_index, is_aligned)
VALUES (
  '${genesisNode.id}',
  'COAGULATION',
  7,
  ${genesisValidation.is_aligned}
);

-- ═══════════════════════════════════════════════════════════
-- FACETTES DU DIAMANT — DONNÉES GENESIS
-- ═══════════════════════════════════════════════════════════

-- 6. Gouvernance — Proposition constitutionnelle Genesis
INSERT INTO governance_proposals (id, type, title, description, sphere_id, proposer_id, status, stake_required, quorum_pct, approval_pct, discussion_days, votes_pour, votes_contre, votes_abstention)
VALUES (
  '${genesisProposal.id}',
  'CONSTITUTIONNELLE',
  '${genesisProposal.title.replace(/'/g, "''")}',
  '${genesisProposal.description.replace(/'/g, "''")}',
  'SPIRITUALITE',
  '${genesisProposal.proposer_id}',
  'APPROVED',
  ${genesisProposal.stake_required},
  ${genesisProposal.quorum_pct},
  ${genesisProposal.approval_pct},
  ${genesisProposal.discussion_days},
  ${genesisProposal.votes_pour},
  ${genesisProposal.votes_contre},
  ${genesisProposal.votes_abstention}
);

-- 7. Économie — Genesis Minting (premiers UR)
INSERT INTO economic_transactions (id, type, from_id, to_id, amount_ur, sphere_id, description, is_flow_keeper)
VALUES (
  '${genesisMinting.id}',
  'MINT_JT',
  NULL,
  NULL,
  ${genesisMinting.amount_ur},
  'ECONOMIE',
  '${genesisMinting.description.replace(/'/g, "''")}',
  false
);

-- 8. Mapping — Événement Chicxulub
INSERT INTO mapping_entries (id, layer, title, epoch_start, epoch_end, sphere_connections, resonance_frequency)
VALUES (
  '${genesisMapping.id}',
  'EVENEMENTS',
  '${genesisMapping.title.replace(/'/g, "''")}',
  ${genesisMapping.epoch_start},
  ${genesisMapping.epoch_end},
  ARRAY['SPIRITUALITE', 'ENVIRONNEMENT']::sphere_id[],
  ${genesisMapping.resonance_frequency}
);

-- 9. Mapping Source — Source archéologique
INSERT INTO mapping_sources (entry_id, type, reference, credibility_score, verified_on_chain)
VALUES (
  '${genesisMapping.id}',
  '${genesisMapping.source.type}',
  '${genesisMapping.source.reference.replace(/'/g, "''")}',
  ${genesisMapping.source.credibility_score},
  ${genesisMapping.source.verified_on_chain}
);
`;
}

// ═══════════════════════════════════════════════════════════
// RAPPORT DE SEED
// ═══════════════════════════════════════════════════════════

export function printSeedReport(): void {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  AT·OM — GENESIS SEED REPORT (Vision Complète)');
  console.log('═══════════════════════════════════════════════════════════');
  console.log('');
  console.log('  ─── TEMPLATES ENREGISTRÉS (13) ───');
  console.log('  Base       : TalentTemplate, SphereEventTemplate, AlchemyTemplate');
  console.log('  Cosmologie : ChakraTemplate, KabbaleTemplate, MayaTemplate, YiKingTemplate, CosmicTemplate');
  console.log('  Facettes   : GovernanceTemplate, EconomyTemplate, MappingTemplate, IdentityTemplate, RedemptionTemplate');
  console.log('');
  console.log(`  ─── GENESIS NODE ───`);
  console.log(`  Node ID:     ${genesisNode.id}`);
  console.log(`  Titre:       ${genesisNode.title}`);
  console.log(`  Sphère:      ${genesisNode.sphere_id} (999Hz)`);
  console.log(`  Status:      ${genesisNode.status}`);
  console.log('');
  console.log('  ─── ROSETTA (3 Dimensions) ───');
  console.log(`  TECH:    ${JSON.stringify(genesisTranslation.tech.data_type)}`);
  console.log(`  PEOPLE:  ${genesisTranslation.people.narrative}`);
  console.log(`  SPIRIT:  ${genesisTranslation.spirit.frequency_hz}Hz / ${genesisTranslation.spirit.sacred_geometry}`);
  console.log(`  Hash:    ${genesisTranslation.integrity_hash}`);
  console.log('');
  console.log('  ─── ALCHIMIE (Table d\'Émeraude) ───');
  console.log(`  Stage:   ${genesisValidation.current_stage} (${genesisValidation.stage_index}/7)`);
  console.log(`  Aligné:  ${genesisValidation.is_aligned ? 'OUI — Or cristallisé' : 'NON — Polissage requis'}`);
  if (genesisValidation.polishing_notes.length > 0) {
    console.log('  Notes:');
    genesisValidation.polishing_notes.forEach(n => console.log(`    ${n}`));
  }
  console.log('');
  console.log('  ─── VIBRATION (Point Zéro) ───');
  console.log(`  Fréquence:  ${vibrationalState.system_resonance}Hz`);
  console.log(`  Cratère:    ${vibrationalState.is_in_crater ? 'ACTIF' : 'Inactif'}`);
  console.log(`  Distance:   ${Math.round(vibrationalState.distance_to_zero)}km`);
  console.log(`  Mode:       ${vibrationalState.mode}`);
  console.log('');
  console.log('  ─── GOUVERNANCE (Facette Politique) ───');
  console.log(`  Proposition: ${genesisProposal.title}`);
  console.log(`  Type:        ${genesisProposal.type}`);
  console.log(`  Status:      ${genesisProposal.status}`);
  console.log(`  Stake:       ${genesisProposal.stake_required} UR`);
  console.log('');
  console.log('  ─── ÉCONOMIE (Facette Économique) ───');
  console.log(`  Minting:     ${genesisMinting.amount_ur} UR`);
  console.log(`  Type:        ${genesisMinting.type}`);
  console.log(`  Sphère:      ${genesisMinting.sphere_id}`);
  console.log('');
  console.log('  ─── IDENTITÉ (Facette Identitaire) ───');
  console.log(`  DID:         ${genesisIdentity.did}`);
  console.log(`  Nom:         ${genesisIdentity.display_name}`);
  console.log(`  Rang:        ${genesisIdentity.rank}`);
  console.log(`  Souverain:   ${genesisIdentity.is_sovereign ? 'OUI' : 'NON'}`);
  console.log('');
  console.log('  ─── MAPPING (Facette Historique) ───');
  console.log(`  Entrée:      ${genesisMapping.title}`);
  console.log(`  Couche:      ${genesisMapping.layer}`);
  console.log(`  Époque:      Il y a ${Math.abs(genesisMapping.epoch_start / 1000000)} M années`);
  console.log(`  Source:      ${genesisMapping.source.type} (crédibilité: ${genesisMapping.source.credibility_score}/100)`);
  console.log('');
  console.log('  "Nous n\'inventons rien. Nous nous souvenons de tout."');
  console.log('═══════════════════════════════════════════════════════════');
}

// Exécution si lancé directement
printSeedReport();
console.log('\n--- SQL SEED ---');
console.log(generateSeedSQL());
