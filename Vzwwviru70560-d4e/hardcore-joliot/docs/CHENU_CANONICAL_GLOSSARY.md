# CHE·NU™ — CANONICAL GLOSSARY

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            CHE·NU™ — CANONICAL GLOSSARY                                     ║
║                                                                              ║
║                    ⚠️ MANDATORY — NO VARIATION PERMITTED ⚠️                  ║
║                                                                              ║
║                    Version 1.0 | Décembre 2025                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Document ID:** GLO-001  
**Sensitivity Label:** CHE·NU — LEVEL_NDA  
**Authority:** Superior to all other documents

---

## DOCUMENT SCOPE

```
Sensitivity Label: CHE·NU — LEVEL_NDA
Unauthorized extraction voids context.

This document establishes the UNIQUE CANONICAL GLOSSARY of CHE·NU.
It has authority over ALL other documents.
```

---

## 1. STATUT & AUTORITÉ

Ce document établit le **GLOSSAIRE CANONIQUE UNIQUE** de CHE·NU.

**Autorité:**
- Supérieure à tous les autres documents
- S'applique à: tous les PDF, toutes les Spheres, tous les modules, tous les agents (Claude inclus)

**AUCUNE VARIATION TERMINOLOGIQUE N'EST AUTORISÉE**

Si un terme n'existe pas ici → **IL NE DOIT PAS ÊTRE UTILISÉ**

---

## 2. RÈGLES ABSOLUES D'UTILISATION

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  RÈGLES NON NÉGOCIABLES                                                      ║
║                                                                              ║
║  1. UN concept = UN terme = UNE définition                                   ║
║  2. AUCUN synonyme                                                           ║
║  3. AUCUNE reformulation                                                     ║
║  4. AUCUNE traduction libre                                                  ║
║  5. AUCUNE simplification                                                    ║
║  6. En cas de doute → reprendre le terme EXACT                              ║
║  7. Toute création de terme nécessite validation CORE                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. GLOSSAIRE CANONIQUE CHE·NU (VERSION 1.0)

### 🧠 CONCEPTS FONDAMENTAUX

---

#### CHE·NU
```
Définition:
Environnement structuré d'assistance humaine à décision contrôlée, 
fondé sur l'intention, la contextualisation et la validation humaine explicite.

Niveau: PUBLIC (nom) → NDA (définition complète)
```

---

#### Human Authority
```
Définition:
Principe selon lequel toute décision ayant un impact réel doit être 
prise, validée ou refusée par un humain identifiable.

Niveau: NDA
NE PAS utiliser: "Validation humaine", "Contrôle utilisateur", "Human-in-the-loop"
```

---

#### Human Validation Gate
```
Définition:
Point de passage obligatoire empêchant toute action, recommandation 
ou exécution tant qu'une validation humaine explicite n'a pas été fournie.

Niveau: NDA
NE PAS utiliser: "Checkpoint", "Point de validation", "Approbation"
```

---

#### Automation Boundary
```
Définition:
Limite stricte définissant ce que le système peut préparer, suggérer 
ou simuler, sans jamais décider ni exécuter.

Niveau: NDA
NE PAS utiliser: "Limite d'automation", "Restriction AI"
```

---

#### Automation Level
```
Définition:
Classification interne (LEVEL_0 à LEVEL_2 uniquement) indiquant le 
degré maximal d'assistance permis pour un contexte donné.

Valeurs autorisées:
- LEVEL_0: Aucune automation
- LEVEL_1: Suggestions uniquement
- LEVEL_2: Préparation + suggestions (validation requise)

Niveau: CORE
NE PAS utiliser: "Niveau d'automatisation", "Degré AI"
```

---

#### Dormant Module
```
Définition:
Module chargé mais inactif, incapable de produire une action ou une 
suggestion sans déclenchement humain explicite.

Niveau: NDA
NE PAS utiliser: "Module inactif", "Module en veille"
```

---

#### Contextual Profile
```
Définition:
Représentation non réductrice d'un contexte humain, social, professionnel 
ou éthique, servant à restreindre et orienter l'assistance.

Niveau: NDA
NE PAS utiliser: "Profil utilisateur", "Contexte", "Persona"
```

---

#### Non-Autosufficiency Principle
```
Définition:
Principe selon lequel aucun document, module ou interface ne doit 
permettre à lui seul une compréhension complète du système.

Niveau: NDA
NE PAS utiliser: "Compartimentage", "Fragmentation"
```

