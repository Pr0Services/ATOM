# 🧠 CHE·NU™ — NOVA PROGRESSIVE PROFILING & TUTORIAL SYSTEM

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║       ✨ NOVA PROGRESSIVE PROFILING SYSTEM ✨                                ║
║                                                                              ║
║       "Apprendre l'utilisateur sans jamais l'interroger"                     ║
║                                                                              ║
║       Governed | Non-Intrusive | Contextual | Reversible                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Version**: 1.0
**Date**: 23 Décembre 2025
**Auteur**: Équipe CHE·NU™
**Conformité**: Memory Governance Laws (10 Lois)

---

## 📋 TABLE DES MATIÈRES

1. [Philosophie du Profilage Non-Intrusif](#1-philosophie-du-profilage-non-intrusif)
2. [Architecture du Système de Découverte](#2-architecture-du-système-de-découverte)
3. [Moments de Découverte (Timing System)](#3-moments-de-découverte)
4. [Questions Contextuelles par Sphère](#4-questions-contextuelles-par-sphère)
5. [Mini-Tutoriels Débloquables](#5-mini-tutoriels-débloquables)
6. [Système de Besoins Détectés](#6-système-de-besoins-détectés)
7. [Nova Presence States & Explications](#7-nova-presence-states--explications)
8. [Angles Morts Identifiés](#8-angles-morts-identifiés)
9. [Plan d'Amélioration](#9-plan-damélioration)
10. [Implémentation Technique](#10-implémentation-technique)

---

# 1. PHILOSOPHIE DU PROFILAGE NON-INTRUSIF

## 1.1 Principes Fondamentaux

```
╔════════════════════════════════════════════════════════════════╗
║                    RÈGLE D'OR NOVA                             ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   "Nova n'interroge JAMAIS l'utilisateur de façon directe.    ║
║    Nova DÉCOUVRE les besoins à travers l'USAGE."              ║
║                                                                ║
║   ❌ Mauvais: "Quels sont vos objectifs professionnels?"      ║
║   ✅ Bon: Détecte que l'utilisateur crée des devis →          ║
║          Propose tutoriel estimation automatique              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## 1.2 Les 5 Règles Anti-Intrusion

| # | Règle | Description | Exemple |
|---|-------|-------------|---------|
| 1 | **Observer, pas demander** | Nova apprend des actions, pas des déclarations | Détecte 3 uploads de bail → comprend "locataire" |
| 2 | **Proposer, pas imposer** | Suggestions toujours refusables | "Je peux vous aider avec ça?" ≠ "Vous devez faire ça" |
| 3 | **Contexte immédiat** | Questions liées à l'action en cours | Pendant upload photo → "C'est une propriété?" |
| 4 | **1 question max** | Jamais de questionnaire | Une seule question à la fois |
| 5 | **Réponse optionnelle** | L'utilisateur peut ignorer | Pas de relance si ignoré |

## 1.3 Conformité Memory Governance

Le profilage respecte les **10 Lois de la Mémoire**:

```typescript
interface NovaProfileDiscovery {
  // Law 1: No Hidden Memory
  allDiscoveriesVisible: true;
  
  // Law 2: Explicit Storage Approval
  requiresConsentBeforeStorage: true;
  
  // Law 3: Identity Scoping
  discoveryBoundToIdentity: true;
  
  // Law 4: No Cross-Identity Access
  noCrossIdentityProfiling: true;
  
  // Law 5: Reversibility
  userCanDeleteAnyDiscovery: true;
  
  // Law 6: Operation Logging
  allDiscoveriesLogged: true;
  
  // Law 7: No Self-Directed Learning
  noAutonomousBehaviorChange: true;
  
  // Law 8: Domain Awareness
  discoveriesOrganizedByDomain: true;
  
  // Law 9: DataSpace Foundation
  discoveriesStoredInDataSpaces: true;
  
  // Law 10: Permission Hierarchy
  respectsUserPermissionLevel: true;
}
```

---

# 2. ARCHITECTURE DU SYSTÈME DE DÉCOUVERTE

## 2.1 Flow de Découverte Progressive

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NOVA DISCOVERY FLOW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │  ACTION  │───▶│ PATTERN  │───▶│  SIGNAL  │───▶│ INSIGHT  │             │
│  │  USER    │    │ DETECTION│    │ STRENGTH │    │ STORAGE  │             │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘             │
│       │               │               │               │                    │
│       ▼               ▼               ▼               ▼                    │
│  • Upload file    • Répétition?   • Faible (1x)   • Working Memory        │
│  • Create task    • Séquence?     • Moyen (3x)    • Session Memory        │
│  • Navigate       • Timing?       • Fort (5x+)    • Long-Term Memory      │
│  • Search         • Échec?        • Confirmé      • Profile Insight       │
│                                                                             │
│                          ▼                                                  │
│              ┌─────────────────────┐                                        │
│              │  CONSENT CHECKPOINT │                                        │
│              │  "Me souvenir?"     │                                        │
│              └─────────────────────┘                                        │
│                          │                                                  │
│           ┌──────────────┼──────────────┐                                   │
│           ▼              ▼              ▼                                   │
│        [Oui]        [Plus tard]     [Non]                                  │
│           │              │              │                                   │
│           ▼              ▼              ▼                                   │
│       Store in       Keep in        Forget                                 │
│       Profile        Session        Immediately                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Niveaux de Signal

| Niveau | Occurrences | Durée | Action Nova |
|--------|-------------|-------|-------------|
| **0 - Observation** | 1x | Immédiat | Aucune - Observation silencieuse |
| **1 - Pattern** | 2-3x | 24h | Note interne (non visible) |
| **2 - Signal** | 3-5x | 7 jours | Suggestion subtile possible |
| **3 - Besoin confirmé** | 5x+ | 30 jours | Proposition tutoriel/aide |
| **4 - Préférence établie** | 10x+ | Permanent | Automatisation proposée |

## 2.3 Types de Découvertes

```typescript
enum DiscoveryType {
  // Découvertes comportementales
  USAGE_PATTERN = 'usage_pattern',        // Comment l'utilisateur travaille
  WORKFLOW_PREFERENCE = 'workflow',       // Ordre des actions préféré
  TIME_PATTERN = 'time_pattern',          // Quand il travaille
  
  // Découvertes de domaine
  DOMAIN_FOCUS = 'domain_focus',          // Construction, Immobilier, etc.
  SPECIALIZATION = 'specialization',      // Sous-domaine spécifique
  EXPERTISE_LEVEL = 'expertise_level',    // Novice, Intermédiaire, Expert
  
  // Découvertes de besoin
  MISSING_FEATURE = 'missing_feature',    // Cherche quelque chose qu'on a
  STRUGGLING_TASK = 'struggling_task',    // Difficulté avec une tâche
  FREQUENT_ERROR = 'frequent_error',      // Erreurs répétées
  
  // Découvertes contextuelles
  LOCATION_CONTEXT = 'location',          // Québec, France, etc.
  LANGUAGE_PREFERENCE = 'language',       // FR, EN, mixte
  ACCESSIBILITY_NEED = 'accessibility',   // Besoins spéciaux
}
```

---

# 3. MOMENTS DE DÉCOUVERTE

## 3.1 Timing Optimal des Questions

```
╔════════════════════════════════════════════════════════════════════════════╗
║                    QUAND NOVA PEUT POSER UNE QUESTION                      ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ✅ MOMENTS APPROPRIÉS                  ❌ MOMENTS INTERDITS               ║
║  ─────────────────────                  ───────────────────                ║
║  • Après succès d'une tâche             • Pendant une tâche complexe      ║
║  • Lors d'une pause naturelle           • Au milieu d'un workflow         ║
║  • À la fin d'une session               • Lors d'une erreur               ║
║  • Au retour après absence              • Pendant une réunion             ║
║  • Première utilisation feature         • Lors d'un upload long           ║
║  • Après 3ème usage d'un pattern        • Si utilisateur semble pressé    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## 3.2 Triggers de Découverte par Contexte

### A. Onboarding Initial (Jour 1)

| Moment | Trigger | Question/Action Nova |
|--------|---------|---------------------|
| Premier login | Compte créé | "Bienvenue! Je suis Nova, votre guide. Explorons ensemble." |
| Choix sphère | Click sur sphère | "Je vois que [Sphère] vous intéresse. C'est un bon début!" |
| Premier upload | Document ajouté | "J'ai bien reçu ce document. Voulez-vous que je le classe?" |
| Première recherche | Query vide | "Cherchez-vous quelque chose? Je peux aider." |

### B. Première Semaine (Jours 2-7)

| Moment | Trigger | Question/Action Nova |
|--------|---------|---------------------|
| 3ème visite même sphère | Pattern détecté | "Je remarque que vous revenez souvent ici. Voulez-vous un raccourci?" |
| Tâche répétitive x3 | Pattern workflow | "Je peux automatiser ça pour vous. Intéressé?" |
| Recherche sans résultat | Frustration possible | "Je n'ai pas trouvé. Décrivez ce que vous cherchez?" |
| Upload même type x3 | Pattern contenu | "Vous gérez plusieurs [type]. Voulez-vous découvrir le mode [X]?" |

### C. Phase d'Adoption (Semaines 2-4)

| Moment | Trigger | Question/Action Nova |
|--------|---------|---------------------|
| Feature non utilisée | Gap d'usage | [Rien - pas de nagging] |
| Workaround détecté | Contournement | "Il existe une façon plus simple. Montrer?" |
| Nouveau domaine exploré | Extension | "Nouveau territoire! Besoin d'un guide?" |
| Agent jamais appelé | Ressource sous-utilisée | [Suggestion contextuelle lors d'un besoin] |

### D. Usage Régulier (Mois 2+)

| Moment | Trigger | Question/Action Nova |
|--------|---------|---------------------|
| Nouvelle feature disponible | Update système | "Nouveauté qui pourrait vous plaire: [X]" |
| Performance exceptionnelle | Succès | "Impressionnant! Voulez-vous partager cette méthode?" |
| Pattern mensuel | Récurrence | "C'est bientôt le moment de [tâche récurrente]" |
| Collaboration initiée | Multi-user | "Premier projet d'équipe! Guide disponible." |

---

# 4. QUESTIONS CONTEXTUELLES PAR SPHÈRE

## 4.1 Matrice Questions × Sphères

### 🏠 Personnel

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Upload facture | 3+ factures | "Voulez-vous suivre vos dépenses?" | Tutoriel Budget Personnel |
| Création rappel santé | 2+ rappels médicaux | "Je peux gérer votre calendrier santé?" | Tutoriel Health Tracking |
| Note famille | Mentions famille | "Des proches à ajouter?" | Tutoriel Cercle Familial |
| Document maison | Facture/contrat maison | "Vous êtes propriétaire?" | Tutoriel Gestion Propriété |

### 💼 Entreprises

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Création facture | Pattern facturation | "Facturation régulière? Template?" | Tutoriel Facturation Pro |
| Upload contrat | Documents légaux | "Besoin de suivi contractuel?" | Tutoriel Gestion Contrats |
| Mention client x3 | Relation commerciale | "CRM intégré disponible" | Tutoriel Client Management |
| Devis créé | Pattern estimation | "Automatiser vos devis?" | Tutoriel Estimation Rapide |

### 🏛️ Gouvernement & Institutions

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Document officiel | Formulaire gov | "Démarche administrative?" | Tutoriel Conformité |
| Mention impôts | Fiscalité | "Période fiscale? Aide disponible" | Tutoriel Déclarations |
| RBQ/CCQ/CNESST | Conformité QC | "Professionnellement réglementé?" | Tutoriel Compliance QC |

### 🎨 Creative Studio

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Upload média | Images/vidéos | "Projet créatif?" | Tutoriel Gestion Assets |
| Mention branding | Identité visuelle | "Travailler sur une marque?" | Tutoriel Brand Guidelines |
| Document script | Écriture | "Projet audiovisuel?" | Tutoriel Production |

### 👥 Community

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Événement créé | Organisation | "Événement communautaire?" | Tutoriel Event Planning |
| Contacts ajoutés x5 | Réseau local | "Construire votre réseau?" | Tutoriel Community Building |

### 📱 Social & Media

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Lien réseaux sociaux | Connexion externe | "Gérer vos réseaux ici?" | Tutoriel Social Dashboard |
| Contenu partagé | Publication | "Planifier vos posts?" | Tutoriel Content Calendar |

### 🎬 Entertainment

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Contenu loisir ajouté | Film/série/jeu | "Tracking loisirs?" | Tutoriel Entertainment Log |
| Voyage mentionné | Planification | "Voyage à organiser?" | Tutoriel Travel Planning |

### 🤝 My Team

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Invitation membre | Collaboration | "Constituer une équipe?" | Tutoriel Team Setup |
| Agent personnalisé | IA Labs | "Créer un agent custom?" | Tutoriel Agent Building |

### 📚 Scholar

| Contexte | Signal | Question Nova | Déblocage |
|----------|--------|---------------|-----------|
| Document recherche | PDF académique | "Recherche en cours?" | Tutoriel Research Mode |
| Mention formation | Apprentissage | "Objectif formation?" | Tutoriel Learning Path |

---

# 5. MINI-TUTORIELS DÉBLOQUABLES

## 5.1 Architecture des Tutoriels

```typescript
interface MiniTutorial {
  id: string;
  title: string;
  titleFr: string;
  
  // Conditions de déblocage
  unlockConditions: UnlockCondition[];
  
  // Contenu
  steps: TutorialStep[];
  duration: '30s' | '1min' | '2min' | '5min';
  
  // Comportement
  skippable: boolean;
  resumable: boolean;
  repeatable: boolean;
  
  // Récompense
  achievement?: Achievement;
  featureUnlocked?: string;
}

interface UnlockCondition {
  type: 'action' | 'pattern' | 'time' | 'manual';
  trigger: string;
  threshold?: number;
  sphere?: SphereId;
}
```

## 5.2 Catalogue Complet des Mini-Tutoriels

### 📦 TUTORIELS FONDAMENTAUX (Tier 0)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-001` | Bienvenue dans CHE·NU | 2min | Automatique (premier login) | Présentation Nova, navigation sphères, premier workspace |
| `TUT-002` | Comprendre les Sphères | 1min | Premier changement de sphère | Concept contexte, séparation, spécificités |
| `TUT-003` | Votre Premier Thread | 1min | Premier thread créé | Concept .chenu, continuité, mémoire |
| `TUT-004` | Nova, Votre Guide | 30s | Première question utilisateur | Rôle Nova, différence avec agents, comment demander |
| `TUT-005` | Gouvernance & Tokens | 2min | Premier coût token affiché | Budget, transparence, contrôle |

### 🏠 TUTORIELS PERSONNEL (Tier 1)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-P01` | Budget Personnel | 2min | 3+ factures uploadées | Tracking dépenses, catégories, rapports |
| `TUT-P02` | Suivi Santé | 2min | 2+ rappels santé | Calendrier médical, historique, alertes |
| `TUT-P03` | Gestion Propriété | 5min | Document maison détecté | DataSpace propriété, maintenance, documents |
| `TUT-P04` | Cercle Familial | 2min | Contacts famille | Partage familial, permissions, calendrier |
| `TUT-P05` | Objectifs Personnels | 2min | Création tâche long-terme | Goal tracking, milestones, motivation |

### 💼 TUTORIELS BUSINESS (Tier 1)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-B01` | Facturation Pro | 2min | Première facture créée | Templates, automatisation, suivi paiements |
| `TUT-B02` | Gestion Clients | 2min | 3+ contacts clients | CRM intégré, historique, pipeline |
| `TUT-B03` | Projets Business | 5min | Premier projet créé | Board, timeline, ressources |
| `TUT-B04` | Estimation Rapide | 2min | Premier devis | 1-Click estimation, templates métier |
| `TUT-B05` | Multi-Entreprise | 2min | Deuxième identité business | Séparation, switching, consolidation |

### 🏗️ TUTORIELS DOMAINE CONSTRUCTION (Tier 2)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-C01` | Soumission Chantier | 5min | Premier devis construction | Matériaux, main-d'œuvre, marges |
| `TUT-C02` | Conformité RBQ | 2min | Mention licence RBQ | Suivi licence, formation, obligations |
| `TUT-C03` | Gestion Chantier | 5min | Projet construction actif | Timeline, sous-traitants, inspections |
| `TUT-C04` | CNESST & Sécurité | 2min | Chantier avec employés | Safety compliance, documentation |

### 🏢 TUTORIELS DOMAINE IMMOBILIER (Tier 2)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-I01` | Portfolio Locatif | 5min | 2+ propriétés | Vue consolidée, métriques, alertes |
| `TUT-I02` | Gestion Locataires | 2min | Premier bail uploadé | TAL, communications, paiements |
| `TUT-I03` | Maintenance Préventive | 2min | Première propriété complète | Calendrier, historique, coûts |
| `TUT-I04` | Analyse ROI | 2min | Données financières complètes | Calculs, projections, comparaisons |

### 🎨 TUTORIELS CRÉATIFS (Tier 2)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-CR01` | Gestion Assets | 2min | 10+ fichiers média | Organisation, tags, versions |
| `TUT-CR02` | Brand Guidelines | 2min | Projet branding créé | Couleurs, fonts, templates |
| `TUT-CR03` | Production Pipeline | 5min | Projet vidéo/audio | Workflow, review, export |

### 🤖 TUTORIELS AGENTS & IA (Tier 3)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-A01` | Comprendre les Agents | 2min | Premier agent appelé | Hiérarchie L0-L3, spécialisations |
| `TUT-A02` | Agent Personnalisé | 5min | Accès IA Labs | Création, training, déploiement |
| `TUT-A03` | Orchestration Multi-Agent | 2min | Workflow complexe | Coordination, handoffs, supervision |
| `TUT-A04` | Encoding Avancé | 2min | Tokens > 1000 | Optimisation, compression, qualité |

### 🥽 TUTORIELS XR (Tier 3)

| ID | Nom | Durée | Déblocage | Contenu |
|----|-----|-------|-----------|---------|
| `TUT-X01` | Mode XR Basics | 2min | Premier toggle XR | Navigation spatiale, contrôles |
| `TUT-X02` | Réunion Immersive | 2min | Première réunion XR | Avatars, objets partagés, annotations |
| `TUT-X03` | Visite Virtuelle | 2min | Propriété avec photos 360 | Navigation, annotations, partage |

## 5.3 État de Progression Tutoriels

```typescript
interface UserTutorialProgress {
  userId: string;
  
  // Tutoriels complétés
  completed: {
    tutorialId: string;
    completedAt: Date;
    skipped: boolean;
    timeSpent: number;
  }[];
  
  // Tutoriels débloqués mais pas commencés
  unlocked: {
    tutorialId: string;
    unlockedAt: Date;
    unlockedBy: string; // trigger description
  }[];
  
  // Tutoriels en cours
  inProgress: {
    tutorialId: string;
    currentStep: number;
    startedAt: Date;
  }[];
  
  // Tutoriels suggérés (non encore débloqués)
  suggested: {
    tutorialId: string;
    progressToUnlock: number; // 0-100%
    missingConditions: string[];
  }[];
}
```

---

# 6. SYSTÈME DE BESOINS DÉTECTÉS

## 6.1 Taxonomie des Besoins

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    HIÉRARCHIE DES BESOINS UTILISATEUR                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  NIVEAU 4: OPTIMISATION                                                  │
│  └── Automatisation, Performance, Scale                                  │
│                                                                          │
│  NIVEAU 3: EXPANSION                                                     │
│  └── Nouveaux domaines, Collaboration, Intégrations                      │
│                                                                          │
│  NIVEAU 2: MAÎTRISE                                                      │
│  └── Workflows complexes, Agents spécialisés, Reporting                  │
│                                                                          │
│  NIVEAU 1: FONDAMENTAUX                                                  │
│  └── Navigation, Création, Organisation, Recherche                       │
│                                                                          │
│  NIVEAU 0: DÉCOUVERTE                                                    │
│  └── Comprendre CHE·NU, Premiers pas, Orientation                        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Signaux de Besoin par Type

### Besoins Explicites (Faciles à détecter)

| Signal | Besoin Détecté | Réponse Nova |
|--------|----------------|--------------|
| Recherche "comment..." | Aide demandée | Tutoriel contextuel |
| Click sur "?" | Documentation | Tooltip/guide |
| "Je ne comprends pas" | Confusion | Explication simplifiée |
| "C'est possible de..." | Feature discovery | Démonstration |

### Besoins Implicites (Détection pattern)

| Signal | Besoin Détecté | Réponse Nova |
|--------|----------------|--------------|
| 3x même navigation | Raccourci | Proposition accès rapide |
| Copier-coller répétitif | Template | Suggestion automatisation |
| Annuler > 3x | Workflow confus | Guide étape par étape |
| Session > 2h sans pause | Fatigue | Suggestion pause |

### Besoins Latents (Prédiction)

| Pattern | Besoin Probable | Action Nova |
|---------|-----------------|-------------|
| Entreprise + Immobilier | Gestion locative pro | Suggestion domaine |
| Creative + Business | Freelance | Mode freelance |
| Construction + Timeline | Suivi chantier | Dashboard projet |

## 6.3 Système de Scoring des Besoins

```typescript
interface NeedScore {
  needId: string;
  category: NeedCategory;
  
  // Scoring
  signals: {
    signalType: string;
    occurrences: number;
    lastSeen: Date;
    weight: number;
  }[];
  
  // Score calculé
  totalScore: number;         // 0-100
  confidence: number;         // 0-1
  urgency: 'low' | 'medium' | 'high';
  
  // Seuils
  thresholds: {
    suggestion: 30,           // Score pour suggestion passive
    proposal: 50,             // Score pour proposition active
    tutorial: 70,             // Score pour déblocage tutoriel
    automation: 90,           // Score pour automatisation
  };
  
  // Actions prises
  actionsTaken: {
    action: string;
    timestamp: Date;
    userResponse: 'accepted' | 'declined' | 'ignored';
  }[];
}
```

---

# 7. NOVA PRESENCE STATES & EXPLICATIONS

## 7.1 États de Nova et Messages Associés

```typescript
const NOVA_STATES_MESSAGES = {
  // État READY - Prête à aider
  ready: {
    defaultMessages: [
      "Je suis là si vous avez besoin.",
      "Prête à vous guider.",
      "Comment puis-je aider?",
    ],
    contextualMessages: {
      afterSuccess: "Bien joué! Autre chose?",
      newSession: "Content de vous revoir!",
      longAbsence: "Ça fait un moment! Besoin d'un rappel?",
    },
  },
  
  // État ACTIVE - En conversation
  active: {
    defaultMessages: [
      "Je vous écoute...",
      "Continuez, je suis avec vous.",
    ],
    contextualMessages: {
      processing: "Je réfléchis à ça...",
      searching: "Je cherche dans vos données...",
      coordinating: "Je coordonne avec les agents spécialisés...",
    },
  },
  
  // État THINKING - Traitement en cours
  thinking: {
    defaultMessages: [
      "Analyse en cours...",
      "Un moment, je vérifie...",
    ],
    contextualMessages: {
      complexTask: "C'est une demande complexe, j'y travaille.",
      agentCoordination: "Je consulte les spécialistes...",
      dataAnalysis: "J'analyse vos données...",
    },
  },
  
  // État IDLE - En veille
  idle: {
    defaultMessages: [
      "En veille. Cliquez pour m'activer.",
    ],
    contextualMessages: {
      userBusy: "Je vous laisse travailler tranquille.",
      nightMode: "Mode nuit actif.",
    },
  },
  
  // État ALERT - Notification importante
  alert: {
    defaultMessages: [],
    contextualMessages: {
      newFeature: "✨ Nouveauté disponible!",
      tutorialUnlocked: "🎓 Nouveau tutoriel débloqué!",
      milestone: "🏆 Objectif atteint!",
      reminder: "⏰ Rappel planifié",
      governanceAlert: "⚠️ Action requise",
    },
  },
};
```

## 7.2 Moments d'Explication Nova

### Explications Automatiques (Proactives)

| Moment | Explication Nova | Durée |
|--------|------------------|-------|
| Premier accès feature | "Ceci est [X]. Il permet de [Y]." | 10s |
| Nouveau concept | "Un Thread est une ligne de pensée persistante." | 15s |
| Token consumption | "Cette action coûtera ~50 tokens." | 5s |
| Agent activation | "[Agent] se spécialise en [domaine]." | 10s |
| Error occurs | "Voici ce qui s'est passé: [explication simple]" | 15s |

### Explications Sur Demande (Click "?")

| Élément | Explication |
|---------|-------------|
| Sphère | Concept, contenu typique, différence avec autres |
| Bureau Section | But, contenus possibles, actions disponibles |
| Thread | Persistance, scope, budget associé |
| Agent | Spécialisation, capacités, limites |
| Token | Valeur, consommation, recharge |
| Governance | Pourquoi, comment, contrôle utilisateur |

### Explications de Gouvernance (Critiques)

| Situation | Explication Obligatoire |
|-----------|------------------------|
| Élévation requise | "Cette action nécessite votre approbation car [raison]." |
| Cross-identity tentée | "Je ne peux pas accéder à [X] depuis ce contexte." |
| Budget dépassé | "Le budget pour cette action est atteint. Options: [...]" |
| Données sensibles | "Ces informations sont protégées. Confirmer l'accès?" |

## 7.3 Tonalité Nova par Contexte

```typescript
const NOVA_TONE_GUIDELINES = {
  // Ton par défaut
  default: {
    style: 'professionnel_chaleureux',
    examples: [
      "Je peux vous aider avec ça.",
      "Voici ce que j'ai trouvé.",
      "Souhaitez-vous que j'approfondisse?",
    ],
  },
  
  // Contexte erreur/problème
  error: {
    style: 'empathique_solution',
    examples: [
      "Je comprends, c'est frustrant. Voici une solution.",
      "Ce n'est pas ce que vous attendiez. Essayons autrement.",
    ],
  },
  
  // Contexte succès
  success: {
    style: 'encourageant_modeste',
    examples: [
      "C'est fait!",
      "Parfait, c'est en place.",
    ],
  },
  
  // Contexte apprentissage
  learning: {
    style: 'pédagogue_patient',
    examples: [
      "C'est une bonne question. Voici comment ça fonctionne...",
      "Pas de souci, je vous montre étape par étape.",
    ],
  },
  
  // Contexte gouvernance
  governance: {
    style: 'clair_transparent',
    examples: [
      "Pour votre sécurité, cette action requiert confirmation.",
      "Voici exactement ce que cette action va faire: [...]",
    ],
  },
};
```

---

# 8. ANGLES MORTS IDENTIFIÉS

## 8.1 Gaps dans le Système Actuel

### 🔴 Critiques (À corriger immédiatement)

| ID | Gap | Impact | Solution Proposée |
|----|-----|--------|-------------------|
| GAP-01 | **Pas de détection silence prolongé** | Utilisateur bloqué non détecté | Ajouter timeout + question contextuelle |
| GAP-02 | **Questions après erreur** | Intrusion au mauvais moment | Bloquer questions pendant état erreur |
| GAP-03 | **Pas de "Do Not Disturb"** | Utilisateur ne peut pas désactiver Nova suggestions | Ajouter mode DND |
| GAP-04 | **Tutoriels non adaptatifs** | Même tutoriel pour expert et novice | Adapter durée/profondeur selon expertise |

### 🟠 Majeurs (Sprint suivant)

| ID | Gap | Impact | Solution Proposée |
|----|-----|--------|-------------------|
| GAP-05 | **Pas de feedback loop** | On ne sait pas si suggestions sont utiles | Tracker accept/decline ratio |
| GAP-06 | **Tutoriels non localisés** | UX dégradée non-FR | Ajouter EN, ES |
| GAP-07 | **Pas de persona "découverte"** | Nouveaux users overwhelmed | Mode simplifié jour 1-7 |
| GAP-08 | **Manque onboarding XR** | XR trop complexe sans guide | Tutoriel XR dédié |

### 🟡 Modérés (Backlog)

| ID | Gap | Impact | Solution Proposée |
|----|-----|--------|-------------------|
| GAP-09 | Pas de gamification | Motivation réduite | Badges/achievements |
| GAP-10 | Tutoriels non vidéo | Certains apprennent mieux visuellement | Ajouter vidéos courtes |
| GAP-11 | Pas de comparaison pairs | Utilisateur ne sait pas s'il progresse | Benchmarks anonymes |
| GAP-12 | Manque rappels tutoriels | Utilisateurs oublient features | Rappels périodiques doux |

## 8.2 Questions Non Couvertes

### Par Sphère - Manquantes

| Sphère | Questions Manquantes |
|--------|---------------------|
| 🏠 Personnel | Détection situation familiale (enfants?), Animaux domestiques |
| 💼 Business | Type entreprise (PME/Startup/Corp), Secteur industrie |
| 🏛️ Gouvernement | Juridiction spécifique, Niveau accréditation |
| 🎨 Creative | Style artistique préféré, Outils externes utilisés |
| 👥 Community | Type associations, Niveau engagement local |
| 📱 Social | Plateformes actives, Objectifs (personal brand?) |
| 🎬 Entertainment | Genres préférés, Budget loisirs |
| 🤝 Team | Taille équipe, Méthodologie (Agile/Waterfall) |
| 📚 Scholar | Niveau études, Domaine recherche |

### Transversales - Manquantes

| Catégorie | Questions Manquantes |
|-----------|---------------------|
| Accessibilité | Déficiences visuelles/auditives, Préférences contrast |
| Langue | Préférence FR/EN, Terminologie métier |
| Timing | Heures de travail habituelles, Timezone |
| Confidentialité | Niveau de partage souhaité |

## 8.3 Patterns Non Détectés

| Pattern | Pourquoi Manquant | Solution |
|---------|-------------------|----------|
| Frustration accumulative | Pas de tracking émotionnel | Ajouter sentiment analysis |
| Contexte switching fréquent | Pas de compteur sphère | Tracker navigation patterns |
| Collaboration patterns | Focus sur single-user | Ajouter social graph |
| Saisonnalité | Pas d'analyse temporelle longue | Tracking annuel |

---

# 9. PLAN D'AMÉLIORATION

## 9.1 Roadmap Corrections

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    AMÉLIORATION PROGRESSIVE NOVA                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SPRINT 1 (Semaine 1-2): FONDAMENTAUX                                        │
│  ├── ✅ Fix GAP-01: Détection silence prolongé                               │
│  ├── ✅ Fix GAP-02: Bloquer questions pendant erreur                         │
│  ├── ✅ Fix GAP-03: Mode "Do Not Disturb"                                    │
│  └── ✅ Fix GAP-04: Tutoriels adaptatifs                                     │
│                                                                              │
│  SPRINT 2 (Semaine 3-4): FEEDBACK & ANALYTICS                                │
│  ├── Implémenter feedback loop (GAP-05)                                      │
│  ├── Dashboard progression utilisateur                                       │
│  └── A/B testing questions                                                   │
│                                                                              │
│  SPRINT 3 (Semaine 5-6): EXPANSION                                           │
│  ├── Nouvelles questions par sphère                                          │
│  ├── Tutoriels XR                                                            │
│  └── Mode persona "découverte"                                               │
│                                                                              │
│  SPRINT 4 (Semaine 7-8): POLISH                                              │
│  ├── Gamification (badges)                                                   │
│  ├── Vidéos tutoriels                                                        │
│  └── Localisation EN                                                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 9.2 Nouvelles Questions à Implémenter

### Priority 1: Questions Essentielles

```typescript
const NEW_QUESTIONS_P1 = [
  {
    id: 'Q-NEW-001',
    trigger: 'first_business_sphere_access',
    question: "Travaillez-vous seul ou en équipe?",
    options: ['Seul/Freelance', 'Petite équipe (2-10)', 'Entreprise (+10)'],
    unlocks: ['team_features', 'collaboration_tutorial'],
  },
  {
    id: 'Q-NEW-002',
    trigger: 'upload_property_document',
    question: "C'est votre résidence ou un investissement?",
    options: ['Résidence principale', 'Investissement locatif', 'Les deux'],
    unlocks: ['immobilier_personal', 'immobilier_business'],
  },
  {
    id: 'Q-NEW-003',
    trigger: 'after_3_sessions',
    question: "À quelle heure travaillez-vous habituellement?",
    options: ['Matin (6h-12h)', 'Journée (9h-17h)', 'Soir (17h-23h)', 'Variable'],
    effect: 'optimize_notification_timing',
  },
  {
    id: 'Q-NEW-004',
    trigger: 'first_agent_call',
    question: "Quel niveau de détail préférez-vous dans les explications?",
    options: ['Concis', 'Détaillé', 'Avec exemples'],
    effect: 'adapt_agent_verbosity',
  },
];
```

### Priority 2: Questions Contextualles

```typescript
const NEW_QUESTIONS_P2 = [
  {
    id: 'Q-NEW-005',
    trigger: 'construction_sphere_used',
    question: "Êtes-vous entrepreneur ou donneur d'ouvrage?",
    options: ['Entrepreneur général', 'Sous-traitant', 'Propriétaire/Client'],
    unlocks: ['construction_pro_features'],
  },
  {
    id: 'Q-NEW-006',
    trigger: 'creative_3_uploads',
    question: "Quel est votre objectif principal?",
    options: ['Portfolio personnel', 'Projets clients', 'Hobby créatif'],
    unlocks: ['creative_workflow_appropriate'],
  },
  {
    id: 'Q-NEW-007',
    trigger: 'quebec_location_detected',
    question: "Travaillez-vous avec des normes québécoises (RBQ, TAL)?",
    options: ['Oui, régulièrement', 'Parfois', 'Non'],
    unlocks: ['quebec_compliance_module'],
  },
];
```

## 9.3 Nouveaux Tutoriels à Créer

| ID | Tutoriel | Priorité | Durée | Déblocage |
|----|----------|----------|-------|-----------|
| TUT-NEW-01 | Mode Focus (DND) | P0 | 30s | Premier long workflow |
| TUT-NEW-02 | Personnaliser Nova | P1 | 2min | 10ème interaction Nova |
| TUT-NEW-03 | Shortcuts & Raccourcis | P1 | 1min | 20ème navigation |
| TUT-NEW-04 | Export & Backup | P1 | 2min | 50+ DataSpaces |
| TUT-NEW-05 | Collaboration Basics | P1 | 3min | Premier partage |
| TUT-NEW-06 | XR Onboarding | P1 | 5min | Premier toggle XR |
| TUT-NEW-07 | Agent Avancé | P2 | 3min | 50+ agent calls |
| TUT-NEW-08 | Intégrations Externes | P2 | 3min | Première connexion API |

---

# 10. IMPLÉMENTATION TECHNIQUE

## 10.1 Schema Base de Données

```sql
-- Table des découvertes utilisateur
CREATE TABLE user_discoveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    -- Type de découverte
    discovery_type VARCHAR(50) NOT NULL,
    discovery_key VARCHAR(100) NOT NULL,
    discovery_value JSONB NOT NULL,
    
    -- Scoring
    signal_count INTEGER DEFAULT 1,
    confidence_score DECIMAL(3,2) DEFAULT 0.1,
    
    -- Timing
    first_detected_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW(),
    
    -- Consent
    user_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    
    -- Audit
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, identity_id, discovery_type, discovery_key)
);

-- Table des tutoriels utilisateur
CREATE TABLE user_tutorials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    tutorial_id VARCHAR(20) NOT NULL,
    
    -- État
    status VARCHAR(20) DEFAULT 'locked', -- locked, unlocked, in_progress, completed, skipped
    
    -- Progression
    current_step INTEGER DEFAULT 0,
    total_steps INTEGER NOT NULL,
    time_spent_seconds INTEGER DEFAULT 0,
    
    -- Timing
    unlocked_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Metadata
    unlock_trigger VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, tutorial_id)
);

-- Table des besoins détectés
CREATE TABLE detected_needs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Need info
    need_category VARCHAR(50) NOT NULL,
    need_id VARCHAR(100) NOT NULL,
    
    -- Scoring
    score INTEGER DEFAULT 0,
    confidence DECIMAL(3,2) DEFAULT 0,
    urgency VARCHAR(20) DEFAULT 'low',
    
    -- Actions
    suggestion_shown BOOLEAN DEFAULT FALSE,
    suggestion_shown_at TIMESTAMP,
    user_response VARCHAR(20), -- accepted, declined, ignored
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, need_category, need_id)
);

-- Table des questions Nova
CREATE TABLE nova_questions_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Question
    question_id VARCHAR(20) NOT NULL,
    question_text TEXT NOT NULL,
    context_trigger VARCHAR(100),
    
    -- Réponse
    response_given BOOLEAN DEFAULT FALSE,
    response_value TEXT,
    response_time_seconds INTEGER,
    
    -- Timing
    asked_at TIMESTAMP DEFAULT NOW(),
    responded_at TIMESTAMP,
    
    -- Metadata
    sphere_context VARCHAR(50),
    was_skipped BOOLEAN DEFAULT FALSE
);

-- Index pour performance
CREATE INDEX idx_discoveries_user ON user_discoveries(user_id, identity_id);
CREATE INDEX idx_tutorials_user ON user_tutorials(user_id, status);
CREATE INDEX idx_needs_user ON detected_needs(user_id, score DESC);
CREATE INDEX idx_questions_user ON nova_questions_log(user_id, asked_at DESC);
```

## 10.2 API Endpoints

```typescript
// Discovery API
POST   /api/v1/nova/discoveries              // Log new discovery
GET    /api/v1/nova/discoveries              // Get user discoveries
PATCH  /api/v1/nova/discoveries/:id/acknowledge  // User acknowledges
DELETE /api/v1/nova/discoveries/:id          // User deletes

// Tutorial API
GET    /api/v1/tutorials                     // List all tutorials + status
GET    /api/v1/tutorials/:id                 // Get tutorial content
POST   /api/v1/tutorials/:id/start           // Start tutorial
PATCH  /api/v1/tutorials/:id/progress        // Update progress
POST   /api/v1/tutorials/:id/complete        // Mark complete
POST   /api/v1/tutorials/:id/skip            // Skip tutorial

// Need Detection API
GET    /api/v1/nova/needs                    // Get detected needs
POST   /api/v1/nova/needs/:id/respond        // User response to suggestion

// Question API
GET    /api/v1/nova/questions/pending        // Get pending contextual question
POST   /api/v1/nova/questions/:id/respond    // Submit response
POST   /api/v1/nova/questions/:id/skip       // Skip question
```

## 10.3 Frontend Hooks

```typescript
// Hook principal Nova Profiling
export function useNovaProfiler() {
  // Tracker d'actions pour pattern detection
  const trackAction = useCallback((action: UserAction) => {
    api.post('/nova/discoveries', {
      type: 'action',
      action: action.type,
      context: action.context,
    });
  }, []);
  
  // Récupérer question contextuelle si disponible
  const { data: pendingQuestion } = useQuery(
    'nova-pending-question',
    () => api.get('/nova/questions/pending'),
    { refetchInterval: 30000 } // Check every 30s
  );
  
  // Tutoriels disponibles
  const { data: tutorials } = useQuery(
    'user-tutorials',
    () => api.get('/tutorials')
  );
  
  return {
    trackAction,
    pendingQuestion,
    tutorials,
    unlockedTutorials: tutorials?.filter(t => t.status === 'unlocked'),
    completedTutorials: tutorials?.filter(t => t.status === 'completed'),
  };
}

// Hook pour afficher question Nova
export function useNovaQuestion(questionId: string) {
  const respondMutation = useMutation(
    (response: string) => api.post(`/nova/questions/${questionId}/respond`, { response })
  );
  
  const skipMutation = useMutation(
    () => api.post(`/nova/questions/${questionId}/skip`)
  );
  
  return {
    respond: respondMutation.mutate,
    skip: skipMutation.mutate,
    isLoading: respondMutation.isLoading || skipMutation.isLoading,
  };
}

// Hook pour tutoriels
export function useTutorial(tutorialId: string) {
  const { data: tutorial } = useQuery(
    ['tutorial', tutorialId],
    () => api.get(`/tutorials/${tutorialId}`)
  );
  
  const startMutation = useMutation(() => 
    api.post(`/tutorials/${tutorialId}/start`)
  );
  
  const progressMutation = useMutation((step: number) =>
    api.patch(`/tutorials/${tutorialId}/progress`, { step })
  );
  
  const completeMutation = useMutation(() =>
    api.post(`/tutorials/${tutorialId}/complete`)
  );
  
  return {
    tutorial,
    start: startMutation.mutate,
    updateProgress: progressMutation.mutate,
    complete: completeMutation.mutate,
  };
}
```

---

# 📊 RÉSUMÉ & MÉTRIQUES

## KPIs de Succès

| Métrique | Cible | Mesure |
|----------|-------|--------|
| Tutoriels complétés | > 70% unlocked | completion_rate |
| Questions répondues | > 50% asked | response_rate |
| Suggestions acceptées | > 40% shown | acceptance_rate |
| Time to first value | < 5 minutes | onboarding_time |
| User retention D7 | > 60% | retention_metric |

## Checklist Implémentation

- [ ] Schema DB créé et migré
- [ ] Endpoints API implémentés
- [ ] Frontend hooks créés
- [ ] 5 tutoriels Tier 0 prêts
- [ ] 10 questions contextuelles configurées
- [ ] Nova states implémentés
- [ ] Feedback loop actif
- [ ] Analytics dashboard

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    NOVA PROGRESSIVE PROFILING COMPLETE                       ║
║                                                                              ║
║                    "Apprendre sans jamais interroger"                        ║
║                    "Guider sans jamais imposer"                              ║
║                    "Personnaliser sans jamais envahir"                       ║
║                                                                              ║
║                           ON CONTINUE! 💪🔥                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

*Document créé le 23 Décembre 2025*
*CHE·NU™ — The Governed Intelligence Operating System*
