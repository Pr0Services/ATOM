# 🧠 CHE·NU™ — PUZZLE INFORMATIONNEL NOVA — DOCUMENT MAÎTRE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           🧠 NOVA PUZZLE SYSTEM — SYNTHÈSE COMPLÈTE                         ║
║                                                                              ║
║     "Le cerveau de l'onboarding — Tout est connecté"                        ║
║                                                                              ║
║                    DOCUMENT DE RÉFÉRENCE UNIQUE                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Version**: 1.0 MASTER
**Date**: 23 Décembre 2025
**Statut**: RÉFÉRENCE CANONIQUE

---

# TABLE DES MATIÈRES GLOBALE

| # | Document | Contenu | Fichier |
|---|----------|---------|---------|
| 1 | **CE DOCUMENT** | Synthèse & Vue d'ensemble | `CHENU_PUZZLE_NOVA_MASTER.md` |
| 2 | Protocole Intégration | Comment intégrer un module | `CHENU_MODULE_INTEGRATION_PROTOCOL.md` |
| 3 | Cascades Déblocage | Ordre & dépendances | `CHENU_CASCADE_DEBLOCAGE_SYSTEM.md` |
| 4 | Besoins Sections | Info par section bureau | `CHENU_BESOINS_INFO_SECTIONS_BUREAU.md` |

---

# 1. VUE D'ENSEMBLE DU SYSTÈME

## 1.1 Qu'est-ce que le Puzzle Informationnel?

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         DÉFINITION DU PUZZLE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Le PUZZLE INFORMATIONNEL est le système par lequel Nova:                   ║
║                                                                              ║
║  1. COLLECTE des informations sur l'utilisateur                             ║
║     └─▶ Par observation (détection)                                         ║
║     └─▶ Par questions (optionnelles)                                        ║
║     └─▶ Par import (services externes)                                      ║
║     └─▶ Par inférence (déduction)                                           ║
║                                                                              ║
║  2. PERSONNALISE l'expérience                                               ║
║     └─▶ Interface adaptée                                                   ║
║     └─▶ Tutoriels pertinents                                                ║
║     └─▶ Features débloquées                                                 ║
║     └─▶ Suggestions contextuelles                                           ║
║                                                                              ║
║  3. GUIDE sans imposer                                                       ║
║     └─▶ Explications d'abord                                                ║
║     └─▶ Questions optionnelles                                              ║
║     └─▶ Skip toujours possible                                              ║
║     └─▶ Apprentissage continu                                               ║
║                                                                              ║
║  RÈGLE D'OR: L'utilisateur n'est JAMAIS bloqué par une pièce manquante     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 1.2 Architecture Globale

```
                              ┌─────────────────────────────────────┐
                              │         NOVA BRAIN                  │
                              │    (Intelligence Centrale)          │
                              └──────────────┬──────────────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
              ▼                              ▼                              ▼
    ┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
    │  PUZZLE ENGINE  │           │ TUTORIAL ENGINE │           │ VARIANT ENGINE  │
    │                 │           │                 │           │                 │
    │ • Collecte      │           │ • Séquences     │           │ • Profils       │
    │ • Détection     │           │ • Déblocages    │           │ • Contextes     │
    │ • Questions     │           │ • Imbrications  │           │ • Ajustements   │
    └────────┬────────┘           └────────┬────────┘           └────────┬────────┘
             │                             │                             │
             └─────────────────────────────┼─────────────────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────────────────┐
                              │         NOVA REGISTRY               │
                              │    (Base de données centrale)       │
                              ├─────────────────────────────────────┤
                              │ • Modules enregistrés               │
                              │ • Pièces puzzle par user            │
                              │ • État tutoriels par user           │
                              │ • Variantes actives                 │
                              │ • Historique questions              │
                              └─────────────────────────────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
    │   MODULE A      │         │   MODULE B      │         │   MODULE C      │
    │   (Manifest)    │         │   (Manifest)    │         │   (Manifest)    │
    │   + Nova Hooks  │         │   + Nova Hooks  │         │   + Nova Hooks  │
    └─────────────────┘         └─────────────────┘         └─────────────────┘
```

