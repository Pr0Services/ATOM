# CHE·NU™ — DOCUMENTATION USAGE RULES

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            CHE·NU™ — DOCUMENTATION USAGE RULES                              ║
║                                                                              ║
║                    ⚠️ MANDATORY — NO VARIATION PERMITTED ⚠️                  ║
║                                                                              ║
║                    Version 1.0 | Décembre 2025                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## DOCUMENT SCOPE

```
Sensitivity Label: CHE·NU — LEVEL_NDA
Unauthorized extraction voids context.

This document defines production and usage rules for ALL CHE·NU documentation.
```

---

## TERMINOLOGY AUTHORITY

```
All terminology in this document follows the CHE·NU Canonical Glossary (GLO-001).
No variation permitted. No synonyms allowed.
Reference: CHE·NU™ — Canonical Glossary v1.0
```

---

**Document ID:** RUL-001  
**Sensitivity Label:** CHE·NU — LEVEL_NDA  
**Référence:** CHE·NU™ Documentation Index (IDX-001)

---

## ⚠️ STATEMENT OFFICIEL

```
CHE·NU n'est pas vulnérable à la copie.
Il est vulnérable à la mauvaise interprétation.
La documentation est donc une barrière active, pas un manuel.
```

---

## 1. RÈGLES DE NON-DÉRIVATION

### 1.1 Règle Fondamentale

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  AUCUN document PUBLIC ou PARTNER ne peut être dérivé directement           ║
║  du SYSTEM MANUAL sans filtrage explicite et validation.                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 1.2 Processus de Dérivation Autorisé

```
SYSTEM MANUAL (🔐 NDA)
        │
        ▼
┌───────────────────────────────────────┐
│   FILTRAGE OBLIGATOIRE                │
│   ────────────────────                │
│   □ Vérifier niveau sensibilité       │
│   □ Supprimer termes NDA/CORE         │
│   □ Remplacer par termes PUBLIC       │
│   □ Valider avec Glossaire            │
│   □ Ajouter "Deliberately Omits"      │
│   □ Validation humaine                │
└───────────────────────────────────────┘
        │
        ▼
INVESTOR OVERVIEW (🟡 PARTNER)
ou
USER GUIDE (🔓 PUBLIC)
```

### 1.3 Interdit de Dérivation Directe

**NE JAMAIS:**
- Copier-coller du System Manual vers documents publics
- "Simplifier" un paragraphe NDA pour le rendre PUBLIC
- Résumer une section CORE dans un document NDA
- Créer des "versions allégées" sans filtrage formel

---

## 2. RÈGLES TERMINOLOGIQUES

### 2.1 Glossaire Canonique Obligatoire

```
RÈGLE: Tous les documents DOIVENT utiliser les termes EXACTS
       du Glossaire Canonique (GLO-001).
       
AUCUNE variation terminologique n'est autorisée.
```

### 2.2 Interdiction de Synonymes

| Action | Status |
|--------|--------|
| Créer un synonyme | ❌ INTERDIT |
| Reformuler un concept sensible | ❌ INTERDIT |
| Traduire un terme canonique | ❌ INTERDIT (sauf exception) |
| Utiliser un terme non listé | ❌ INTERDIT |

### 2.3 Exceptions Linguistiques

```
Exception: Contexte 100% français pour audience francophone non-technique

Dans ce cas:
- Utiliser le terme canonique EN PREMIER
- Suivi de la traduction entre parenthèses
- Exemple: "Governance (gouvernance)"

MAIS:
- Pour termes techniques: PAS de traduction
- "Human Sovereignty" reste "Human Sovereignty"
- "Encoding Layer" reste "Encoding Layer"
```

---

## 3. RÈGLES DE CONTENU

### 3.1 Section Obligatoire: "Ce Document Ne Couvre Pas"

**CHAQUE document doit contenir:**

```markdown
## Ce Que Ce Document Ne Couvre Pas

Ce document omet délibérément:
- [Liste explicite des sujets non couverts]
- [Raison de l'omission si approprié]
- [Référence au document approprié si existe]
```

### 3.2 Distinction "Quoi" vs "Comment"

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  🔓 PUBLIC peut expliquer:    QUOI (ce que ça fait)           ║
║  🟡 PARTNER peut expliquer:   QUOI + POURQUOI (valeur)        ║
║  🔐 NDA peut expliquer:       QUOI + POURQUOI + COMMENT       ║
║  🔴 CORE:                     Mécanismes profonds             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**INTERDIT:** Expliquer "comment" à un niveau qui ne devrait voir que "quoi"

### 3.3 Avertissement de Contexte

Chaque page/section sensible doit inclure:

```
[CHE·NU — LEVEL_XXX]
[Extracting this section voids context]
```

---

## 4. RISQUES DE MAUVAISE INTERPRÉTATION

### 4.1 Risques Identifiés