---

#### Zone of Agent Freedom
```
Définition:
Espace isolé où un agent peut exécuter des simulations, préparations 
ou analyses, sans que les résultats soient injectés dans les données 
utilisateur avant validation humaine.

Niveau: CORE
NE PAS utiliser: "Sandbox", "Espace de test", "Environnement isolé"
```

---

#### Isolated Execution Result
```
Définition:
Résultat produit dans une Zone of Agent Freedom, conservé séparément 
et non appliqué tant qu'il n'est pas validé.

Niveau: CORE
NE PAS utiliser: "Résultat en attente", "Draft"
```

---

#### Sensitive Context
```
Définition:
Contexte présentant un risque social, légal, émotionnel ou irréversible, 
imposant des restrictions supplémentaires d'assistance.

Niveau: NDA
NE PAS utiliser: "Contexte sensible", "Situation à risque"
```

---

#### Irreversible Risk
```
Définition:
Situation dans laquelle une erreur, même minime, ne peut être corrigée 
après exécution.

Niveau: NDA
NE PAS utiliser: "Risque irréversible", "Action définitive"
```

---

#### Documentation Index Map
```
Définition:
Document maître listant l'ensemble des documents CHE·NU, leur niveau 
de sensibilité et leurs relations.

Niveau: PUBLIC (existence) → NDA (contenu)
Référence: IDX-001
```

---

#### Sensitivity Label
```
Définition:
Marqueur interne indiquant le niveau de diffusion autorisé d'un 
document ou d'une section.

Valeurs autorisées:
- [CHE·NU — LEVEL_PUBLIC]
- [CHE·NU — LEVEL_PARTNER]
- [CHE·NU — LEVEL_NDA]
- [CHE·NU — LEVEL_CORE]

Niveau: PUBLIC
AUCUN AUTRE LABEL N'EST AUTORISÉ
```

---

#### Governance Before Execution
```
Définition:
Loi fondamentale stipulant que toute structure, règle ou validation 
doit exister avant toute action.

Niveau: PUBLIC (concept) → NDA (application)
NE PAS utiliser: "Gouvernance d'abord", "Règles avant action"
```

---

### 🏛️ TERMES ARCHITECTURAUX

---

#### Sphere
```
Définition:
Domaine de vie isolé (9 au total) avec agents et fonctionnalités dédiés.

Liste officielle:
1. Personal
2. Business
3. Government
4. Creative Studio
5. Community
6. Social
7. Entertainment
8. My Team
9. Scholar

Niveau: PUBLIC (liste) → NDA (détails)
NE PAS utiliser: "Sphère", "Domaine", "Section"
```

---

#### Nova
```
Définition:
Intelligence système centrale, toujours présente, jamais "hired".

Niveau: PUBLIC (existence) → NDA (capacités)
NE PAS utiliser: "Assistant principal", "AI centrale"
```

---

#### Agent
```
Définition:
Entité AI spécialisée avec identité, capacités, coûts et scope définis.

Niveau: PUBLIC (concept) → NDA (mécaniques)
NE PAS utiliser: "Bot", "Assistant virtuel", "AI helper"
```

---

#### Thread
```
Définition:
Objet conversationnel natif CHE·NU au format .chenu

Niveau: PUBLIC → NDA
NE PAS utiliser: "Conversation", "Fil", "Discussion"
```

---

#### Token
```
Définition:
Unité de crédit interne pour mesurer les coûts AI.

⚠️ IMPORTANT: Token n'est PAS une crypto-monnaie, n'est PAS tradeable

Niveau: PUBLIC (concept) → NDA (mécaniques)
NE PAS utiliser: "Crédit", "Point", "Monnaie"
```

---

#### Encoding Layer
```
Définition:
Couche de transformation appliquée avant et après exécution AI.

Niveau: NDA
NE PAS utiliser: "Couche de transformation", "Middleware"
```

---

#### Module Registry
```
Définition:
Registre officiel de tous les modules CHE·NU avec leur status.

Niveau: NDA
NE PAS utiliser: "Liste des modules", "Catalogue"
```

---

### ⚖️ RÈGLES R&D (LES 7 RÈGLES)

---

#### Human Sovereignty (R&D Rule #1)
```
Définition:
Aucune action n'affecte la production sans approbation humaine explicite.

Niveau: NDA
Lié à: Human Authority, Human Validation Gate
```

