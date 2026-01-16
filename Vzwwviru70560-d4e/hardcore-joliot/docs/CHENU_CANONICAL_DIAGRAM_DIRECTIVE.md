# CHE·NU™ — CANONICAL DIAGRAM DIRECTIVE v1.0

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              CHE·NU™ — CANONICAL DIAGRAM DIRECTIVE v1.0                      ║
║                                                                              ║
║          GOVERNANCE • CLARITY • NON-REPLICABILITY                            ║
║                                                                              ║
║      ⚠️ CANONICAL — COPY AS-IS — NO INTERPRETATION ⚠️                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## DOCUMENT SCOPE

```
Sensitivity Label: CHE·NU — LEVEL_NDA
Unauthorized extraction voids context.

This document defines the Canonical Diagram Directive for ALL CHE·NU visual content.
It is not self-sufficient.
```

---

## TERMINOLOGY AUTHORITY

```
All terminology in this document follows the CHE·NU Canonical Glossary (GLO-001).
No variation permitted. No synonyms allowed.
Reference: CHE·NU™ — Canonical Glossary v1.0
```

---

**Document ID:** CDD-001  
**Sensitivity Label:** CHE·NU — LEVEL_NDA  
**Authority:** Mandatory for ALL diagrams

---

## OBJECTIF GLOBAL

Les diagrammes CHE·NU servent à:
- **EXPLIQUER** le système sans révéler son implémentation
- **ÉDUQUER** sans exposer la logique interne exploitable
- **ALIGNER** humains, agents et documentation
- **PROTÉGER** la philosophie: Humans > Automation

Les diagrammes **NE servent PAS à:**
- Décrire le code
- Montrer les APIs internes
- Détailler les flux exécutables
- Permettre la reproduction du système

---

## I. TYPES DE DIAGRAMMES AUTORISÉS (LISTE FERMÉE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  SEULS les 6 types suivants sont autorisés.                                  ║
║  TOUT AUTRE DIAGRAMME EST INTERDIT                                           ║
║  (sauf annexe interne NDA explicite).                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 1. SYSTEM MAP (Vue haute)

```
Contenu autorisé:
- Montre les sphères CHE·NU
- Aucune API
- Aucune logique interne
- Aucune flèche conditionnelle

Usage: Compréhension globale
```

### 2. LAYERED GOVERNANCE DIAGRAM

```
Contenu autorisé:
- Couches verticales
- Met l'humain AU-DESSUS du système

Usage: Philosophie & sécurité
```

### 3. HUMAN VALIDATION GATE

```
Contenu autorisé:
- Barrière explicite
- Rien ne passe sans validation

Usage: Règle non négociable (Human Authority)
```

### 4. AGENT FREEDOM ZONE (Sandbox)

```
Contenu autorisé:
- Zone isolée
- Exécution parallèle autorisée
- Résultats stockés hors données utilisateur

Usage: Expliquer l'autonomie contrôlée
```

### 5. INTER-SPHERE WORKFLOW (EXEMPLE UNIQUE)

```
Contenu autorisé:
- Un seul scénario simple
- Pas de cascade complexe

Usage: Démonstration pédagogique
```

### 6. DOCUMENT SENSITIVITY LEVELS

```
Contenu autorisé:
- Classification documentaire (Sensitivity Labels)
- Pas de contenu technique

Usage: Gouvernance & diffusion
```

---

## II. LANGAGE VISUEL CANONIQUE (OBLIGATOIRE)

### FORMES (sens unique, jamais décoratif)

| Forme | Signification |
|-------|---------------|
| Cercle | Sphère |
| Rectangle | Module |
| Rectangle arrondi | Agent |
| Ligne pleine | Flux autorisé |
| Ligne pointillée | Suggestion / Préparation |
| Ligne rouge | Interdit |
| Barrière verticale | Validation humaine |

### COULEURS

```
Fond:           Blanc ou gris très clair
Traits:         Gris foncé
Accent unique:  Bleu OU vert (un seul)
Rouge:          UNIQUEMENT pour interdiction
```

### INTERDICTIONS VISUELLES

```
❌ Pas d'ombres
❌ Pas de dégradés
❌ Pas d'icônes décoratives
❌ Pas de flèches multiples sans hiérarchie
❌ Pas de "tout connecté à tout"
```