| Risque | Description | Mitigation |
|--------|-------------|------------|
| Reconstruction logique | Recouper plusieurs docs pour comprendre CORE | Compartimentage strict |
| Dérivation sémantique | Créer synonymes pour déduire sens | Glossaire verrouillé |
| Simplification excessive | Perdre nuances critiques | Sections "Ne Couvre Pas" |
| Copie partielle | Extraire hors contexte | Labels de sensibilité |
| Interprétation littérale | Appliquer sans comprendre | Formation requise |

### 4.2 Reconstruction Logique Interdite

```
⚠️ AVERTISSEMENT

Il est INTERDIT de:
- Compiler des extraits de plusieurs documents
- Tenter de reconstruire la logique CORE
- Créer des "synthèses" non autorisées
- Partager des déductions personnelles

Toute tentative de reconstruction = violation de NDA
```

---

## 5. RÈGLES POUR PRODUCTEURS DE DOCUMENTATION

### 5.1 Avant de Créer un Document

```markdown
CHECKLIST PRE-CRÉATION

□ Consulter l'INDEX (IDX-001)
□ Vérifier qu'il n'existe pas déjà
□ Déterminer le niveau de sensibilité
□ Définir ce qui sera couvert
□ Définir ce qui NE sera PAS couvert
□ Vérifier le Glossaire Canonique
□ Préparer le filtrage si dérivation
```

### 5.2 Pendant la Rédaction

```markdown
RÈGLES DE RÉDACTION

□ Utiliser UNIQUEMENT les termes du Glossaire
□ Ne jamais mélanger deux niveaux de sensibilité
□ Ne jamais rendre un document auto-suffisant
□ Ne jamais exposer une mécanique sans nécessité
□ En cas de doute → classer PLUS sensible
□ Ajouter labels de sensibilité
□ Ajouter section "Ne Couvre Pas"
```

### 5.3 Après la Création

```markdown
CHECKLIST POST-CRÉATION

□ Relire avec Glossaire en main
□ Vérifier aucun terme interdit
□ Valider niveau de sensibilité correct
□ Ajouter au INDEX (IDX-001)
□ Indiquer références croisées
□ Obtenir validation appropriée
□ Archiver version source
```

---

## 6. RÈGLES POUR CLAUDE (AI)

### 6.1 Règles Absolues

```
LORS DE LA PRODUCTION DE DOCUMENTATION CHE·NU:

1. INTERDICTION de reformuler un concept sensible
2. INTERDICTION de créer des synonymes non validés
3. OBLIGATION d'utiliser les termes EXACTS du Glossaire
4. OBLIGATION de déclarer ce qui est couvert ET ce qui est absent
5. INTERDICTION de produire un document qui explique "comment"
   à un niveau qui ne devrait voir que le "quoi"
6. OBLIGATION de vérifier l'INDEX avant toute création
7. OBLIGATION d'ajouter les labels de sensibilité
8. INTERDICTION de dériver directement sans filtrage
```

### 6.2 En Cas de Doute

```
SI INCERTAIN SUR:
- Niveau de sensibilité → Choisir le PLUS restrictif
- Terme à utiliser → Consulter Glossaire ou DEMANDER
- Contenu à inclure → L'OMETTRE et documenter l'omission
- Dérivation → NE PAS dériver, créer de novo
```

---

## 7. MATRICE DE VALIDATION

| Action | Validation Requise |
|--------|-------------------|
| Créer document PUBLIC | Auto (avec checklist) |
| Créer document PARTNER | Validation fondateur |
| Créer document NDA | Validation fondateur |
| Modifier document existant | Validation fondateur |
| Dériver vers niveau inférieur | Validation fondateur + filtrage |
| Ajouter terme au Glossaire | Validation fondateur |
| Supprimer du Glossaire | INTERDIT |

---

## 8. VIOLATIONS ET CONSÉQUENCES

### 8.1 Types de Violations

| Violation | Sévérité | Action |
|-----------|----------|--------|
| Utilisation terme interdit | Moyenne | Correction immédiate |
| Mélange de niveaux | Haute | Révision complète |
| Dérivation non autorisée | Critique | Destruction document |
| Partage hors contexte | Critique | Révocation accès |
| Reconstruction logique | Critique | Violation NDA |

### 8.2 Processus de Correction

```
1. Identifier la violation
2. Documenter l'impact
3. Retirer/corriger le document
4. Notifier les parties affectées
5. Mettre à jour les procédures si nécessaire
6. Validation fondateur
```

---

## ✅ VALIDATION

```
Document: CHE·NU™ Documentation Usage Rules
ID: RUL-001
Version: 1.0
Sensibilité: 🔐 LEVEL_NDA (Internal)
Créé: 23 Décembre 2025

Ce document définit les règles d'usage de TOUTE documentation CHE·NU.
Non-respect = violation de gouvernance.
```

---

```
[CHE·NU — LEVEL_NDA] — This document is not self-sufficient.
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