## 1.3 Les 4 Piliers du Système

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LES 4 PILIERS NOVA                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PILIER 1: PIÈCES DU PUZZLE                                           ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Unités d'information sur l'utilisateur                             ║ │
│  ║  • 4 sources: Détection, Question, Import, Inférence                  ║ │
│  ║  • 3 priorités: Essentiel, Utile, Optionnel                          ║ │
│  ║  • Stockage: Profil utilisateur                                       ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PILIER 2: TUTORIELS                                                  ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Guides interactifs contextuels                                     ║ │
│  ║  • 4 niveaux: Intro, Feature, Avancé, Imbriqué                       ║ │
│  ║  • Débloqués par actions/pièces                                       ║ │
│  ║  • Toujours skippables                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PILIER 3: QUESTIONS                                                  ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Invitations optionnelles                                           ║ │
│  ║  • Déclenchées par contexte                                           ║ │
│  ║  • Maximum 1 par session                                              ║ │
│  ║  • Skip = pas de relance immédiate                                    ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PILIER 4: VARIANTES                                                  ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Parcours adaptés au profil                                         ║ │
│  ║  • Ajustements contextuels                                            ║ │
│  ║  • Fusion intelligente                                                ║ │
│  ║  • Évolution dynamique                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. INVENTAIRE COMPLET DES PIÈCES

## 2.1 Pièces Système (Niveau 0)

| ID | Nom | Source | Obligatoire |
|----|-----|--------|-------------|
| P000 | Identité (nom) | Inscription | ✓ |
| P001 | Email | Inscription | ✓ |
| P002 | Langue | Inscription | ✓ |
| P003 | Conditions acceptées | Inscription | ✓ |
| P004 | Timezone | Auto-détection | ✓ |

## 2.2 Pièces Contextuelles (Niveau 1)

| ID | Nom | Source | Débloque |
|----|-----|--------|----------|
| P010 | Sphère principale | Détection | Tutoriels sphère |
| P011 | Premier thread créé | Détection | TUT-003 |
| P012 | Types fichiers | Détection | Organisation auto |
| P013 | Niveau expertise | Inférence | Complexité UI |

## 2.3 Pièces Sphère Personnel

| ID | Nom | Source | Débloque |
|----|-----|--------|----------|
| P-PER-001 | Budget actif | Détection (3+ factures) | TUT-P01 |
| P-PER-002 | Propriétaire | Détection (docs) | TUT-P03, Module Immo |
| P-PER-003 | Santé tracking | Détection (rappels) | TUT-P02 |
| P-PER-004 | Famille présente | Détection (mentions) | TUT-P04 |

## 2.4 Pièces Sphère Business

| ID | Nom | Source | Débloque |
|----|-----|--------|----------|
| P-BUS-001a | Mode Solo | Question | Path Freelance |
| P-BUS-001b | Mode Équipe | Question | Path Entreprise |
| P-BUS-002 | Facturation active | Détection | TUT-B01 |
| P-BUS-003 | Estimation active | Détection | TUT-B04 |
| P-BUS-004 | CRM besoin | Détection (3+ clients) | TUT-B02 |
| P-BUS-005a | Domaine Construction | Question/Détection | Module Construction |
| P-BUS-005b | Domaine Immobilier | Question/Détection | Module Immobilier |
| P-BUS-005c | Domaine Créatif | Question/Détection | Sphère Creative |
| P-BUS-006a | Petite équipe (2-5) | Question | TUT-B-TEAM-S |
| P-BUS-006b | Moyenne équipe (6-20) | Question | TUT-B-TEAM-M |
| P-BUS-006c | Grande entreprise (20+) | Question | TUT-B-TEAM-L |
| P-BUS-007a | Rôle Dirigeant | Question | TUT-B-ROLE-L |
| P-BUS-007b | Rôle Manager | Question | TUT-B-ROLE-M |
| P-BUS-007c | Rôle Employé | Question | TUT-B-ROLE-E |

## 2.5 Pièces Domaine Construction