---

#### Autonomy Isolation (R&D Rule #2)
```
Définition:
L'AI opère exclusivement en sandbox, jamais en production directe.

Niveau: NDA
Lié à: Zone of Agent Freedom
```

---

#### Sphere Integrity (R&D Rule #3)
```
Définition:
Les transferts Cross-Sphere requièrent des workflows explicites.

Niveau: NDA
```

---

#### My Team Restrictions (R&D Rule #4)
```
Définition:
Interdiction d'orchestration AI→AI automatique.

Niveau: NDA
```

---

#### Social Restrictions (R&D Rule #5)
```
Définition:
Interdiction des algorithmes de ranking et bots d'engagement.

Niveau: NDA
```

---

#### Module Traceability (R&D Rule #6)
```
Définition:
Tous les objets ont created_by, created_at, id obligatoires.

Niveau: NDA
```

---

#### R&D Continuity (R&D Rule #7)
```
Définition:
Cohérence des décisions et documentation obligatoire.

Niveau: NDA
```

---

## 4. LABELS INTERNES DE SENSIBILITÉ

### LABELS OFFICIELS (SEULS AUTORISÉS)

```
[CHE·NU — LEVEL_PUBLIC]
[CHE·NU — LEVEL_PARTNER]
[CHE·NU — LEVEL_NDA]
[CHE·NU — LEVEL_CORE]
```

**AUCUN AUTRE LABEL N'EST AUTORISÉ**

### EMPLACEMENTS OBLIGATOIRES DANS LES PDF

```
📌 Page de couverture (discret)
📌 Pied de page (toutes les pages)
📌 Section "Document Scope"
```

### FORMAT CANONIQUE — PIED DE PAGE

```
[CHE·NU — LEVEL_NDA] — This document is not self-sufficient.
```

### FORMAT CANONIQUE — SECTION SCOPE

```
Sensitivity Label: CHE·NU — LEVEL_NDA
Unauthorized extraction voids context.
```

### FORMAT CANONIQUE — SECTIONS MIXTES

```
────────────────────────────────────
SECTION SENSITIVITY:
[CHE·NU — LEVEL_CORE]
This section must not be extracted,
summarized, or redistributed.
────────────────────────────────────
```

---

## 5. TERMES INTERDITS

| Terme Interdit | Remplacer Par |
|----------------|---------------|
| Gouvernance | Governance Before Execution |
| Sphère | Sphere |
| Validation humaine | Human Authority / Human Validation Gate |
| Bot | Agent |
| Sandbox | Zone of Agent Freedom |
| Contexte sensible | Sensitive Context |
| Limite d'automation | Automation Boundary |
| Niveau d'automatisation | Automation Level |
| Module inactif | Dormant Module |
| Résultat en attente | Isolated Execution Result |
| Profil utilisateur | Contextual Profile |
| Compartimentage | Non-Autosufficiency Principle |

---

## 6. RÈGLES DE MODIFICATION

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  RÈGLES ABSOLUES                                                             ║
║                                                                              ║
║  - Toute modification terminologique → vérifier ce glossaire                 ║
║  - Tout nouveau terme → REFUSÉ par défaut                                   ║
║  - Toute section sans label → NON CONFORME                                  ║
║  - Tout document sans Scope explicite → NON CONFORME                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 7. CLAUSE DE VERROUILLAGE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  À PARTIR DE CE MOMENT:                                                      ║
║                                                                              ║
║  - Le glossaire est FIGÉ                                                     ║
║  - Toute dérivation est INTERDITE                                           ║
║  - Toute ambiguïté est une ERREUR                                           ║
║  - Toute simplification est un RISQUE                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## TERMINOLOGY AUTHORITY

```
Ce document est la SOURCE DE VÉRITÉ terminologique unique.

Tous les autres documents CHE·NU DOIVENT référencer ce glossaire.

Document ID: GLO-001
Version: 1.0
Status: LOCKED
Effective: 23 Décembre 2025
```

---

```
[CHE·NU — LEVEL_NDA] — This document is not self-sufficient.
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    TERMINOLOGY LOCKED — INTERPRETATION RESTRICTED                            ║
║                                                                              ║
║    CHE·NU™ — HUMAN AUTHORITY IS NOT NEGOTIABLE                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
