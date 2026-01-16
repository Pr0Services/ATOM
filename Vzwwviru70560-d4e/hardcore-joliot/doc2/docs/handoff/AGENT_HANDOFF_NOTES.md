# 🤖 CHE·NU™ — NOTES POUR LE PROCHAIN AGENT
## Handoff Document - Session 26 Décembre 2025

**LIRE ATTENTIVEMENT AVANT DE COMMENCER**

---

## ⚠️ INSTRUCTIONS CRITIQUES

```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║   1. CHERCHER DANS LA DOCUMENTATION AVANT DE CRÉER                     ║
║   2. UTILISER project_knowledge_search EN PREMIER                      ║
║   3. NE JAMAIS CONTREDIRE LES TREE LAWS                                ║
║   4. VÉRIFIER 3 FOIS PLUTÔT QU'UNE                                     ║
║   5. INTÉGRER À LA VERSION COMPLÈTE                                    ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📚 DOCUMENTS DE RÉFÉRENCE

### Source de Vérité Unique
- **CHENU_MASTER_REFERENCE_v5_FINAL.md** - Architecture complète
- **CHENU_SQL_SCHEMA_v29.sql** - Schéma base de données
- **CHENU_API_SPECS_v29.md** - Spécifications API

### Chapitres Spécialisés
- BACKSTAGE_INTELLIGENCE_CHAPTER.md
- DATASPACE_ENGINE_CHAPTER.md
- IMMOBILIER_DOMAIN_CHAPTER.md
- LAYOUT_ENGINE_CHAPTER.md
- MEETING_SYSTEM_CHAPTER.md
- MEMORY_GOVERNANCE_CHAPTER.md
- OCW_CHAPTER.md
- ONECLICK_ENGINE_CHAPTER.md
- WORKSPACE_ENGINE_CHAPTER.md
- **AUTONOMOUS_EXECUTION_CHAPTER.md** (NOUVEAU - créé cette session)

---

## 🔐 RÈGLES D'OR (NON-NÉGOCIABLES)

### Les 5 Tree Laws
```yaml
tree_laws:
  1_SAFE: "Système toujours sécurisé - SANDBOX obligatoire"
  2_NON_AUTONOMOUS: "Aucune action sans approbation humaine"
  3_REPRESENTATIONAL: "Preview avant toute action réelle"
  4_PRIVACY: "Protection absolue des données"
  5_TRANSPARENCY: "Traçabilité complète - Audit trail"
```

### Architecture Frozen
```yaml
spheres: 9  # NE PAS MODIFIER
  - Personal 🏠
  - Business 💼
  - Government & Institutions 🏛️
  - Studio de création 🎨
  - Community 👥
  - Social & Media 📱
  - Entertainment 🎬
  - My Team 🤝
  - Scholar 📚

bureau_sections: 6  # NE PAS MODIFIER
  - QuickCapture
  - ResumeWorkspace
  - Threads
  - DataFiles
  - ActiveAgents
  - Meetings