| ID | Nom | Source | Débloque |
|----|-----|--------|----------|
| P-CON-001a | Rôle GC | Question | TUT-CON-GC |
| P-CON-001b | Rôle Sous-traitant | Question | TUT-CON-SUB |
| P-CON-001c | Rôle Propriétaire | Question | TUT-CON-OWN |
| P-CON-002 | Licence RBQ | Détection | TUT-CON-RBQ |
| P-CON-003 | Projet actif | Détection | TUT-CON-PROJ |
| P-CON-004 | Employés | Détection | TUT-CON-CNESST |
| P-CON-005 | Soumissions | Détection | TUT-CON-BID |

## 2.6 Pièces Domaine Immobilier

| ID | Nom | Source | Débloque |
|----|-----|--------|----------|
| P-IMM-001a | Type Résidentiel | Question | TUT-IMM-RES |
| P-IMM-001b | Type Commercial | Question | TUT-IMM-COM |
| P-IMM-001c | Type Mixte | Question | TUT-IMM-MIX |
| P-IMM-002 | Juridiction Québec | Détection (TAL) | TUT-IMM-TAL |
| P-IMM-003 | Portfolio large (5+) | Détection | TUT-IMM-PORT |
| P-IMM-004 | Paiements trackés | Détection | TUT-IMM-PAY |

## 2.7 Pièces Sections Bureau

| Section | IDs | Nombre |
|---------|-----|--------|
| Dashboard | P-DASH-001 à 012 | 12 |
| Notes | P-NOTE-001 à 011 | 8 |
| Tasks | P-TASK-001 à 020 | 12 |
| Projects | P-PROJ-001 à 012 + spé | 15+ |
| Threads | P-THRD-001 à 011 | 8 |
| Meetings | P-MEET-001 à 012 | 10 |
| Data | P-DATA-001 à 004 | 4 |
| Agents | P-AGNT-001 à 003 | 3 |
| Governance | P-GOVN-001 à 003 | 3 |

## 2.8 Statistiques Globales

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         STATISTIQUES PIÈCES                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CATÉGORIE                    │ NOMBRE │ SOURCE PRINCIPALE                  ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  Système (Niveau 0)           │    5   │ Inscription                        ║
║  Contextuelles (Niveau 1)     │    4   │ Détection                          ║
║  Sphère Personnel             │    8   │ Détection (70%) / Question (30%)   ║
║  Sphère Business              │   14   │ Question (60%) / Détection (40%)   ║
║  Domaine Construction         │    7   │ Détection (60%) / Question (40%)   ║
║  Domaine Immobilier           │    6   │ Détection (50%) / Question (50%)   ║
║  Sections Bureau              │   75   │ Détection (80%) / Question (20%)   ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  TOTAL                        │  119   │                                    ║
║                                                                              ║
║  Par source:                                                                 ║
║  • Détection automatique: ~70%                                              ║
║  • Questions Nova: ~25%                                                      ║
║  • Import externe: ~3%                                                       ║
║  • Inférence: ~2%                                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 3. INVENTAIRE COMPLET DES TUTORIELS

## 3.1 Tutoriels Système

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-000 | Bienvenue dans CHE·NU | 2min | Inscription |
| TUT-001 | Les Sphères | 1min | 1ère sphère visitée |
| TUT-002 | Le Workspace | 1min | 1er workspace créé |
| TUT-003 | Les Threads | 2min | 1er thread créé |
| TUT-004 | Vos Fichiers | 1min | 1er upload |

## 3.2 Tutoriels Sphère Personnel

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-P01 | Budget Personnel | 2min | P-PER-001 |
| TUT-P01a | Rapports Financiers | 2min | 3+ catégories |
| TUT-P01b | Suivi Abonnements | 1min | Dépenses récurrentes |
| TUT-P02 | Santé & Bien-être | 2min | P-PER-003 |
| TUT-P03 | Gestion Propriété | 2min | P-PER-002 |
| TUT-P03a | Portfolio Immo Perso | 2min | 2+ propriétés |
| TUT-P03b | Rentabilité Locative | 3min | Investisseur = true |
| TUT-P03c | Maintenance Maison | 2min | Résidence = true |
| TUT-P04 | Cercle Familial | 2min | P-PER-004 |
| TUT-P04a | Calendrier Partagé | 1min | Partage activé |
| TUT-P04b | Organisation Familiale | 2min | Enfants = true |

