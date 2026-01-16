# 🔄 CHE·NU™ V76 — PROTOCOLE DE SYNCHRONISATION

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                         SYNC PROTOCOL V76 — DOCUMENT OFFICIEL                        ║
║                                                                                      ║
║                    Coordination Agent A (Contrôleur) ↔ Agent B (Exécuteur)          ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

**Version:** 1.0  
**Date:** 8 Janvier 2026  
**Usage:** À utiliser par Jo pour coordonner les deux agents

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Le Handshake (Avant Phase)](#2-le-handshake-avant-phase)
3. [Le Contrat de Sync (Fin de Phase)](#3-le-contrat-de-sync-fin-de-phase)
4. [Le Rythme de Sprint (48h)](#4-le-rythme-de-sprint-48h)
5. [Checkpoints de Réconciliation](#5-checkpoints-de-réconciliation)
6. [Templates Prêts à Copier](#6-templates-prêts-à-copier)
7. [Procédure d'Arrêt Critique](#7-procédure-darrêt-critique)

---

# 1. VUE D'ENSEMBLE

## Rôles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RÉPARTITION DES RÔLES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AGENT A — CONTRÔLEUR & HACKER DE QUALITÉ                                   │
│  ├── Tests unitaires & E2E                                                  │
│  ├── Documentation API                                                      │
│  ├── Audit R&D compliance                                                   │
│  ├── Script check_compliance.py                                             │
│  └── Réconciliation & validation                                            │
│                                                                             │
│  AGENT B — INTÉGRATEUR DE SYSTÈMES                                          │
│  ├── Intégration backend routers                                            │
│  ├── Connexion frontend pages                                               │
│  ├── Déduplication logique                                                  │
│  ├── Génération api_map.json                                                │
│  └── Database & real-time                                                   │
│                                                                             │
│  JO — ORCHESTRATEUR HUMAIN                                                  │
│  ├── Transmet les Sync Contracts entre agents                               │
│  ├── Décisions sur violations R&D                                           │
│  ├── Validation des réconciliations                                         │
│  └── Direction stratégique                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Flow de Communication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLOW DE SYNCHRONISATION                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Agent B → HANDSHAKE → Jo → Agent A                                      │
│     "Voici ce que je compte faire"                                          │
│                                                                             │
│  2. Agent A → VALIDATION → Jo → Agent B                                     │
│     "OK, c'est testable, GO"                                                │
│                                                                             │
│  3. [EXÉCUTION PARALLÈLE - 48h]                                            │
│     Agent B: Code          Agent A: Tests                                   │
│                                                                             │
│  4. Agent B → SYNC CONTRACT → Jo → Agent A                                  │
│     "Voici ce que j'ai fait"                                                │
│                                                                             │
│  5. Agent A → VALIDATION REPORT → Jo → Agent B                              │
│     "Voici les problèmes trouvés"                                           │
│                                                                             │
│  6. [RÉCONCILIATION si nécessaire]                                          │
│                                                                             │
│  7. NEXT PHASE...                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. LE HANDSHAKE (AVANT PHASE)

## Quand l'utiliser

**AVANT que Agent B commence une nouvelle phase.**

## Template à Copier

```markdown
### 🤝 HANDSHAKE — PHASE B[X]

**Agent B → Agent A**
**Date:** [Date]

#### 📋 Signatures de Fonctions Prévues

```python
# Router/Service: [nom].py

# Fonction 1
async def function_name(param: Type, user: User) -> ReturnType:
    """Description"""
    pass

# Fonction 2
async def another_function(id: UUID, user: User) -> None:
    """⚠️ Action sensible - nécessite checkpoint"""
    pass
```

#### 🔗 Dépendances Requises
- Service existant: [nom_service.py]
- Middleware: [identity_boundary, etc.]
- Modèles: [Model1, Model2]

#### ⚠️ Points d'Attention pour Tests
- [ ] Endpoint X doit retourner HTTP 403 si identity mismatch
- [ ] Endpoint Y doit retourner HTTP 423 pour action sensible
- [ ] Chronological order (pas de ranking) pour list endpoints

#### 🎯 Edge Cases à Couvrir
- [ ] [Edge case 1]
- [ ] [Edge case 2]

---

**Agent A, valides-tu ces signatures comme testables?**
```

## Réponse Attendue d'Agent A

```markdown
### ✅ HANDSHAKE VALIDÉ — PHASE B[X]

**Agent A → Agent B**
**Date:** [Date]

#### Validation des Signatures
- ✅ function_name: Testable, Dependency Injection OK
- ⚠️ another_function: Ajouter paramètre `checkpoint_service` pour mock

#### Mocks Préparés
- MockUserService
- MockCheckpointService

#### Tests Prévus
- test_function_name_success
- test_function_name_identity_boundary
- test_another_function_requires_checkpoint

---

**GO pour Phase B[X]! 🚀**
```

---

# 3. LE CONTRAT DE SYNC (FIN DE PHASE)

## Quand l'utiliser

**À LA FIN de chaque phase, l'agent actif remplit ce contrat.**

## Template Agent B → Agent A

```markdown
### 🔄 SYNC PROTOCOL V76 — PHASE B[X]
**Statut de l'Intégrité:** Agent B → Agent A
**Date:** [Date]

#### 🏗️ MODIFICATIONS ARCHITECTURALES
- **Endpoints créés/modifiés:** [Nombre] ([Liste des paths])
- **Tables DB impactées:** [table1, table2]
- **Nouveaux Hooks/Services:** [useHook1, Service2]
- **Fichier api_map.json:** Mis à jour ✅

#### 🛡️ GOUVERNANCE R&D CHECK (7/7)
| Règle | Status | Détail |
|-------|--------|--------|
| #1 Sovereignty | ✅/⚠️/❌ | Checkpoints sur [actions] |
| #2 Autonomy | ✅/⚠️/❌ | [détail] |
| #3 Boundaries | ✅/⚠️/❌ | HTTP 403 sur [endpoints] |
| #4 My Team | ✅/⚠️/❌ | [détail] |
| #5 No Ranking | ✅/⚠️/❌ | ORDER BY created_at DESC |
| #6 Traceability | ✅/⚠️/❌ | Champs présents sur [models] |
| #7 Continuity | ✅/⚠️/❌ | Cohérent avec [décisions] |

#### 🔍 DÉDUPLICATION EFFECTUÉE
| Original | Consolidé vers | Raison |
|----------|---------------|--------|
| [fichier1] | [fichier2] | [raison] |

#### ⚠️ DETTE TECHNIQUE & BLOCAGES
- [Compromis 1]: [Raison] — À corriger en Phase [Y]
- [Blocage 1]: [Description] — Besoin décision Jo

#### 📊 MÉTRIQUES
- Endpoints total: [X] (+[Y] cette phase)
- Pages connectées: [X] (+[Y] cette phase)
- Hooks créés: [X] (+[Y] cette phase)

#### 🎯 INPUT REQUIS POUR AGENT A
- "Teste particulièrement: [edge case spécifique]"
- "J'ai modifié [service], vérifie les tests existants"
- "Potentiel problème sur [endpoint], à investiguer"

---

**Prêt pour validation Agent A! 🔍**
```

## Template Agent A → Agent B

```markdown
### 🔄 SYNC PROTOCOL V76 — PHASE A[X]
**Statut de l'Intégrité:** Agent A → Agent B
**Date:** [Date]

#### 🧪 TESTS CRÉÉS
- **Tests unitaires:** [Nombre] fichiers, [Nombre] tests
- **Tests E2E:** [Nombre] fichiers, [Nombre] tests
- **Coverage:** Backend [X]%, Frontend [Y]%

#### 🛡️ VIOLATIONS R&D DÉTECTÉES
| Fichier | Ligne | Règle | Description | Sévérité |
|---------|-------|-------|-------------|----------|
| [path] | [line] | #[X] | [description] | 🔴/🟠/🟡 |

#### ✅ VALIDATIONS PASSÉES
- [X] Endpoints testés: [liste]
- [X] Identity boundary vérifié
- [X] Checkpoints fonctionnels
- [X] check_compliance.py: PASS

#### 🔴 ACTIONS CRITIQUES POUR AGENT B
1. **[Action 1]**: [Description] — BLOQUANT
2. **[Action 2]**: [Description] — HAUTE PRIORITÉ

#### 🟡 SUGGESTIONS (Non-bloquantes)
1. [Suggestion 1]
2. [Suggestion 2]

#### 📊 SCORE DE LA PHASE
| Critère | Score | Max |
|---------|-------|-----|
| Endpoints fonctionnels | [X] | [Y] |
| Tests passants | [X] | [Y] |
| R&D Compliance | [X]/7 | 7 |
| **TOTAL** | **[X]%** | 100% |

---

**[Status: GO / RÉCONCILIATION REQUISE]**
```

---

# 4. LE RYTHME DE SPRINT (48h)

## Cycle Standard

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                         CYCLE DE SPRINT 48H                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║  HEURE    │ AGENT B (Exécuteur)          │ AGENT A (Contrôleur)                  ║
║  ─────────┼──────────────────────────────┼───────────────────────────────────── ║
║           │                              │                                       ║
║  00h-04h  │ 📝 DRAFT                     │ 🔧 INFRASTRUCTURE                     ║
║           │ • Intégration brute routers  │ • Prépare fichiers tests vides       ║
║           │ • Premier branchement        │ • Configure mocks                     ║
║           │ • Scan déduplication         │ • Setup fixtures                      ║
║           │                              │                                       ║
║  ─────────┼──────────────────────────────┼───────────────────────────────────── ║
║           │                              │                                       ║
║  04h-12h  │ 🔨 IMPLÉMENTATION            │ 🧪 TESTS UNITAIRES                    ║
║           │ • Connecte pages/services    │ • Code tests sur base du Draft       ║
║           │ • Dependency Injection       │ • Tests négatifs (ce qui DOIT fail)  ║
║           │ • Génère api_map.json        │ • Tests R&D compliance               ║
║           │                              │                                       ║
║  ─────────┼──────────────────────────────┼───────────────────────────────────── ║
║           │                              │                                       ║
║  12h-16h  │ 🔧 AUTO-CORRECTION           │ 🎭 E2E & DOCUMENTATION                ║
║           │ • Répare bugs trouvés par A  │ • Lance Cypress sur code de B        ║
║           │ • Ajuste selon feedback      │ • Met à jour docs API                ║
║           │ • Re-run tests locaux        │ • Screenshots & rapports             ║
║           │                              │                                       ║
║  ─────────┼──────────────────────────────┼───────────────────────────────────── ║
║           │                              │                                       ║
║  16h-20h  │ 📋 SYNC & PUSH               │ ✅ VALIDATION FINALE                  ║
║           │ • Remplit Contrat de Sync    │ • Calcule score de la phase          ║
║           │ • Push code final            │ • Rapport de validation              ║
║           │ • Handshake phase suivante   │ • GO/NO-GO pour suite                ║
║           │                              │                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

## Timeline des 20 Phases

```
SEMAINE 1 (Jours 1-4):
├── Phase A1 + B1 (Sprint 1)
└── Phase A2 + B2 (Sprint 2)

SEMAINE 2 (Jours 5-8):
├── Phase A3 + B3 (Sprint 3)
├── 🔄 CHECKPOINT #1 (Réconciliation)
└── Phase A4 + B4 (Sprint 4)

SEMAINE 3 (Jours 9-12):
├── Phase A5 + B5 (Sprint 5)
├── 🔄 CHECKPOINT #2 (Réconciliation)
└── Phase A6 + B6 (Sprint 6)

SEMAINE 4 (Jours 13-16):
├── Phase A7 + B7 (Sprint 7)
├── 🔄 CHECKPOINT #3 (Réconciliation)
└── Phase A8 + B8 (Sprint 8)

SEMAINE 5 (Jours 17-20):
├── Phase A9 + B9 (Sprint 9)
├── Phase A10 + B10 (Sprint 10)
└── 🔄 CHECKPOINT FINAL (Réconciliation & Score)
```

---

# 5. CHECKPOINTS DE RÉCONCILIATION

## Quand Réconcilier

```
CHECKPOINTS OBLIGATOIRES:
├── Après Phase 5 (A5 + B5 terminées)
├── Après Phase 10 (A10 + B10 terminées)
├── Après Phase 15 (si applicable)
└── FINAL (avant production)

RÉCONCILIATION IMMÉDIATE SI:
├── Test E2E échoue de manière inattendue
├── Violation R&D détectée
├── Score de phase < 70%
└── Blocage technique majeur
```

## Template de Réconciliation

```markdown
### 🔄 RÉCONCILIATION CHECKPOINT #[X]

**Date:** [Date]
**Phases couvertes:** A[X]-A[Y] + B[X]-B[Y]

#### 📊 SCORE CUMULÉ

| Critère | Cible | Actuel | Status |
|---------|-------|--------|--------|
| Endpoints | 350+ | [X] | ✅/⚠️/❌ |
| Pages connectées | 100+ | [X] | ✅/⚠️/❌ |
| Tests E2E | 150+ | [X] | ✅/⚠️/❌ |
| Tests unitaires | 1200+ | [X] | ✅/⚠️/❌ |
| Coverage backend | 85% | [X]% | ✅/⚠️/❌ |
| Coverage frontend | 70% | [X]% | ✅/⚠️/❌ |
| R&D Compliance | 7/7 | [X]/7 | ✅/⚠️/❌ |

**SCORE GLOBAL:** [X]/100 (Cible: 92-95)

#### 🔴 PROBLÈMES À RÉSOUDRE

| # | Problème | Responsable | Priorité | Deadline |
|---|----------|-------------|----------|----------|
| 1 | [Desc] | Agent A/B | P0/P1/P2 | Phase [X] |

#### ✅ DÉCISIONS PRISES

| # | Décision | Raison | Impact |
|---|----------|--------|--------|
| 1 | [Desc] | [Raison] | [Impact] |

#### 🎯 PLAN POUR PHASES SUIVANTES

**Agent A:**
- Focus sur: [X]
- Éviter: [Y]

**Agent B:**
- Focus sur: [X]
- Éviter: [Y]

---

**Validation Jo:** ✅/❌
**Signature:** _______________
**Date:** [Date]
```

---

# 6. TEMPLATES PRÊTS À COPIER

## 6.1 Message Initial pour Agent B

```markdown
# 🚀 DÉMARRAGE PHASE B[X]

Salut Agent B!

## 📋 Context
[Coller le dernier Sync Contract d'Agent A ici]

## 🎯 Ta Mission Cette Phase
[Description de la phase depuis ROADMAP]

## ⚠️ Points d'Attention
- [Point 1 du feedback Agent A]
- [Point 2]

## 📎 Ressources
- api_map.json actuel: [lien/contenu]
- Tests existants: [lien]

---

**Commence par le Handshake!**
```

## 6.2 Message Initial pour Agent A

```markdown
# 🔍 DÉMARRAGE PHASE A[X]

Salut Agent A!

## 📋 Context
[Coller le dernier Sync Contract d'Agent B ici]

## 🎯 Ta Mission Cette Phase
[Description de la phase depuis ROADMAP]

## 🧪 Nouveaux Endpoints à Tester
[Liste depuis api_map.json d'Agent B]

## ⚠️ Points d'Attention d'Agent B
- "[Edge case mentionné par B]"
- "[Service modifié]"

---

**Lance check_compliance.py d'abord!**
```

## 6.3 Message de Réconciliation

```markdown
# 🔄 RÉCONCILIATION REQUISE

**Problème détecté:** [Description]

## 📊 Status Actuel
- Agent A: Phase A[X] terminée
- Agent B: Phase B[X] bloquée

## 🔴 Le Problème
[Description détaillée]

## 💡 Solutions Proposées
1. [Solution 1]
2. [Solution 2]

## 🎯 Action Requise
[Qui doit faire quoi]

---

**Jo, décision requise sur [point spécifique].**
```

---

# 7. PROCÉDURE D'ARRÊT CRITIQUE

## Quand Arrêter

```
🛑 ARRÊT OBLIGATOIRE SI:

1. Violation R&D Rule #1 (Human Sovereignty)
   → Code exécute action sensible SANS checkpoint

2. Violation R&D Rule #3 (Identity Boundary)
   → Code permet accès cross-identity SANS vérification

3. Violation R&D Rule #5 (No Ranking)
   → Algorithme de ranking détecté dans feed

4. Contradiction architecturale majeure
   → Décision qui contredit architecture Canon
```

## Template de Rapport d'Arrêt

```markdown
### 🛑 RAPPORT D'ARRÊT CRITIQUE

**Agent:** [A/B]
**Date/Heure:** [Timestamp]
**Phase en cours:** [X]

#### 🚨 VIOLATION DÉTECTÉE

**Règle violée:** R&D Rule #[X] - [Nom]

**Fichier:** `[path/to/file.py]`
**Ligne:** [X]

**Code problématique:**
```python
[Extrait du code]
```

**Description:**
[Explication de pourquoi c'est une violation]

**Impact potentiel:**
[Ce qui pourrait arriver si non corrigé]

#### ⏸️ STATUS

- ⏸️ Exécution ARRÊTÉE
- ⏳ En attente décision humaine
- 📋 Code non committé

#### 💡 OPTIONS

1. **Option A:** [Description] — Impact: [X]
2. **Option B:** [Description] — Impact: [Y]
3. **Option C:** Annuler et repenser — Impact: [Z]

---

**Jo, décision requise.**
**Ne pas continuer sans validation explicite.**
```

---

# 📊 RÉSUMÉ VISUEL

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║                         SYNC PROTOCOL V76 — RÉSUMÉ                               ║
║                                                                                  ║
║  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐                ║
║  │  AGENT B    │───────▶│     JO      │───────▶│  AGENT A    │                ║
║  │  Exécuteur  │         │ Orchestrateur│        │ Contrôleur  │                ║
║  └─────────────┘         └─────────────┘         └─────────────┘                ║
║        │                       │                       │                        ║
║        │    HANDSHAKE         │                       │                        ║
║        │ ─────────────────────▶ ─────────────────────▶│                        ║
║        │                       │                       │                        ║
║        │                       │    VALIDATION        │                        ║
║        │◀───────────────────── ◀─────────────────────│                        ║
║        │                       │                       │                        ║
║        │    [SPRINT 48H]       │                       │                        ║
║        │    Code + Tests       │                       │                        ║
║        │                       │                       │                        ║
║        │    SYNC CONTRACT     │                       │                        ║
║        │ ─────────────────────▶ ─────────────────────▶│                        ║
║        │                       │                       │                        ║
║        │                       │    VALIDATION        │                        ║
║        │◀───────────────────── ◀─────────────────────│                        ║
║        │                       │                       │                        ║
║        │    [NEXT PHASE...]    │                       │                        ║
║                                                                                  ║
║  CHECKPOINTS: Phases 5, 10, 15, 20                                              ║
║  DURÉE ESTIMÉE: 20-25 jours                                                     ║
║  OBJECTIF: 92-95/100                                                            ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

**Document créé le 8 Janvier 2026**  
**Pour usage exclusif CHE·NU™ V76**

© 2026 CHE·NU™ | GOUVERNANCE > EXÉCUTION