### RÈGLE ABSOLUE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  Une forme = un sens.                                                        ║
║  Si une forme n'a pas de sens → elle n'existe pas.                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## III. STRUCTURE DE DOSSIERS (OÙ CRÉER)

Tous les diagrammes doivent être créés dans:

```
/docs/diagrams/
├── canonical/
│   ├── system_map.png
│   ├── layered_governance.png
│   ├── human_validation_gate.png
│   ├── agent_freedom_zone.png
│   ├── inter_sphere_example.png
│   └── document_sensitivity_levels.png
│
├── source/
│   ├── system_map.drawio
│   ├── governance.drawio
│   └── workflows.drawio
│
└── README.md
    - décrit le rôle de chaque diagramme
    - interdit toute modification non validée
```

```
⚠️ Les fichiers "source/" ne sont JAMAIS diffusés hors NDA.
```

---

## IV. INTÉGRATION DANS LES PDF

### RÈGLE GÉNÉRALE

```
Un diagramme = un message.
Jamais plus d'un diagramme par section clé.
```

### INTÉGRATION PAR DOCUMENT

| Document | Diagrammes Autorisés |
|----------|---------------------|
| **PDF INDEX (PUBLIC)** | system_map, document_sensitivity_levels |
| **INVESTOR PDF (PARTNER)** | system_map, layered_governance, human_validation_gate (version simplifiée) |
| **USER GUIDE (PUBLIC)** | inter_sphere_example, human_validation_gate (pédagogique) |
| **SYSTEM MANUAL (NDA)** | Tous les 6 diagrammes (aucun diagramme supplémentaire) |

---

## V. TEST DE SÉCURITÉ AVANT ACCEPTATION

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  Avant de valider un diagramme, poser ces 3 questions:                       ║
║                                                                              ║
║  1. Un ingénieur externe pourrait-il reproduire CHE·NU                       ║
║     à partir de ce diagramme?                                                ║
║     → OUI = REFUS                                                            ║
║                                                                              ║
║  2. Le diagramme montre-t-il COMMENT le système agit                         ║
║     au lieu de POURQUOI?                                                     ║
║     → OUI = REFUS                                                            ║
║                                                                              ║
║  3. Le diagramme respecte-t-il Humans > Automation?                          ║
║     → NON = REFUS                                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## VI. RÈGLE FINALE (NON NÉGOCIABLE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  Si un diagramme semble "trop intelligent", "trop complet",                  ║
║  ou "trop impressionnant":                                                   ║
║                                                                              ║
║                         IL EST MAUVAIS.                                      ║
║                                                                              ║
║  CHE·NU privilégie:                                                          ║
║  • la clarté                                                                 ║
║  • la lenteur                                                                ║
║  • la gouvernance                                                            ║
║  • la compréhension humaine                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## VII. CHECKLIST VALIDATION DIAGRAMME

```
DIAGRAM_COMPLIANCE_CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

TYPE & AUTORISATION
────────────────────────────────────────────────────────────────────────────────
□ DIA_01 — Type de diagramme dans liste des 6 autorisés
□ DIA_02 — Aucun type non autorisé utilisé

LANGAGE VISUEL
────────────────────────────────────────────────────────────────────────────────
□ DIA_03 — Formes utilisées avec sens canonique uniquement
□ DIA_04 — Couleurs conformes (blanc/gris + 1 accent + rouge interdit)
□ DIA_05 — Aucune ombre, dégradé, icône décorative

SÉCURITÉ
────────────────────────────────────────────────────────────────────────────────
□ DIA_06 — Non-reproductibilité vérifiée (test question 1)
□ DIA_07 — Montre POURQUOI pas COMMENT (test question 2)
□ DIA_08 — Humans > Automation (test question 3)

INTÉGRATION
────────────────────────────────────────────────────────────────────────────────
□ DIA_09 — Placé dans /docs/diagrams/canonical/
□ DIA_10 — Source dans /docs/diagrams/source/ (NDA)
□ DIA_11 — Documenté dans README.md
□ DIA_12 — Un seul diagramme par section clé

═══════════════════════════════════════════════════════════════════════════════

⚠️ Si une seule case est FALSE → DIAGRAMME = NON CONFORME
```

---

```
[CHE·NU — LEVEL_NDA] — This document is not self-sufficient.
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   CHE·NU™ — GOVERNANCE BEFORE EXECUTION                                      ║
║   HUMANS BEFORE AUTOMATION                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