## 3.3 Tutoriels Sphère Business

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-B00a | Mode Freelance | 2min | P-BUS-001a |
| TUT-B00b | Mode Équipe | 2min | P-BUS-001b |
| TUT-B01 | Facturation Pro | 2min | P-BUS-002 |
| TUT-B01a | Client Récurrent | 1min | 3+ fact même client |
| TUT-B01b | Multi-devise | 2min | Fact internationale |
| TUT-B02 | Gestion Clients | 2min | P-BUS-004 |
| TUT-B03 | Gestion Projets | 2min | 1er projet créé |
| TUT-B04 | Estimation Rapide | 2min | P-BUS-003 |
| TUT-B-TEAM-S | Collaboration Simple | 2min | P-BUS-006a |
| TUT-B-TEAM-M | Gestion Équipe | 3min | P-BUS-006b |
| TUT-B-TEAM-L | Gouvernance Entreprise | 3min | P-BUS-006c |
| TUT-B-ROLE-L | Vue Direction | 2min | P-BUS-007a |
| TUT-B-ROLE-M | Vue Manager | 2min | P-BUS-007b |
| TUT-B-ROLE-E | Vue Collaborateur | 2min | P-BUS-007c |
| TUT-B-GEN | Business Générique | 3min | Domaine = Autre |

## 3.4 Tutoriels Construction

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-CONSTR-INTRO | Intro Construction | 2min | P-BUS-005a |
| TUT-CON-GC | Mode Entrepreneur | 3min | P-CON-001a |
| TUT-CON-SUB | Mode Sous-traitant | 2min | P-CON-001b |
| TUT-CON-OWN | Mode Donneur d'ouvrage | 2min | P-CON-001c |
| TUT-CON-RBQ | Conformité RBQ | 3min | P-CON-002 |
| TUT-CON-RBQ-ADV | RBQ Avancé | 3min | TUT-CON-RBQ + 30j |
| TUT-CON-PROJ | Gestion Chantier | 3min | P-CON-003 |
| TUT-CON-CNESST | Sécurité CNESST | 2min | P-CON-004 |
| TUT-CON-SUBS | Gestion Sous-traitants | 2min | Sous-traitants ajoutés |
| TUT-CON-BID | Soumissions Pro | 3min | P-CON-005 |
| TUT-CON-PRICING | Estimation Avancée | 3min | 5+ soumissions |

## 3.5 Tutoriels Immobilier

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-IMMO-INTRO | Intro Immobilier Pro | 2min | P-BUS-005b |
| TUT-IMM-RES | Gestion Résidentielle | 3min | P-IMM-001a |
| TUT-IMM-COM | Immobilier Commercial | 3min | P-IMM-001b |
| TUT-IMM-MIX | Portfolio Mixte | 2min | P-IMM-001c |
| TUT-IMM-TAL | Conformité TAL | 3min | P-IMM-002 |
| TUT-IMM-LEASE | Gestion Baux | 2min | Bail uploadé |
| TUT-IMM-PORT | Analytics Portfolio | 3min | P-IMM-003 |
| TUT-IMM-PAY | Suivi Paiements | 2min | P-IMM-004 |
| TUT-IMM-LATE | Gestion Impayés | 2min | Retard détecté |

## 3.6 Tutoriels Cross-Sphère

| ID | Titre | Durée | Déclencheur |
|----|-------|-------|-------------|
| TUT-CROSS-01 | Perso → Business | 2min | P-PER-002b (Investisseur) |
| TUT-CROSS-02 | Perso → Creative | 1min | Hobby créatif détecté |
| TUT-CROSS-03 | Perso → Community | 1min | Événement 10+ invités |