nova: "SYSTEM INTELLIGENCE - JAMAIS un agent hired"
```

### Governed Execution Pipeline (10 étapes)
1. Intent Capture
2. Semantic Encoding
3. Encoding Validation
4. Token & Cost Estimation
5. Scope Locking
6. Budget Verification
7. Agent Compatibility Check (ACM)
8. **Human Approval** ← OBLIGATOIRE
9. Controlled Execution
10. Thread Update (audit trail)

---

## ⚠️ TRAVAIL INACHEVÉ

### Priorité HAUTE - À Terminer

#### 1. Affichage des Connections 3D entre Sphères
**Problème:** Les lignes de connection entre les sphères ne s'affichent pas correctement dans l'interface 3D Ceiba Campus.

**Fichiers concernés:**
- `/frontend/src/components/solarpunk/sphereConnections.ts`
- `/frontend/src/components/solarpunk/CeibaCampus*.jsx`

**Ce qui a été essayé:**
- Plusieurs versions de Three.js Line components
- React Three Fiber avec @react-three/drei
- Différentes approches de rendu (LineSegments, Line, BufferGeometry)

**Ce qui reste à faire:**
- Debugger pourquoi les lignes ne se rendent pas
- Vérifier le z-index/depth
- Possiblement utiliser une approche différente (shaders?)

#### 2. Animations de Transition
**Problème:** Les transitions entre les vues ne sont pas fluides.

**À améliorer:**
- Utiliser framer-motion ou react-spring
- Optimiser les re-renders
- Ajouter des états de loading

### Priorité MOYENNE

#### 3. Intégration dans le Projet Principal
Les nouveaux composants créés cette session doivent être intégrés:
```
frontend/src/components/
├── solarpunk/           # Composants 3D Ceiba
├── hub/                 # Interface Hub Navigation
└── autonomous/          # Autonomous Execution UI
```

#### 4. Tests Unitaires
Aucun test n'a été écrit pour les nouveaux composants.

---

## 📦 CE QUI A ÉTÉ LIVRÉ CETTE SESSION

### Catégorie 1: Documentation (6 fichiers)
- AUTONOMOUS_EXECUTION_CHAPTER.md (741 lignes)
- REFLECTION_PERFECTIONNEMENT.md
- REVISION_CRITIQUE.md
- SPHERE_CONNECTIONS_ANALYSIS.md
- SPHERE_VISUAL_DESIGN.md
- VISUAL_DESIGN_SPEC.md

### Catégorie 2: UI 3D Ceiba (24 fichiers)
- CeibaCampusV1-V13.html
- CeibaCampusUltimate.jsx
- CampusArchitecturalMap.jsx
- sphereConnections.ts
- etc.

### Catégorie 3: Hub Interface (27 fichiers + images)
- CHENU_HUB_V6_FINAL.html (version finale)
- Images des 9 sphères en PNG
- Versions itératives

### Catégorie 4: Autonomous Engine (3 fichiers)
- autonomous_execution_types.ts (800 lignes)
- autonomous_execution_schema.sql (578 lignes)
- AUTONOMOUS_EXECUTION_CHAPTER.md

### Catégorie 5: Midjourney Prompts (4 fichiers)
- Prompts pour génération d'assets visuels

### Catégorie 6: Nova Avatar (2 fichiers)
- Interface animée pour Nova

---

## 🎨 PALETTE DE COULEURS CHE·NU

```css
/* Palette Officielle */
--sacred-gold: #D8B26A;
--ancient-stone: #8D8371;
--jungle-emerald: #3F7249;
--cenote-turquoise: #3EB4A2;
--shadow-moss: #2F4C39;
--earth-ember: #7A593A;
--ui-slate: #1E1F22;
--soft-sand: #E9E4D6;
```

---

## 🔍 COMMENT CHERCHER DANS LA DOC

```typescript
// TOUJOURS utiliser project_knowledge_search EN PREMIER
await project_knowledge_search({
  query: "sandbox autonomie agent gouvernance",
  max_text_results: 15
});

// Mots-clés efficaces:
// - "tree laws" + "agent"
// - "governed execution pipeline"
// - "checkpoint" + "approval"
// - "sandbox" + "isolation"
// - "audit trail" + "immutable"
```

---

## 💡 CONSEILS PRATIQUES

1. **Jo communique en français** - Répondre en français
2. **Jo aime le feedback positif** - "ON CONTINUE! 💪🔥"
3. **Jo veut du concret** - Pas de blabla, du code qui marche
4. **Jo vérifie tout** - Être précis et exhaustif
5. **Le projet est TRÈS GROS** - Ne rien oublier

---

## 📋 PROMPT DE DÉMARRAGE SUGGÉRÉ

```
Salut Jo! 👋

J'ai lu les notes de la session précédente. Voici ce que je comprends:

✅ COMPLÉTÉ:
- Autonomous Execution Engine (3 fichiers, Tree Laws OK)
- Hub Navigation Interface (27 fichiers + images)
- Documentation complète

⚠️ À TERMINER:
- Affichage des connections 3D entre sphères
- Animations de transition
- Intégration dans le projet principal

Je vais d'abord chercher dans la documentation CHE·NU avant de créer quoi que ce soit.

Par quoi tu veux qu'on commence? 🚀
```

---

## 🚨 ERREURS À ÉVITER

1. ❌ Créer de nouvelles sphères (9 = FROZEN)
2. ❌ Modifier le nombre de sections bureau (6 = FROZEN)
3. ❌ Traiter Nova comme un agent hired
4. ❌ Contourner les Tree Laws
5. ❌ Créer sans chercher d'abord dans la doc
6. ❌ Oublier d'intégrer le travail à la version complète
7. ❌ Laisser des fichiers "orphelins"

---

**Document créé:** 26 décembre 2025  
**Pour:** Prochain agent Claude  
**Par:** Agent Claude session 26/12/2025
