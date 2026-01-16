# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║                           CHE·NU™                                            ║
# ║                                                                              ║
# ║                    SYSTEM OVERVIEW                                           ║
# ║                                                                              ║
# ║                         VERSION 1.0                                          ║
# ║                                                                              ║
# ║              🟡 SEMI-PRIVATE — NDA REQUIRED                                  ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

---

# Vue d'ensemble

CHE·NU est organisé autour de quatre espaces distincts, 
un système de meetings structuré, et une séparation claire 
entre notes et décisions.

Ce document offre une vue fonctionnelle du système 
sans entrer dans les détails d'implémentation.

---

# 1. Les quatre espaces

## Architecture générale

```
┌─────────────────────────────────────────────────────────────┐
│                        CHE·NU                               │
├──────────────┬──────────────┬──────────────┬───────────────┤
│  Dashboard   │  Workspace   │ Collaboration│   Knowledge   │
│  (Observer)  │  (Produire)  │  (Décider)   │  (Comprendre) │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

## Dashboard — Piloter

**Mode** : Observation pure

Le Dashboard affiche l'état du système sans permettre de le modifier.

**Contenu** :
- État général du projet/équipe
- Décisions actives
- Changements récents
- Métriques clés

**Interaction** : Lecture seule

## Workspace — Produire

**Mode** : Travail concentré

L'espace de production individuelle ou en petite équipe.

**Contenu** :
- Tâches en cours
- Documents de travail
- Outils de production
- Contexte local

**Interaction** : Création et modification

## Collaboration Space — Délibérer

**Mode** : Réflexion collective

L'espace dédié aux échanges structurés et à la prise de décision.

**Contenu** :
- Notes partagées
- Meetings
- Décisions en cours
- Discussions thématiques

**Interaction** : Collaboration et validation

## Knowledge — Explorer

**Mode** : Compréhension

Navigation dans la connaissance accumulée.

**Contenu** :
- Thèmes et relations
- Historique des décisions
- Documentation
- Synthèses générées

**Interaction** : Exploration et consultation

---

# 2. Système de Meetings

## Principe

Les meetings sont structurés par intention. 
Chaque type a un objectif clair et des limites définies.

## Les quatre types

### Alignment

| Aspect | Détail |
|--------|--------|
| **Objectif** | Synchroniser la compréhension |
| **Durée typique** | 30-45 min |
| **Output** | Compréhension partagée documentée |
| **Interdit** | Décider, assigner des tâches |

### Decision

| Aspect | Détail |
|--------|--------|
| **Objectif** | Trancher une question |
| **Durée typique** | 45-60 min |
| **Output** | Décision(s) formalisée(s) |
| **Interdit** | Produire, explorer sans cadre |

### Working

| Aspect | Détail |
|--------|--------|
| **Objectif** | Produire ensemble |
| **Durée typique** | 60-90 min |
| **Output** | Travail concret réalisé |
| **Interdit** | Délibérer longuement, décider |

### Review / Retrospective

| Aspect | Détail |
|--------|--------|
| **Objectif** | Évaluer et apprendre |
| **Durée typique** | 45-60 min |
| **Output** | Apprentissages documentés |
| **Interdit** | Accuser, décider dans l'urgence |

---

# 3. Notes vs Décisions

## Distinction fondamentale

| Aspect | Notes | Décisions |
|--------|-------|-----------|
| **Nature** | Capture libre | Engagement formel |
| **Évolution** | Libre | Contrôlée |
| **Validation** | Non requise | Explicite |
| **Impact** | Personnel/exploratoire | Collectif/structurant |

## Transformation Note → Décision

Une note peut devenir une décision si :

1. Elle est discutée dans un **Decision Meeting**
2. Les parties concernées sont présentes
3. Une validation explicite est obtenue
4. Elle est formalisée avec un statut

## Cycle de vie des décisions

```
┌─────────┐
│  Draft  │ ← Proposition initiale
└────┬────┘
     ↓
┌─────────┐
│ Active  │ ← Validée, en vigueur
└────┬────┘
     │
     ├────────────┐
     ↓            ↓
┌─────────┐  ┌───────────┐
│Superseded│  │ Revisited │
└─────────┘  └───────────┘
```

---

# 4. Flux typiques

## Flux de travail individuel

```
1. Consulter Dashboard (état, priorités)
2. Entrer en Workspace (production)
3. Consulter Knowledge si besoin (contexte)
4. Revenir au Workspace
5. Partager en Collaboration si nécessaire
```

## Flux de décision collective

```
1. Préparer en Workspace (document, options)
2. Partager en Collaboration (discussion)
3. Planifier Decision Meeting
4. Tenir le meeting
5. Formaliser la décision
6. Visible en Dashboard (état)
```

## Flux de révision

```
1. Signal en Dashboard (besoin de révision)
2. Consulter Knowledge (contexte original)
3. Préparer en Collaboration (nouvelle proposition)
4. Planifier Decision Meeting
5. Décision : maintien, modification ou remplacement
```

---

# 5. Rôle des agents

## Principe général

Les agents IA assistent sans interférer.
Ils sont contextuels : leurs capacités dépendent de l'espace.

## Par espace

| Espace | Rôle agent |
|--------|------------|
| **Dashboard** | Résumer l'état, signaler les changements |
| **Workspace** | Assistance ponctuelle, rappel de contexte |
| **Collaboration** | Structuration, résumé, détection d'incohérences |
| **Knowledge** | Explication, génération de synthèses |

## Limites absolues

Les agents ne peuvent **jamais** :
- Prendre des décisions
- Modifier des décisions existantes
- Agir sans contexte d'espace
- Interrompre avec du contenu non sollicité

---

# 6. Intégration des composants

## Relation entre espaces

```
                 ┌─────────────┐
                 │  Dashboard  │
                 │  (observe)  │
                 └──────┬──────┘
                        │ lit
        ┌───────────────┼───────────────┐
        │               │               │
        ↓               ↓               ↓
┌───────────┐   ┌───────────────┐   ┌───────────┐
│ Workspace │ ← │ Collaboration │ → │ Knowledge │
│ (produit) │   │   (décide)    │   │(comprend) │
└───────────┘   └───────────────┘   └───────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │ alimente
                        ↓
                 ┌─────────────┐
                 │  Dashboard  │
                 │  (observe)  │
                 └─────────────┘
```

## Flux d'information

- **Workspace** → produit du contenu
- **Collaboration** → produit des décisions
- **Knowledge** → capitalise et relie
- **Dashboard** → synthétise et affiche

---

# Conclusion

CHE·NU est conçu comme un système intégré où chaque composant 
a une fonction précise et des limites claires.

La séparation des espaces n'est pas arbitraire. 
Elle protège l'intégrité de chaque mode cognitif :
observer, produire, décider, comprendre.

Cette architecture permet un travail de qualité sur le long terme,
sans le chaos habituel des outils fragmentés.

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                              CHE·NU™                                         ║
║                                                                              ║
║                    SYSTEM OVERVIEW v1.0                                      ║
║                                                                              ║
║              🟡 SEMI-PRIVATE — DO NOT SHARE PUBLICLY                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