## 3.7 Statistiques Tutoriels

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         STATISTIQUES TUTORIELS                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CATÉGORIE                    │ NOMBRE │ DURÉE MOYENNE                      ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  Système                      │    5   │ 1.4 min                            ║
║  Sphère Personnel             │   11   │ 1.9 min                            ║
║  Sphère Business              │   15   │ 2.2 min                            ║
║  Domaine Construction         │   11   │ 2.6 min                            ║
║  Domaine Immobilier           │    9   │ 2.4 min                            ║
║  Cross-Sphère                 │    3   │ 1.3 min                            ║
║  Sections Bureau              │   30+  │ 1.5 min                            ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  TOTAL                        │   84+  │ ~2 min                             ║
║                                                                              ║
║  Par niveau:                                                                 ║
║  • Niveau 0 (Intro): 15 tutoriels                                           ║
║  • Niveau 1 (Feature): 40 tutoriels                                         ║
║  • Niveau 2 (Avancé): 20 tutoriels                                          ║
║  • Niveau 3 (Imbriqué): 9 tutoriels                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 4. INVENTAIRE COMPLET DES QUESTIONS

## 4.1 Questions Système/Onboarding

| ID | Question | Timing | Skippable |
|----|----------|--------|-----------|
| Q-SYS-001 | Quelle sphère en premier? | Fin TUT-000 | ✓ |
| Q-SYS-002 | Comment trouvez-vous CHE·NU? | Fin semaine 1 | ✓ |

## 4.2 Questions Business

| ID | Question | Timing | Skippable |
|----|----------|--------|-----------|
| Q-BUS-001 | Solo ou équipe? | 1ère visite Business | ✓ |
| Q-BUS-002 | Taille équipe? | Après Q-BUS-001 = équipe | ✓ |
| Q-BUS-003 | Votre rôle? | Après Q-BUS-002 | ✓ |
| Q-BUS-004 | Domaine d'activité? | Après 2 semaines | ✓ |

## 4.3 Questions Construction

| ID | Question | Timing | Skippable |
|----|----------|--------|-----------|
| Q-CON-001 | Rôle dans construction? | Entrée module | ✓ |
| Q-CON-002 | Bases prix standardisées? | 5+ soumissions | ✓ |

## 4.4 Questions Immobilier

| ID | Question | Timing | Skippable |
|----|----------|--------|-----------|
| Q-IMM-001 | Type immobilier géré? | Entrée module | ✓ |

## 4.5 Questions Sections Bureau

| ID | Question | Timing | Skippable |
|----|----------|--------|-----------|
| Q-DASH-001 | Infos prioritaires dashboard? | 5 visites | ✓ |
| Q-DASH-002 | Simple ou détaillé? | 30 jours | ✓ |
| Q-NOTE-001 | Organisation notes? | 10 notes | ✓ |
| Q-TASK-001 | Vue tâches préférée? | 5 tâches | ✓ |
| Q-TASK-002 | Rappels échéances? | 1ère deadline | ✓ |
| Q-TASK-003 | Déléguer à l'équipe? | Membre ajouté | ✓ |
| Q-PROJ-001 | Visualisation projets? | 1er projet | ✓ |
| Q-PROJ-002 | Méthodologie PM? | 3 projets (si expert) | ✓ |
| Q-THRD-001 | Archivage threads? | 10 threads | ✓ |
| Q-MEET-001 | Connecter calendrier? | 1ère visite | ✓ |
| Q-MEET-002 | Temps tampon réunions? | 2 réunions/jour | ✓ |
| Q-MEET-003 | Notes auto réunions? | 3 réunions complétées | ✓ |

## 4.6 Statistiques Questions

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         STATISTIQUES QUESTIONS                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CATÉGORIE                    │ NOMBRE │ TIMING PRINCIPAL                   ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  Système/Onboarding           │    2   │ Fin tutorial / Fin semaine         ║
║  Sphère Business              │    4   │ Contextuel                         ║
║  Domaine Construction         │    2   │ Contextuel                         ║
║  Domaine Immobilier           │    1   │ Contextuel                         ║
║  Sections Bureau              │   12   │ Après actions                      ║
║  ─────────────────────────────┼────────┼──────────────────────────────────  ║
║  TOTAL                        │   21   │                                    ║
║                                                                              ║
║  Règles:                                                                     ║
║  • Maximum 1 question par session                                           ║
║  • Maximum 3 questions par semaine                                          ║
║  • Toutes skippables                                                         ║
║  • Cooldown 7 jours après skip                                              ║
║  • Arrêt après 3 skips consécutifs                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 5. INVENTAIRE DES VARIANTES

