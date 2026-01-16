# 1. Contexte du Système

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHAPITRE 1 — CONTEXTE SYSTÉMIQUE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1.1 CHE-NU — Moteur d'Orchestration

CHE-NU est un **moteur d'orchestration multi-agents** structuré en **9 sphères fonctionnelles**.

### Fonctions Principales

| Rôle | Description |
|------|-------------|
| **Coordinateur** | Orchestre les interactions entre agents |
| **Mémoire** | Infrastructure de persistance et rappel |
| **Producteur** | Génération de connaissances et récits |

### Architecture en 9 Sphères

```
┌─────────────────────────────────────────────────────────────┐
│                      SPHÈRES CHE-NU                         │
├─────────────────────────────────────────────────────────────┤
│  1. Personal      │  Vie personnelle, bien-être            │
│  2. Business      │  Entreprise, stratégie, finances       │
│  3. Government    │  Administration, conformité            │
│  4. Design Studio │  Création, production visuelle         │
│  5. Community     │  Réseaux, relations                    │
│  6. Social        │  Impact social, mission                │
│  7. Entertainment │  Culture, loisirs, arts                │
│  8. Team          │  Collaboration, équipes                │
│  9. [Système]     │  Infrastructure, monitoring            │
└─────────────────────────────────────────────────────────────┘
```

**Point clé**: CHE-NU n'est pas un agent unique, mais un **écosystème gouverné**.

---

## 1.2 AT·OM Mapping — Couche de Vision

AT·OM est la couche de **vision**, de **métamodélisation** et de **cartographie symbolique**.

### Position dans l'Architecture

AT·OM agit comme une **10ème sphère** :
- Non opérationnelle directement
- Structurante pour le sens, la cohérence et la direction

### Fonctions AT·OM

| Fonction | Description |
|----------|-------------|
| **Vision** | Définition de la direction à long terme |
| **Métamodèle** | Structure des structures |
| **Cartographie** | Représentation symbolique du système |
| **Cohérence** | Maintien de l'unité sémantique |

### Représentation Graphique

```
                    ┌─────────┐
                    │  AT·OM  │  ← Vision, Structure
                    │ (Meta)  │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Sphère  │    │ Sphère  │    │ Sphère  │
    │   1-3   │    │   4-6   │    │   7-9   │
    └─────────┘    └─────────┘    └─────────┘
         │               │               │
         └───────────────┴───────────────┘
                         │
                    ┌────┴────┐
                    │ CHE-NU  │  ← Action, Exécution
                    │ (Core)  │
                    └─────────┘
```

---

## 1.3 Dualité Fonctionnelle

Le système repose sur une **dualité explicite** et intentionnelle.

### Tableau Comparatif

| Aspect | CHE-NU | AT·OM |
|--------|--------|-------|
| **Nature** | Action | Vision |
| **Mode** | Production | Définition |
| **Temps** | Présent / Futur proche | Long terme |
| **Sortie** | Artefacts concrets | Structures abstraites |
| **Gouvernance** | Exécute les règles | Définit les règles |

### Pourquoi cette Séparation ?

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRINCIPE DE SÉPARATION                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Pouvoir d'AGIR  ≠  Pouvoir de DÉFINIR                         │
│                                                                  │
│   Cette séparation évite :                                       │
│   • La confusion des responsabilités                             │
│   • L'auto-validation des actions                                │
│   • La dérive sans référentiel externe                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Analogie Systémique

| Domaine | Équivalent CHE-NU | Équivalent AT·OM |
|---------|-------------------|------------------|
| Biologie | Métabolisme | ADN |
| Informatique | Runtime | Compilateur |
| Organisation | Opérations | Gouvernance |
| Construction | Chantier | Architecte |

---

## 1.4 Implications pour l'Activation

### Ce qui est activé

- **CHE-NU** : Les 350+ agents, les sphères, le cortex
- **AT·OM** : La structure de cohérence, les cycles

### Ce qui reste stable

- **Les règles fondamentales** : définies avant activation
- **La gouvernance humaine** : non automatisable
- **Les limites du système** : définies explicitement

---

## Points de Contrôle

- [ ] Comprendre la différence CHE-NU / AT·OM
- [ ] Identifier les 9 sphères opérationnelles
- [ ] Reconnaître AT·OM comme sphère méta (non opérationnelle)
- [ ] Accepter la dualité action / vision

---

*Prochain chapitre : 02_ARCHITECTURE_TECHNIQUE.md*
