# CHE·NU™ — DOCUMENTATION INDEX & SENSITIVITY MAP

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            CHE·NU™ DOCUMENTATION INDEX & SENSITIVITY MAP                    ║
║                                                                              ║
║                    Version 1.1 | Décembre 2025                              ║
║                                                                              ║
║         "La compréhension est un cheminement, pas une destination"          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## DOCUMENT SCOPE

```
Sensitivity Label: CHE·NU — LEVEL_PUBLIC
Unauthorized extraction voids context.

This document is the official map of all CHE·NU documentation.
Structure is visible, sensitive content is referenced only.
```

---

## TERMINOLOGY AUTHORITY

```
All terminology in this document follows the CHE·NU Canonical Glossary (GLO-001).
No variation permitted. No synonyms allowed.
Reference: CHE·NU™ — Canonical Glossary v1.0
```

---

## 📋 À PROPOS DE CE DOCUMENT

Ce document est la **carte officielle** de toute la documentation CHE·NU.

**Rôle:**
- Liste TOUS les documents existants
- Indique leur niveau de sensibilité
- Précise les conditions d'accès
- Définit ce qui est volontairement non documenté
- Sert de référence unique pour l'organisation documentaire

**⚠️ RÈGLE:** Toujours consulter ce document avant de produire ou modifier toute documentation.

---

## ⛔ RÈGLE DE NON-DÉRIVATION

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  AUCUN document PUBLIC ou PARTNER ne peut être dérivé directement           ║
║  du SYSTEM MANUAL sans filtrage explicite et validation.                    ║
║                                                                              ║
║  Processus obligatoire:                                                      ║
║  1. Identifier le contenu source (NDA)                                       ║
║  2. Appliquer filtrage par niveau de sensibilité                            ║
║  3. Remplacer termes NDA par termes PUBLIC (via Glossaire)                  ║
║  4. Valider absence de fuite conceptuelle                                    ║
║  5. Ajouter section "Ce document omet délibérément..."                      ║
║  6. Validation humaine obligatoire                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 📖 DOCUMENTS DE RÉFÉRENCE OBLIGATOIRES

| ID | Document | Rôle |
|----|----------|------|
| GLO-001 | CHE·NU™ Canonical Glossary | Terminologie officielle verrouillée |
| RUL-001 | CHE·NU™ Documentation Usage Rules | Règles de production/usage |
| IDX-001 | Ce document | Carte de la documentation |

**⚠️ TOUS les documents doivent référencer le Glossaire Canonique (GLO-001)**

---

## 🔐 LABELS DE SENSIBILITÉ

### 🔓 LEVEL_PUBLIC
```
Accès: Libre
Contenu autorisé:
  ✓ Pédagogique et descriptif
  ✓ Présentation générale
  ✓ Comment utiliser (utilisateur)
  
Contenu INTERDIT:
  ✗ Mécaniques internes
  ✗ Règles système
  ✗ Logique d'automation
```

### 🟡 LEVEL_PARTNER
```
Accès: Partenaires, investisseurs, démos encadrées
Contenu autorisé:
  ✓ Vision produit
  ✓ Différenciation
  ✓ Cas d'usage agrégés
  ✓ Roadmap haute altitude
  
Contenu INTERDIT:
  ✗ Détails d'implémentation
  ✗ Validation humaine interne
  ✗ Niveaux d'automation précis
  ✗ Règles R&D
  ✗ Modules sensibles
```

### 🔐 LEVEL_NDA
```
Accès: NDA requis
Contenu autorisé:
  ✓ Philosophie complète
  ✓ Architecture conceptuelle
  ✓ Sphères & inter-sphères
  ✓ Principes de validation humaine
  ✓ Méthodologie R&D
  ✓ Profils utilisateurs (abstraits)
  ✓ Principes de sécurité
  
Contenu INTERDIT:
  ✗ Code exploitable
  ✗ Instructions opérationnelles sensibles
  ✗ Bypass ou raccourcis
```

### 🔴 LEVEL_CORE
```
Accès: Fondateur uniquement
Contenu:
  • Règles internes non négociables
  • Lois d'automation
  • Zones de liberté isolées
  • Séparation résultats / données utilisateur
  • Mécanismes de neutralité
  • Anti-duplication
  • Audits
  • Lint R&D
  • Design philosophique profond

⚠️ Ce niveau n'est JAMAIS résumé ailleurs.
```