## 5.1 Profils Utilisateur

| ID | Nom | Conditions | Ajustements principaux |
|----|-----|------------|------------------------|
| `absolute-beginner` | Débutant | < 5 sessions | Nova haute, UI minimale |
| `intermediate` | Intermédiaire | 10-50 sessions | Nova moyenne |
| `power-user` | Expert | 50+ sessions | Nova basse, UI complète |
| `freelance` | Freelance | P-BUS-001a = true | Features solo |
| `sme-business` | PME | P-BUS-006a/b = true | Features équipe |
| `construction-pro` | Construction | P-BUS-005a | Module Construction |
| `real-estate-pro` | Immobilier | P-BUS-005b | Module Immobilier |

## 5.2 Contextes

| ID | Nom | Trigger | Ajustements |
|----|-----|---------|-------------|
| `first-week` | Première semaine | < 7 jours | Mode découverte |
| `mobile-context` | Mobile | Device mobile | UI compacte |
| `work-hours` | Heures travail | 8h-18h weekday | Mode focus |
| `end-of-day` | Fin de journée | 17h-20h | Suggestions review |
| `return-after-absence` | Retour | 7+ jours absence | Re-onboarding léger |

---

# 6. FLUX DE DONNÉES

## 6.1 Flux de Collecte

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUX DE COLLECTE PIÈCE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐                                                            │
│  │ ACTION USER │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MODULE NOVA HOOKS                                 │   │
│  │                    onUserAction(action)                              │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                          │
│         ┌───────────────────────┼───────────────────────┐                  │
│         │                       │                       │                  │
│         ▼                       ▼                       ▼                  │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐            │
│  │  DÉTECTION  │        │   PATTERN   │        │  ANALYTICS  │            │
│  │   TRIGGER   │        │   CHECK     │        │   TRACK     │            │
│  └──────┬──────┘        └──────┬──────┘        └─────────────┘            │
│         │                      │                                           │
│         │ Match?               │ Pattern confirmé?                         │
│         │                      │                                           │
│         ▼                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              PUZZLE ENGINE - onPuzzlePieceDetected()                │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                          │
│         ┌───────────────────────┼───────────────────────┐                  │
│         │                       │                       │                  │
│         ▼                       ▼                       ▼                  │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐            │
│  │   STORE     │        │   CHECK     │        │   TRIGGER   │            │
│  │   PIECE     │        │  UNLOCKS    │        │  TUTORIALS  │            │
│  └─────────────┘        └──────┬──────┘        └─────────────┘            │
│                                │                                           │
│                                ▼                                           │
│                       ┌─────────────────┐                                  │
│                       │ UNLOCK FEATURES │                                  │
│                       │ UNLOCK TUTORIALS│                                  │
│                       │ QUEUE QUESTIONS │                                  │
│                       └─────────────────┘                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Flux Question Nova

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUX QUESTION NOVA                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐                                                            │
│  │   TRIGGER   │ (action, pièce, temps)                                    │
│  └──────┬──────┘                                                            │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    QUESTION ELIGIBILITY CHECK                        │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ □ Pièces prérequises collectées?                                    │   │
│  │ □ Pas de pièces d'exclusion?                                        │   │
│  │ □ Cooldown respecté? (7j après skip)                                │   │
│  │ □ Max asks pas atteint? (<3)                                        │   │
│  │ □ Max questions session pas atteint? (<1)                           │   │
│  │ □ Contexte approprié? (pas en erreur, pas en tutorial)             │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                          │
│              ┌──────────────────┴──────────────────┐                       │
│              │                                     │                       │
│              ▼                                     ▼                       │
│       ┌─────────────┐                       ┌─────────────┐                │
│       │   ÉLIGIBLE  │                       │ NON ÉLIGIBLE│                │
│       └──────┬──────┘                       └──────┬──────┘                │
│              │                                     │                       │
│              ▼                                     ▼                       │
│  ┌─────────────────────┐                    ┌─────────────┐                │
│  │  CHECK TIMING       │                    │    SKIP     │                │
│  │  immediate/after/   │                    │  (silent)   │                │
│  │  session_end/next   │                    └─────────────┘                │
│  └──────────┬──────────┘                                                   │
│             │                                                              │
│             ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DISPLAY QUESTION                                  │   │
│  │            [Options] [Skip] [Plus tard]                             │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                          │
│         ┌───────────────────────┴───────────────────────┐                  │
│         │                                               │                  │
│         ▼                                               ▼                  │
│  ┌─────────────────┐                           ┌─────────────────┐         │
│  │    RÉPONSE      │                           │      SKIP       │         │
│  └────────┬────────┘                           └────────┬────────┘         │
│           │                                             │                  │
│           ▼                                             ▼                  │
│  ┌─────────────────┐                           ┌─────────────────┐         │
│  │ • Store réponse │                           │ • Log skip      │         │
│  │ • Update pièce  │                           │ • Set cooldown  │         │
│  │ • Exec onAnswer │                           │ • Increment cnt │         │
│  │ • Nova message  │                           │                 │         │
│  └─────────────────┘                           └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 7. IMPLÉMENTATION TECHNIQUE

