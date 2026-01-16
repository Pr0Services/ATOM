# 03_PRIVATE — Documents Internes

## 🔴 Niveau : PRIVATE

Ce dossier contient les documents **strictement confidentiels**.

---

## Usage exclusif

- Fondateur(s)
- Core team
- IA (Claude) pour référence
- Archivage long terme

---

## Critères d'inclusion

Un document appartient ici s'il :

- Décrit le fonctionnement interne réel
- Contient des règles de gouvernance
- Définit les agents et leurs limites
- Explique la logique décisionnelle
- **Permet de reproduire CHE·NU**

---

## Documents actuels

| Fichier | Description |
|---------|-------------|
| `CHE-NU_Foundation_Manifest_v1.0.md` | Constitution complète de CHE·NU |
| `CHE-NU_Design_System_v1.0.md` | Tokens, couleurs, typo, règles |
| `CHE-NU_Governance_and_Agents_v1.0.md` | Permissions, voix, audit trail |
| `CHE-NU_Tooling_and_CLI_v1.0.md` | CLI, lint, Storybook, CI/CD |

---

## Ce qui appartient ici

| Catégorie | Exemples |
|-----------|----------|
| Manifeste fondateur | Vision complète, principes détaillés |
| Design System | Tokens, valeurs exactes, composants |
| Gouvernance | Permissions agents, audit, décisions |
| Tooling | CLI, lint, Storybook, tests |
| Architecture | Schémas, flux, implémentation |
| Sécurité | Règles, accès, vulnérabilités |

---

## Règles de gestion

### Versioning

- Format : `CHE-NU_<Sujet>_v<X.Y>.md`
- Incrémenter la version pour chaque modification
- Archiver les anciennes versions

### Accès

- Jamais dans un repo public
- Jamais envoyé sans validation
- Jamais simplifié pour partage externe

### Modifications

- Toute modification majeure = nouvelle version
- Documenter les changements
- Maintenir la cohérence entre documents

---

## Hiérarchie de dérivation

```
03_PRIVATE (source canonique)
     │
     ├──→ 02_SEMI_PRIVATE (version simplifiée)
     │
     └──→ 01_PUBLIC (version abstraite)
```

Les documents PUBLIC et SEMI-PRIVATE sont **dérivés** du PRIVATE,
jamais l'inverse.

---

## Règle d'or

> **Ce dossier contient la "constitution" de CHE·NU.**
> **Protéger comme tel.**

---

*Classification CHE·NU v1.0*