---

## 📚 CATALOGUE DES DOCUMENTS

### NIVEAU 0: INDEX & GOUVERNANCE

| ID | Document | Sensibilité | Status | Pages |
|----|----------|-------------|--------|-------|
| IDX-001 | CHE·NU™ Documentation Index & Sensitivity Map | 🔓 PUBLIC | ✅ Actif | ~10 |
| GLO-001 | CHE·NU™ Canonical Glossary | 🔐 NDA | ✅ Actif | ~15 |
| RUL-001 | CHE·NU™ Documentation Usage Rules | 🔐 NDA | ✅ Actif | ~6 |
| DCS-001 | CHE·NU™ Documentary Compliance System | 🔐 NDA | ✅ Actif | ~8 |
| CDD-001 | CHE·NU™ Canonical Diagram Directive | 🔐 NDA | ✅ Actif | ~6 |
| FDT-001 | CHE·NU™ Figma Canonical Diagram Template | 🔐 NDA | ✅ Actif | ~8 |
| QUP-001 | CHE·NU™ Quantum Usage Policy | 🔐 NDA | ✅ Actif | ~10 |
| SQR-001 | CHE·NU™ Scholar Quantum Roadmap | 🔐 NDA | ✅ Actif | ~15 |

---

### NIVEAU 1: USER GUIDE

| ID | Document | Sensibilité | Status | Pages | Couvre | Ne couvre PAS |
|----|----------|-------------|--------|-------|--------|---------------|
| USR-001 | CHE·NU™ User Guide | 🔓 PUBLIC | 🔄 En cours | ~60-70 | Comment utiliser, Navigation, Features utilisateur, Nova (visible) | Architecture interne, Règles R&D, Mécaniques d'agents |

---

### NIVEAU 2: PARTNER/INVESTOR

| ID | Document | Sensibilité | Status | Pages | Couvre | Ne couvre PAS |
|----|----------|-------------|--------|-------|--------|---------------|
| INV-001 | CHE·NU™ Product & Vision Overview | 🟡 PARTNER | 🔄 En cours | ~40-50 | Vision, Marché, Différenciation, Roadmap | Implémentation, Règles internes, Validation humaine détaillée |

---

### NIVEAU 3: SYSTEM MANUAL (NDA)

| ID | Document | Sensibilité | Status | Pages | Couvre | Ne couvre PAS |
|----|----------|-------------|--------|-------|--------|---------------|
| SYS-001 | CHE·NU™ System Manual | 🔐 NDA | 🔄 En cours | ~110 | Philosophie, Architecture, Sphères, Agents, Gouvernance, Technique | Code source, Secrets opérationnels |

---

### NIVEAU 4: DOCUMENTS SPÉCIALISÉS

| ID | Document | Sensibilité | Status | Pages | Couvre |
|----|----------|-------------|--------|-------|--------|
| SPE-001 | Ethics & Human Authority | 🔐 NDA | 📋 Planifié | ~20 | Éthique AI, Souveraineté humaine |
| SPE-002 | Automation Boundaries | 🔴 CORE | 📋 Planifié | ~15 | Limites d'automation, Zones interdites |
| SPE-003 | Relational & Social Safety | 🔐 NDA | 📋 Planifié | ~15 | Sécurité sociale, Relations |
| SPE-004 | Start-a-Business Framework | 🔐 NDA | 📋 Planifié | ~20 | Entrepreneuriat, LNIS |
| SPE-005 | Scholar & Knowledge Commons | 🔐 NDA | 📋 Planifié | ~15 | Recherche, Savoir partagé |
| SPE-006 | XR & Spatial Design | 🟡 PARTNER | 📋 Planifié | ~20 | Vision XR, Interfaces spatiales |
| SPE-007 | Agent Security Framework | 🔴 CORE | 📋 Planifié | ~25 | Sécurité agents, Règles R&D |
| SPE-008 | Module Registry & Integration | 🔐 NDA | 📋 Planifié | ~30 | Registre modules, Processus |

---

## 🔗 MATRICE DE DÉPENDANCES