## 7.1 Structure des Fichiers

```
src/
├── core/
│   └── nova/
│       ├── index.ts                    # Export principal
│       ├── NovaRegistry.ts             # Registry central
│       ├── NovaBrain.ts                # Intelligence centrale
│       ├── engines/
│       │   ├── PuzzleEngine.ts         # Gestion pièces
│       │   ├── TutorialEngine.ts       # Gestion tutoriels
│       │   ├── QuestionEngine.ts       # Gestion questions
│       │   └── VariantEngine.ts        # Gestion variantes
│       ├── hooks/
│       │   ├── NovaHooks.interface.ts  # Interface hooks
│       │   └── BaseNovaHooks.ts        # Implémentation base
│       ├── types/
│       │   ├── puzzle.types.ts         # Types pièces
│       │   ├── tutorial.types.ts       # Types tutoriels
│       │   ├── question.types.ts       # Types questions
│       │   └── variant.types.ts        # Types variantes
│       └── validation/
│           └── ModuleValidator.ts      # Validation manifests
│
├── modules/
│   ├── [module-name]/
│   │   ├── module.manifest.ts          # Manifest obligatoire
│   │   ├── nova-hooks.ts               # Hooks Nova
│   │   └── ...                         # Code module
│   │
│   ├── mod-construction/
│   │   ├── module.manifest.ts
│   │   └── nova-hooks.ts
│   │
│   └── mod-immobilier-rental/
│       ├── module.manifest.ts
│       └── nova-hooks.ts
│
└── database/
    └── migrations/
        ├── 001_puzzle_tables.sql       # Tables puzzle
        ├── 002_tutorial_tables.sql     # Tables tutoriels
        └── 003_question_tables.sql     # Tables questions
```

## 7.2 API Endpoints

```typescript
// Routes API Nova

// Puzzle
GET    /api/nova/puzzle/:userId           // État puzzle utilisateur
POST   /api/nova/puzzle/piece             // Ajouter pièce
GET    /api/nova/puzzle/missing           // Pièces manquantes

// Tutoriels
GET    /api/nova/tutorials/:userId        // Tutoriels disponibles
POST   /api/nova/tutorials/start          // Démarrer tutoriel
POST   /api/nova/tutorials/complete       // Terminer tutoriel
POST   /api/nova/tutorials/skip           // Skip tutoriel

// Questions
GET    /api/nova/questions/pending        // Questions en attente
POST   /api/nova/questions/answer         // Répondre
POST   /api/nova/questions/skip           // Skip question

// Variantes
GET    /api/nova/variants/:userId         // Variantes actives
GET    /api/nova/adjustments/:userId      // Ajustements appliqués

// Registry
GET    /api/nova/registry/modules         // Modules enregistrés
GET    /api/nova/registry/stats           // Statistiques
```

---

# 8. CHECKLIST D'IMPLÉMENTATION

## 8.1 Phase 1: Core Nova (Semaine 1-2)