```
                    LECTURE REQUISE POUR COMPRENDRE
                    ================================

USER GUIDE (PUBLIC)
    └── Standalone (peut être lu seul)

INVESTOR OVERVIEW (PARTNER)
    └── Standalone (peut être lu seul)

SYSTEM MANUAL (NDA)
    ├── Requiert: Compréhension USER GUIDE
    └── Complète: INVESTOR OVERVIEW

DOCUMENTS SPÉCIALISÉS (NDA/CORE)
    ├── Requiert: SYSTEM MANUAL
    └── Se référencent entre eux selon sujet
```

---

## 🚫 CE QUI N'EST VOLONTAIREMENT PAS DOCUMENTÉ

| Sujet | Raison | Niveau requis pour discussion |
|-------|--------|-------------------------------|
| Secrets cryptographiques | Sécurité | CORE uniquement, oral |
| Bypass de validation | Sécurité | Jamais documenté |
| Clés API / Credentials | Sécurité | Vault séparé |
| Vulnérabilités connues | Sécurité | CORE, oral |
| Stratégies anti-concurrence | Business | CORE |
| Détails pricing exacts | Business | Non finalisé |
| Roadmap détaillée < 6 mois | Stratégique | CORE |

---

## 📐 RÈGLES DE PRODUCTION DOCUMENTAIRE

### AVANT de créer un document:
```
□ Consulter cet INDEX
□ Vérifier qu'il n'existe pas déjà
□ Déterminer le niveau de sensibilité
□ Définir ce qui sera couvert
□ Définir ce qui NE sera PAS couvert
```

### PENDANT la rédaction:
```
□ Ne jamais mélanger deux niveaux de sensibilité
□ Ne jamais rendre un document auto-suffisant
□ Ne jamais exposer une mécanique sans nécessité
□ En cas de doute → classer PLUS sensible
```

### APRÈS la création:
```
□ Ajouter le document à cet INDEX
□ Indiquer les références croisées
□ Valider avec le niveau d'autorisation approprié
```

---

## 📊 STATISTIQUES DOCUMENTATION

| Niveau | Documents | Pages Total | Status |
|--------|-----------|-------------|--------|
| 🔓 PUBLIC | 2 | ~70-80 | En cours |
| 🟡 PARTNER | 2 | ~60-70 | En cours |
| 🔐 NDA | 12 | ~320-350 | En cours |
| 🔴 CORE | 2 | ~40 | Planifié |
| **TOTAL** | **18** | **~490-540** | |

---

## ⚠️ RISQUES DE MAUVAISE INTERPRÉTATION

### Avertissement Officiel

```
CHE·NU n'est pas vulnérable à la copie.
Il est vulnérable à la mauvaise interprétation.
La documentation est donc une barrière active, pas un manuel.
```

### Risques Identifiés

| Risque | Description | Mitigation |
|--------|-------------|------------|
| Reconstruction logique | Recouper plusieurs docs pour comprendre CORE | Compartimentage strict |
| Dérivation sémantique | Créer synonymes pour déduire sens | Glossaire verrouillé (GLO-001) |
| Simplification excessive | Perdre nuances critiques | Sections "Ne Couvre Pas" |
| Copie partielle | Extraire hors contexte | Labels de sensibilité internes |
| Interprétation littérale | Appliquer sans comprendre | Formation requise |

### Interdiction de Reconstruction

```
⚠️ Il est INTERDIT de:
- Compiler des extraits de plusieurs documents
- Tenter de reconstruire la logique CORE
- Créer des "synthèses" non autorisées
- Partager des déductions personnelles

Toute tentative de reconstruction = violation de NDA
```

---

## 🔄 HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0 | 23 Dec 2025 | Création initiale |
| 1.1 | 23 Dec 2025 | Ajout règle No Derivation, Glossaire, Usage Rules, Risques |

---

## ✅ VALIDATION

```
Document: CHE·NU™ Documentation Index & Sensitivity Map
Version: 1.1
Créé: 23 Décembre 2025
Niveau: 🔓 PUBLIC (la structure est visible, pas le contenu sensible)
Validé par: Jo (Fondateur)

Ce document est la référence unique pour l'organisation documentaire CHE·NU.
```

---

```
[CHE·NU — LEVEL_PUBLIC] — This document is not self-sufficient.
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    GOVERNANCE BEFORE EXECUTION                               ║
║                HUMAN AUTHORITY IS NOT NEGOTIABLE                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