```
□ NovaRegistry base
  □ Enregistrement modules
  □ Storage pièces
  □ Storage tutoriels
  
□ PuzzleEngine
  □ Collecte pièces
  □ Détection triggers
  □ Vérification conditions
  
□ TutorialEngine
  □ Déblocage tutoriels
  □ Tracking progression
  □ Tutoriels imbriqués
  
□ QuestionEngine
  □ Éligibilité questions
  □ Timing management
  □ Skip/cooldown
  
□ Base de données
  □ Tables puzzle
  □ Tables tutoriels
  □ Tables questions
```

## 8.2 Phase 2: Module Integration (Semaine 3-4)

```
□ ModuleValidator
  □ Validation manifest
  □ Score validation
  
□ Nova Hooks Interface
  □ Interface complète
  □ Base implementation
  
□ Premier module test
  □ mod-construction manifest
  □ mod-construction hooks
  □ Tests end-to-end
  
□ Deuxième module test
  □ mod-immobilier-rental manifest
  □ mod-immobilier-rental hooks
  □ Tests end-to-end
```

## 8.3 Phase 3: Variantes (Semaine 5)

```
□ VariantEngine
  □ Sélection profils
  □ Sélection contextes
  □ Fusion ajustements
  
□ Variantes utilisateur
  □ absolute-beginner
  □ intermediate
  □ power-user
  □ freelance
  □ sme-business
  
□ Variantes contexte
  □ first-week
  □ mobile-context
  □ work-hours
```

## 8.4 Phase 4: UI Components (Semaine 6)

```
□ Composants tutoriels
  □ TutorialOverlay
  □ TutorialStep
  □ TutorialProgress
  
□ Composants questions
  □ NovaQuestion
  □ QuestionOptions
  □ SkipButton
  
□ Composants Nova
  □ NovaAvatar
  □ NovaMessage
  □ NovaBadge (nouveau tutoriel)
```

---

# 9. RÈGLES D'OR

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         LES 10 RÈGLES D'OR NOVA                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. JAMAIS DE BLOCAGE                                                        ║
║     └─▶ Une pièce manquante = expérience réduite, jamais bloquée           ║
║                                                                              ║
║  2. EXPLIQUER AVANT DE QUESTIONNER                                          ║
║     └─▶ Nova présente d'abord, invite ensuite                              ║
║                                                                              ║
║  3. OBSERVER PLUS QUE DEMANDER                                              ║
║     └─▶ 70% détection, 25% questions, 5% autre                             ║
║                                                                              ║
║  4. RESPECTER LE SKIP                                                        ║
║     └─▶ Skip = 7 jours cooldown, 3 skips = stop                            ║
║                                                                              ║
║  5. UNE QUESTION PAR SESSION MAX                                            ║
║     └─▶ Jamais de questionnaire, toujours contextuel                       ║
║                                                                              ║
║  6. TUTORIELS COURTS ET SKIPPABLES                                          ║
║     └─▶ Max 3 minutes, toujours option skip                                ║
║                                                                              ║
║  7. DÉBLOCAGE PROGRESSIF                                                     ║
║     └─▶ Chaque pièce ouvre des possibilités, pas de flood                  ║
║                                                                              ║
║  8. ADAPTATION SILENCIEUSE                                                   ║
║     └─▶ Nova ajuste sans annoncer, l'expérience s'améliore naturellement   ║
║                                                                              ║
║  9. PAS DE MANIFEST = PAS D'EXISTENCE                                       ║
║     └─▶ Tout module doit avoir son manifest Nova complet                   ║
║                                                                              ║
║  10. CLARTÉ > FEATURES                                                       ║
║      └─▶ Mieux vaut moins de pièces bien collectées que beaucoup mal       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    PUZZLE INFORMATIONNEL NOVA                                ║
║                         DOCUMENT MAÎTRE                                      ║
║                                                                              ║
║     119 Pièces | 84+ Tutoriels | 21 Questions | 12 Variantes               ║
║                                                                              ║
║           "L'intelligence qui guide sans imposer"                           ║
║                                                                              ║
║                          ON CONTINUE! 💪🔥                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
