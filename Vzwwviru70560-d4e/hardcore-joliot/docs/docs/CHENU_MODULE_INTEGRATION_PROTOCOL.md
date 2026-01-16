# 🔌 CHE·NU™ — PROTOCOLE D'INTÉGRATION MODULES

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           🔌 MODULE INTEGRATION PROTOCOL (MIP)                               ║
║                                                                              ║
║     "Chaque module s'intègre dans l'écosystème Nova automatiquement"        ║
║                                                                              ║
║              STANDARD OBLIGATOIRE POUR TOUT NOUVEAU MODULE                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Version**: 1.0
**Date**: 23 Décembre 2025
**Statut**: OBLIGATOIRE — Aucun module ne peut être intégré sans suivre ce protocole

---

## 📋 TABLE DES MATIÈRES

1. [PHILOSOPHIE D'INTÉGRATION](#1-philosophie-dintégration)
2. [CHECKLIST INTÉGRATION COMPLÈTE](#2-checklist-intégration-complète)
3. [MODULE MANIFEST (OBLIGATOIRE)](#3-module-manifest)
4. [HOOKS NOVA OBLIGATOIRES](#4-hooks-nova-obligatoires)
5. [PIÈCES DU PUZZLE À DÉFINIR](#5-pièces-du-puzzle-à-définir)
6. [SYSTÈME DE TUTORIELS MODULE](#6-système-de-tutoriels-module)
7. [QUESTIONS DE DÉCOUVERTE MODULE](#7-questions-de-découverte-module)
8. [REGISTRY CENTRAL NOVA](#8-registry-central-nova)
9. [TEMPLATES & EXEMPLES](#9-templates--exemples)
10. [VALIDATION & CERTIFICATION](#10-validation--certification)

---

# 1. PHILOSOPHIE D'INTÉGRATION

## 1.1 Principe Fondamental

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RÈGLE D'OR D'INTÉGRATION                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   UN MODULE N'EXISTE PAS S'IL N'EST PAS INTÉGRÉ DANS NOVA                   ║
║                                                                              ║
║   Chaque module DOIT:                                                        ║
║   ├── Se déclarer au Registry Nova                                           ║
║   ├── Définir ses besoins informationnels                                    ║
║   ├── Fournir ses explications Nova                                          ║
║   ├── Définir ses tutoriels                                                  ║
║   ├── Spécifier ses triggers de découverte                                   ║
║   └── Déclarer ses dépendances avec autres modules                          ║
║                                                                              ║
║   Sans ça = Module orphelin = INTERDIT                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 1.2 Les 7 Couches d'Intégration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    7 COUCHES D'INTÉGRATION MODULE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  COUCHE 7: ANALYTICS & FEEDBACK                                             │
│  └── Métriques usage, feedback loop, amélioration continue                 │
│                                                                             │
│  COUCHE 6: TUTORIELS & APPRENTISSAGE                                        │
│  └── Mini-tutoriels, guides contextuels, progression                       │
│                                                                             │
│  COUCHE 5: DÉCOUVERTE & PROFILING                                           │
│  └── Questions Nova, détection patterns, pièces puzzle                     │
│                                                                             │
│  COUCHE 4: PRÉSENTATION & EXPLICATIONS                                      │
│  └── Messages Nova, tooltips, descriptions                                  │
│                                                                             │
│  COUCHE 3: GOUVERNANCE & PERMISSIONS                                        │
│  └── Tokens requis, permissions, identity scoping                          │
│                                                                             │
│  COUCHE 2: NAVIGATION & UI                                                  │
│  └── Placement dans sphère/bureau, icônes, routes                          │
│                                                                             │
│  COUCHE 1: CORE FONCTIONNEL                                                 │
│  └── Backend, API, database, logique métier                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 Ordre d'Intégration Obligatoire

```
   DÉVELOPPEMENT              INTÉGRATION NOVA              DÉPLOIEMENT
   ─────────────              ────────────────              ───────────
                                    
   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Core    │───▶│ Module  │───▶│ Nova    │───▶│ Valid.  │───▶│ Deploy  │
   │ Code    │    │ Manifest│    │ Registry│    │ & Test  │    │         │
   └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
       │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼
   Backend +      Déclarer       Enregistrer    Tester tous    Activer
   Frontend       toutes les     dans Nova      les hooks      pour
   prêts          métadonnées    Central        Nova           users
```

---

# 2. CHECKLIST INTÉGRATION COMPLÈTE

## 2.1 Checklist Maître (30 Points)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHECKLIST INTÉGRATION MODULE                              ║
║                    (Tous les points sont OBLIGATOIRES)                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  📁 PHASE 1: MANIFEST (8 points)                                            ║
║  □ 1.1  Créer fichier module.manifest.json                                  ║
║  □ 1.2  Définir identité module (id, nom, version)                          ║
║  □ 1.3  Déclarer sphère(s) parente(s)                                       ║
║  □ 1.4  Déclarer section bureau cible                                       ║
║  □ 1.5  Définir dépendances (autres modules requis)                         ║
║  □ 1.6  Définir conflits (modules incompatibles)                            ║
║  □ 1.7  Déclarer coût token base                                            ║
║  □ 1.8  Définir permissions requises                                        ║
║                                                                              ║
║  🗣️ PHASE 2: NOVA EXPLICATIONS (6 points)                                   ║
║  □ 2.1  Écrire description courte (< 50 mots)                               ║
║  □ 2.2  Écrire description longue (< 200 mots)                              ║
║  □ 2.3  Définir message première découverte                                 ║
║  □ 2.4  Définir messages contextuels (min 3)                                ║
║  □ 2.5  Définir tooltips éléments UI (tous)                                 ║
║  □ 2.6  Traduire FR + EN                                                    ║
║                                                                              ║
║  🧩 PHASE 3: PUZZLE INFORMATIONNEL (5 points)                               ║
║  □ 3.1  Lister pièces info requises                                         ║
║  □ 3.2  Définir ordre de collecte                                           ║
║  □ 3.3  Créer questions de découverte                                       ║
║  □ 3.4  Définir triggers de détection                                       ║
║  □ 3.5  Mapper déblocages conditionnels                                     ║
║                                                                              ║
║  🎓 PHASE 4: TUTORIELS (5 points)                                           ║
║  □ 4.1  Créer tutoriel introduction (obligatoire)                           ║
║  □ 4.2  Créer tutoriels features (1 par feature majeure)                    ║
║  □ 4.3  Définir conditions déblocage tutoriels                              ║
║  □ 4.4  Créer tutoriels imbriqués si applicable                             ║
║  □ 4.5  Tester parcours complet                                             ║
║                                                                              ║
║  🔗 PHASE 5: REGISTRY & HOOKS (4 points)                                    ║
║  □ 5.1  Enregistrer dans Nova Registry                                      ║
║  □ 5.2  Implémenter hooks événements                                        ║
║  □ 5.3  Connecter analytics                                                 ║
║  □ 5.4  Valider intégration end-to-end                                      ║
║                                                                              ║
║  ✅ PHASE 6: VALIDATION (2 points)                                          ║
║  □ 6.1  Passer tests automatisés Nova                                       ║
║  □ 6.2  Review par équipe Nova                                              ║
║                                                                              ║
║  SCORE MINIMUM POUR DÉPLOIEMENT: 30/30                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 2.2 Checklist Rapide (Version Imprimable)

```
INTÉGRATION MODULE: _________________ DATE: _________

PHASE 1 - MANIFEST
□ module.manifest.json créé
□ Identité complète
□ Sphère(s) déclarée(s)
□ Section bureau définie
□ Dépendances listées
□ Conflits listés
□ Coût token défini
□ Permissions définies

PHASE 2 - NOVA EXPLICATIONS
□ Description courte
□ Description longue
□ Message première découverte
□ Messages contextuels (3+)
□ Tooltips complets
□ Traductions FR/EN

PHASE 3 - PUZZLE
□ Pièces info listées
□ Ordre collecte défini
□ Questions découverte
□ Triggers détection
□ Déblocages mappés

PHASE 4 - TUTORIELS
□ Tuto introduction
□ Tutos features
□ Conditions déblocage
□ Tutos imbriqués
□ Parcours testé

PHASE 5 - REGISTRY
□ Nova Registry OK
□ Hooks implémentés
□ Analytics connecté
□ E2E validé

PHASE 6 - VALIDATION
□ Tests auto passés
□ Review équipe OK

SIGNATURE: _____________ VALIDÉ: □
```

---

# 3. MODULE MANIFEST (OBLIGATOIRE)

## 3.1 Structure du Manifest

```typescript
// Fichier: modules/[module-name]/module.manifest.ts

export interface ModuleManifest {
  // ═══════════════════════════════════════════════════════════════
  // SECTION 1: IDENTITÉ
  // ═══════════════════════════════════════════════════════════════
  identity: {
    id: string;                    // Unique: "mod-immobilier-rental"
    name: string;                  // "Gestion Locative"
    nameFr: string;                // "Gestion Locative"
    nameEn: string;                // "Rental Management"
    version: string;               // "1.0.0"
    icon: string;                  // "🏘️" ou path icône
    color: string;                 // Couleur thème module
    author: string;                // Équipe/développeur
    category: ModuleCategory;      // 'core' | 'domain' | 'addon'
  };

  // ═══════════════════════════════════════════════════════════════
  // SECTION 2: PLACEMENT
  // ═══════════════════════════════════════════════════════════════
  placement: {
    spheres: SphereId[];           // ['personal', 'business']
    primarySphere: SphereId;       // 'business'
    bureauSection: BureauSection;  // 'projects' | 'data' | etc.
    navigation: {
      showInSidebar: boolean;
      showInQuickAccess: boolean;
      menuOrder: number;           // Position dans menu
    };
    routes: {
      base: string;                // '/immobilier/rental'
      children: RouteConfig[];     // Sous-routes
    };
  };

  // ═══════════════════════════════════════════════════════════════
  // SECTION 3: DÉPENDANCES & CONFLITS
  // ═══════════════════════════════════════════════════════════════
  dependencies: {
    required: ModuleDependency[];   // Modules obligatoires
    optional: ModuleDependency[];   // Modules recommandés
    conflicts: string[];            // Modules incompatibles
  };

  // ═══════════════════════════════════════════════════════════════
  // SECTION 4: GOUVERNANCE
  // ═══════════════════════════════════════════════════════════════
  governance: {
    tokenCost: {
      base: number;                // Coût base par action
      perItem: number;             // Coût par élément traité
      aiFeatures: Record<string, number>; // Coûts features IA
    };
    permissions: {
      required: Permission[];       // Permissions nécessaires
      optional: Permission[];       // Permissions optionnelles
    };
    dataScope: {
      identityBound: boolean;       // Lié à une identité
      crossIdentityAllowed: boolean; // Accès cross-identity
      exportable: boolean;          // Données exportables
    };
  };

  // ═══════════════════════════════════════════════════════════════
  // SECTION 5: NOVA INTEGRATION (CRITIQUE)
  // ═══════════════════════════════════════════════════════════════
  nova: NovaIntegration;           // Voir section dédiée

  // ═══════════════════════════════════════════════════════════════
  // SECTION 6: FEATURES
  // ═══════════════════════════════════════════════════════════════
  features: ModuleFeature[];       // Liste des fonctionnalités

  // ═══════════════════════════════════════════════════════════════
  // SECTION 7: ANALYTICS
  // ═══════════════════════════════════════════════════════════════
  analytics: {
    trackingEvents: AnalyticsEvent[];
    kpis: ModuleKPI[];
  };
}
```

## 3.2 Section Nova Integration (Détaillée)

```typescript
interface NovaIntegration {
  // ═══════════════════════════════════════════════════════════════
  // 5.1 EXPLICATIONS NOVA
  // ═══════════════════════════════════════════════════════════════
  explanations: {
    // Description courte (pour listes, tooltips)
    short: {
      fr: string;  // Max 50 mots
      en: string;
    };
    
    // Description longue (pour pages info)
    long: {
      fr: string;  // Max 200 mots
      en: string;
    };
    
    // Message première découverte
    firstDiscovery: {
      fr: string;
      en: string;
      displayTrigger: 'first_visit' | 'first_action' | 'manual';
    };
    
    // Messages contextuels par situation
    contextual: NovaContextualMessage[];
    
    // Tooltips pour éléments UI
    tooltips: Record<string, { fr: string; en: string }>;
  };

  // ═══════════════════════════════════════════════════════════════
  // 5.2 PUZZLE INFORMATIONNEL
  // ═══════════════════════════════════════════════════════════════
  puzzle: {
    // Pièces d'information nécessaires
    requiredPieces: PuzzlePiece[];
    
    // Ordre de collecte recommandé
    collectionOrder: string[];  // IDs des pièces
    
    // Questions de découverte
    discoveryQuestions: DiscoveryQuestion[];
    
    // Triggers de détection automatique
    detectionTriggers: DetectionTrigger[];
    
    // Déblocages conditionnels
    conditionalUnlocks: ConditionalUnlock[];
  };

  // ═══════════════════════════════════════════════════════════════
  // 5.3 TUTORIELS
  // ═══════════════════════════════════════════════════════════════
  tutorials: {
    // Tutoriel introduction (obligatoire)
    intro: ModuleTutorial;
    
    // Tutoriels features
    features: ModuleTutorial[];
    
    // Tutoriels avancés (déblocables)
    advanced: ModuleTutorial[];
    
    // Tutoriels imbriqués
    nested: NestedTutorial[];
  };

  // ═══════════════════════════════════════════════════════════════
  // 5.4 HOOKS ÉVÉNEMENTS
  // ═══════════════════════════════════════════════════════════════
  hooks: {
    // Événements émis par le module
    emits: ModuleEvent[];
    
    // Événements écoutés
    listensTo: EventSubscription[];
    
    // Callbacks Nova
    callbacks: {
      onModuleLoad?: string;      // Fonction à appeler
      onModuleUnload?: string;
      onUserAction?: string;
      onError?: string;
    };
  };

  // ═══════════════════════════════════════════════════════════════
  // 5.5 VARIANTES DE PARCOURS
  // ═══════════════════════════════════════════════════════════════
  variants: {
    // Parcours selon profil utilisateur
    userProfiles: UserProfileVariant[];
    
    // Parcours selon contexte
    contexts: ContextVariant[];
  };
}
```

## 3.3 Exemple Complet — Module Gestion Locative

```typescript
// modules/immobilier-rental/module.manifest.ts

export const ImmobilierRentalManifest: ModuleManifest = {
  // ═══════════════════════════════════════════════════════════════
  // IDENTITÉ
  // ═══════════════════════════════════════════════════════════════
  identity: {
    id: 'mod-immobilier-rental',
    name: 'Gestion Locative',
    nameFr: 'Gestion Locative',
    nameEn: 'Rental Management',
    version: '1.0.0',
    icon: '🏘️',
    color: '#3F7249', // Jungle Emerald
    author: 'CHE·NU Core Team',
    category: 'domain',
  },

  // ═══════════════════════════════════════════════════════════════
  // PLACEMENT
  // ═══════════════════════════════════════════════════════════════
  placement: {
    spheres: ['personal', 'business'],
    primarySphere: 'business',
    bureauSection: 'projects',
    navigation: {
      showInSidebar: true,
      showInQuickAccess: true,
      menuOrder: 3,
    },
    routes: {
      base: '/immobilier/rental',
      children: [
        { path: '/properties', component: 'PropertiesList' },
        { path: '/properties/:id', component: 'PropertyDetail' },
        { path: '/tenants', component: 'TenantsList' },
        { path: '/leases', component: 'LeasesList' },
        { path: '/payments', component: 'PaymentsTracker' },
        { path: '/maintenance', component: 'MaintenanceBoard' },
        { path: '/analytics', component: 'RentalAnalytics' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // DÉPENDANCES
  // ═══════════════════════════════════════════════════════════════
  dependencies: {
    required: [
      { moduleId: 'mod-dataspace', minVersion: '1.0.0' },
      { moduleId: 'mod-documents', minVersion: '1.0.0' },
    ],
    optional: [
      { moduleId: 'mod-finance', reason: 'Suivi financier avancé' },
      { moduleId: 'mod-calendar', reason: 'Rappels automatiques' },
      { moduleId: 'mod-xr-viewer', reason: 'Visites virtuelles' },
    ],
    conflicts: [],
  },

  // ═══════════════════════════════════════════════════════════════
  // GOUVERNANCE
  // ═══════════════════════════════════════════════════════════════
  governance: {
    tokenCost: {
      base: 5,
      perItem: 2,
      aiFeatures: {
        'lease-analysis': 50,
        'rent-optimization': 100,
        'tenant-screening': 75,
        'maintenance-prediction': 60,
      },
    },
    permissions: {
      required: ['dataspace.read', 'dataspace.write', 'documents.upload'],
      optional: ['finance.read', 'calendar.write', 'xr.view'],
    },
    dataScope: {
      identityBound: true,
      crossIdentityAllowed: false,
      exportable: true,
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // NOVA INTEGRATION
  // ═══════════════════════════════════════════════════════════════
  nova: {
    // EXPLICATIONS
    explanations: {
      short: {
        fr: "Gérez vos propriétés locatives, locataires, baux et paiements en un seul endroit.",
        en: "Manage your rental properties, tenants, leases and payments in one place.",
      },
      long: {
        fr: `La Gestion Locative vous permet de centraliser toute l'administration 
             de vos propriétés en location. Suivez vos locataires, gérez les baux, 
             trackez les paiements de loyer, planifiez la maintenance, et analysez 
             la performance de votre portfolio. Conforme aux réglementations 
             québécoises (TAL) et françaises.`,
        en: `Rental Management centralizes all administration for your rental 
             properties. Track tenants, manage leases, monitor rent payments, 
             plan maintenance, and analyze portfolio performance. Compliant 
             with Quebec (TAL) and French regulations.`,
      },
      firstDiscovery: {
        fr: `Bienvenue dans la Gestion Locative! Ici, vous pouvez gérer vos 
             propriétés en location. Commencez par ajouter votre première propriété.`,
        en: `Welcome to Rental Management! Here you can manage your rental 
             properties. Start by adding your first property.`,
        displayTrigger: 'first_visit',
      },
      contextual: [
        {
          id: 'ctx-add-property',
          trigger: 'click_add_property',
          message: {
            fr: "Ajoutez les informations de base. Vous pourrez compléter plus tard.",
            en: "Add basic information. You can complete details later.",
          },
        },
        {
          id: 'ctx-first-tenant',
          trigger: 'first_tenant_added',
          message: {
            fr: "Premier locataire ajouté! Voulez-vous créer un bail maintenant?",
            en: "First tenant added! Would you like to create a lease now?",
          },
        },
        {
          id: 'ctx-payment-due',
          trigger: 'payment_approaching',
          message: {
            fr: "Un loyer arrive à échéance dans 5 jours.",
            en: "A rent payment is due in 5 days.",
          },
        },
        {
          id: 'ctx-lease-expiring',
          trigger: 'lease_expiring_30d',
          message: {
            fr: "Un bail expire dans 30 jours. Pensez au renouvellement.",
            en: "A lease expires in 30 days. Consider renewal.",
          },
        },
      ],
      tooltips: {
        'btn-add-property': {
          fr: "Ajouter une nouvelle propriété à votre portfolio",
          en: "Add a new property to your portfolio",
        },
        'btn-add-tenant': {
          fr: "Enregistrer un nouveau locataire",
          en: "Register a new tenant",
        },
        'view-analytics': {
          fr: "Voir les statistiques de rentabilité",
          en: "View profitability statistics",
        },
        'tal-compliance': {
          fr: "Vérifier la conformité TAL (Tribunal Administratif du Logement)",
          en: "Check TAL compliance (Administrative Housing Tribunal)",
        },
      },
    },

    // PUZZLE INFORMATIONNEL
    puzzle: {
      requiredPieces: [
        {
          id: 'piece-property-count',
          name: 'Nombre de propriétés',
          priority: 'essential',
          source: 'detection',
          affectsExperience: true,
        },
        {
          id: 'piece-rental-type',
          name: 'Type de location',
          priority: 'essential',
          source: 'question',
          options: ['Résidentiel', 'Commercial', 'Mixte'],
          affectsExperience: true,
        },
        {
          id: 'piece-jurisdiction',
          name: 'Juridiction',
          priority: 'essential',
          source: 'detection',
          affectsExperience: true, // Change templates/règles
        },
        {
          id: 'piece-management-style',
          name: 'Style de gestion',
          priority: 'useful',
          source: 'question',
          options: ['Auto-gestion', 'Avec gestionnaire', 'Mixte'],
          affectsExperience: false,
        },
        {
          id: 'piece-tenant-count',
          name: 'Nombre de locataires',
          priority: 'useful',
          source: 'detection',
          affectsExperience: false,
        },
      ],
      
      collectionOrder: [
        'piece-property-count',   // 1. Combien de propriétés?
        'piece-rental-type',      // 2. Quel type?
        'piece-jurisdiction',     // 3. Où? (détection auto)
        'piece-management-style', // 4. Comment gérez-vous?
        'piece-tenant-count',     // 5. Combien de locataires? (détection)
      ],
      
      discoveryQuestions: [
        {
          id: 'q-rental-type',
          pieceId: 'piece-rental-type',
          trigger: 'first_property_added',
          question: {
            fr: "Quel type de location gérez-vous principalement?",
            en: "What type of rental do you mainly manage?",
          },
          options: [
            { value: 'residential', label: { fr: 'Résidentiel', en: 'Residential' } },
            { value: 'commercial', label: { fr: 'Commercial', en: 'Commercial' } },
            { value: 'mixed', label: { fr: 'Mixte', en: 'Mixed' } },
          ],
          skippable: true,
          timing: 'after_action',
        },
        {
          id: 'q-management-style',
          pieceId: 'piece-management-style',
          trigger: 'third_property_added',
          question: {
            fr: "Comment gérez-vous vos propriétés?",
            en: "How do you manage your properties?",
          },
          options: [
            { value: 'self', label: { fr: 'Je gère moi-même', en: 'Self-managed' } },
            { value: 'manager', label: { fr: 'Avec un gestionnaire', en: 'With a manager' } },
            { value: 'mixed', label: { fr: 'Ça dépend', en: 'It depends' } },
          ],
          skippable: true,
          timing: 'session_end',
        },
      ],
      
      detectionTriggers: [
        {
          id: 'detect-property-count',
          pieceId: 'piece-property-count',
          event: 'property_created',
          aggregation: 'count',
          thresholds: [
            { value: 1, label: 'Débutant' },
            { value: 5, label: 'Intermédiaire' },
            { value: 10, label: 'Portfolio' },
            { value: 25, label: 'Pro' },
          ],
        },
        {
          id: 'detect-jurisdiction-qc',
          pieceId: 'piece-jurisdiction',
          event: 'document_uploaded',
          pattern: 'tal|tribunal|bail_quebec|regie',
          value: 'quebec',
        },
        {
          id: 'detect-jurisdiction-fr',
          pieceId: 'piece-jurisdiction',
          event: 'document_uploaded',
          pattern: 'bail_france|loi_alur|apl',
          value: 'france',
        },
      ],
      
      conditionalUnlocks: [
        {
          id: 'unlock-tal-tools',
          condition: { piece: 'piece-jurisdiction', value: 'quebec' },
          unlocks: ['feature-tal-compliance', 'tut-tal-basics'],
        },
        {
          id: 'unlock-portfolio-analytics',
          condition: { piece: 'piece-property-count', minValue: 5 },
          unlocks: ['feature-portfolio-analytics', 'tut-portfolio-analysis'],
        },
        {
          id: 'unlock-commercial-tools',
          condition: { piece: 'piece-rental-type', value: 'commercial' },
          unlocks: ['feature-commercial-lease', 'tut-commercial-rental'],
        },
      ],
    },

    // TUTORIELS
    tutorials: {
      intro: {
        id: 'tut-rental-intro',
        title: { fr: 'Introduction Gestion Locative', en: 'Rental Management Intro' },
        duration: '2min',
        unlockCondition: 'first_visit',
        steps: [
          {
            id: 'step-1',
            title: { fr: 'Bienvenue', en: 'Welcome' },
            content: {
              fr: "La Gestion Locative centralise tout ce dont vous avez besoin pour gérer vos propriétés en location.",
              en: "Rental Management centralizes everything you need to manage your rental properties.",
            },
            highlight: null,
          },
          {
            id: 'step-2',
            title: { fr: 'Vos Propriétés', en: 'Your Properties' },
            content: {
              fr: "Commencez par ajouter vos propriétés. Chaque propriété a son propre espace de données.",
              en: "Start by adding your properties. Each property has its own data space.",
            },
            highlight: '#btn-add-property',
          },
          {
            id: 'step-3',
            title: { fr: 'Locataires & Baux', en: 'Tenants & Leases' },
            content: {
              fr: "Ajoutez vos locataires et créez des baux. Tout est lié automatiquement.",
              en: "Add your tenants and create leases. Everything links automatically.",
            },
            highlight: '#nav-tenants',
          },
          {
            id: 'step-4',
            title: { fr: 'Suivi Paiements', en: 'Payment Tracking' },
            content: {
              fr: "Suivez les loyers, recevez des alertes, gérez les retards.",
              en: "Track rent, receive alerts, manage late payments.",
            },
            highlight: '#nav-payments',
          },
        ],
      },
      
      features: [
        {
          id: 'tut-add-property',
          title: { fr: 'Ajouter une Propriété', en: 'Add a Property' },
          duration: '1min',
          unlockCondition: 'click_add_property_first_time',
          steps: [/* ... */],
        },
        {
          id: 'tut-create-lease',
          title: { fr: 'Créer un Bail', en: 'Create a Lease' },
          duration: '2min',
          unlockCondition: 'first_tenant_added',
          steps: [/* ... */],
        },
        {
          id: 'tut-payment-tracking',
          title: { fr: 'Suivi des Paiements', en: 'Payment Tracking' },
          duration: '1min',
          unlockCondition: 'first_lease_created',
          steps: [/* ... */],
        },
      ],
      
      advanced: [
        {
          id: 'tut-tal-basics',
          title: { fr: 'Conformité TAL', en: 'TAL Compliance' },
          duration: '3min',
          unlockCondition: { piece: 'piece-jurisdiction', value: 'quebec' },
          steps: [/* ... */],
        },
        {
          id: 'tut-portfolio-analysis',
          title: { fr: 'Analyse de Portfolio', en: 'Portfolio Analysis' },
          duration: '3min',
          unlockCondition: { piece: 'piece-property-count', minValue: 5 },
          steps: [/* ... */],
        },
      ],
      
      nested: [
        {
          parentId: 'tut-create-lease',
          childId: 'tut-lease-renewal',
          unlockAfterCompletion: true,
          delay: '7d', // Déblocage 7 jours après
        },
        {
          parentId: 'tut-payment-tracking',
          childId: 'tut-late-payment-handling',
          unlockCondition: 'first_late_payment_detected',
        },
      ],
    },

    // HOOKS ÉVÉNEMENTS
    hooks: {
      emits: [
        { event: 'rental.property.created', data: ['propertyId', 'type'] },
        { event: 'rental.tenant.added', data: ['tenantId', 'propertyId'] },
        { event: 'rental.lease.created', data: ['leaseId', 'propertyId', 'tenantId'] },
        { event: 'rental.payment.recorded', data: ['paymentId', 'amount', 'status'] },
        { event: 'rental.payment.late', data: ['leaseId', 'daysLate'] },
        { event: 'rental.lease.expiring', data: ['leaseId', 'daysRemaining'] },
        { event: 'rental.maintenance.created', data: ['maintenanceId', 'propertyId'] },
      ],
      listensTo: [
        { event: 'document.uploaded', handler: 'handleDocumentUpload' },
        { event: 'calendar.reminder', handler: 'handleCalendarReminder' },
        { event: 'finance.transaction', handler: 'handleFinanceTransaction' },
      ],
      callbacks: {
        onModuleLoad: 'initializeRentalModule',
        onModuleUnload: 'cleanupRentalModule',
        onUserAction: 'trackRentalAction',
        onError: 'handleRentalError',
      },
    },

    // VARIANTES DE PARCOURS
    variants: {
      userProfiles: [
        {
          profileId: 'first-time-landlord',
          conditions: { 'piece-property-count': { max: 1 } },
          adjustments: {
            tutorialDepth: 'detailed',
            tooltipsFrequency: 'high',
            novaProactivity: 'high',
          },
        },
        {
          profileId: 'experienced-landlord',
          conditions: { 'piece-property-count': { min: 10 } },
          adjustments: {
            tutorialDepth: 'minimal',
            tooltipsFrequency: 'low',
            novaProactivity: 'low',
            showAdvancedFeatures: true,
          },
        },
        {
          profileId: 'property-manager',
          conditions: { 'piece-management-style': 'manager' },
          adjustments: {
            showBulkActions: true,
            showReporting: true,
            multiPropertyView: 'default',
          },
        },
      ],
      contexts: [
        {
          contextId: 'quebec-residential',
          conditions: {
            'piece-jurisdiction': 'quebec',
            'piece-rental-type': 'residential',
          },
          adjustments: {
            enableTalTools: true,
            leaseTemplates: 'quebec-tal',
            showRegieLinks: true,
          },
        },
        {
          contextId: 'france-residential',
          conditions: {
            'piece-jurisdiction': 'france',
            'piece-rental-type': 'residential',
          },
          adjustments: {
            enableAlurTools: true,
            leaseTemplates: 'france-alur',
            showAplInfo: true,
          },
        },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // FEATURES
  // ═══════════════════════════════════════════════════════════════
  features: [
    {
      id: 'feature-property-management',
      name: { fr: 'Gestion Propriétés', en: 'Property Management' },
      core: true,
    },
    {
      id: 'feature-tenant-management',
      name: { fr: 'Gestion Locataires', en: 'Tenant Management' },
      core: true,
    },
    {
      id: 'feature-lease-management',
      name: { fr: 'Gestion Baux', en: 'Lease Management' },
      core: true,
    },
    {
      id: 'feature-payment-tracking',
      name: { fr: 'Suivi Paiements', en: 'Payment Tracking' },
      core: true,
    },
    {
      id: 'feature-maintenance',
      name: { fr: 'Maintenance', en: 'Maintenance' },
      core: true,
    },
    {
      id: 'feature-tal-compliance',
      name: { fr: 'Conformité TAL', en: 'TAL Compliance' },
      core: false,
      unlockCondition: { piece: 'piece-jurisdiction', value: 'quebec' },
    },
    {
      id: 'feature-portfolio-analytics',
      name: { fr: 'Analytics Portfolio', en: 'Portfolio Analytics' },
      core: false,
      unlockCondition: { piece: 'piece-property-count', minValue: 5 },
    },
  ],

  // ═══════════════════════════════════════════════════════════════
  // ANALYTICS
  // ═══════════════════════════════════════════════════════════════
  analytics: {
    trackingEvents: [
      { event: 'module_opened', category: 'engagement' },
      { event: 'property_added', category: 'action' },
      { event: 'lease_created', category: 'action' },
      { event: 'payment_recorded', category: 'action' },
      { event: 'tutorial_completed', category: 'learning' },
      { event: 'feature_used', category: 'feature_adoption' },
    ],
    kpis: [
      { id: 'adoption_rate', name: 'Taux adoption', target: 0.7 },
      { id: 'tutorial_completion', name: 'Tutoriels complétés', target: 0.8 },
      { id: 'feature_depth', name: 'Profondeur utilisation', target: 0.5 },
      { id: 'return_rate', name: 'Taux retour 7j', target: 0.6 },
    ],
  },
};

export default ImmobilierRentalManifest;
```

---

# 4. HOOKS NOVA OBLIGATOIRES

## 4.1 Liste des Hooks à Implémenter

```typescript
// ═══════════════════════════════════════════════════════════════════════════
// HOOKS NOVA OBLIGATOIRES POUR TOUT MODULE
// ═══════════════════════════════════════════════════════════════════════════

export interface NovaHooks {
  // ───────────────────────────────────────────────────────────────
  // HOOK 1: MODULE LIFECYCLE
  // ───────────────────────────────────────────────────────────────
  onModuleLoad: () => Promise<void>;
  // Appelé quand le module est chargé
  // DOIT: Enregistrer le module dans Nova Registry
  
  onModuleUnload: () => Promise<void>;
  // Appelé quand le module est déchargé
  // DOIT: Nettoyer les listeners, sauvegarder état
  
  onModuleError: (error: ModuleError) => Promise<void>;
  // Appelé sur erreur module
  // DOIT: Logger, notifier Nova si critique

  // ───────────────────────────────────────────────────────────────
  // HOOK 2: USER ACTIONS
  // ───────────────────────────────────────────────────────────────
  onUserAction: (action: UserAction) => Promise<void>;
  // Appelé à CHAQUE action utilisateur
  // DOIT: Envoyer à Nova pour pattern detection
  
  onFirstAction: (actionType: string) => Promise<void>;
  // Appelé la PREMIÈRE fois qu'un type d'action est effectué
  // DOIT: Déclencher tutoriel contextuel si défini

  // ───────────────────────────────────────────────────────────────
  // HOOK 3: DISCOVERY & PROFILING
  // ───────────────────────────────────────────────────────────────
  onPuzzlePieceDetected: (piece: PuzzlePiece) => Promise<void>;
  // Appelé quand une pièce du puzzle est détectée
  // DOIT: Mettre à jour profil, vérifier déblocages
  
  onQuestionAnswered: (question: DiscoveryQuestion, answer: any) => Promise<void>;
  // Appelé quand user répond à une question
  // DOIT: Stocker réponse, mettre à jour profil
  
  onQuestionSkipped: (question: DiscoveryQuestion) => Promise<void>;
  // Appelé quand user skip une question
  // DOIT: Logger, ne pas re-poser avant délai

  // ───────────────────────────────────────────────────────────────
  // HOOK 4: TUTORIALS
  // ───────────────────────────────────────────────────────────────
  onTutorialUnlocked: (tutorial: ModuleTutorial) => Promise<void>;
  // Appelé quand un tutoriel est débloqué
  // DOIT: Notifier user si pertinent
  
  onTutorialStarted: (tutorial: ModuleTutorial) => Promise<void>;
  // Appelé au début d'un tutoriel
  // DOIT: Logger, tracker temps
  
  onTutorialCompleted: (tutorial: ModuleTutorial) => Promise<void>;
  // Appelé à la fin d'un tutoriel
  // DOIT: Marquer complété, vérifier déblocages imbriqués
  
  onTutorialSkipped: (tutorial: ModuleTutorial) => Promise<void>;
  // Appelé si tutoriel skippé
  // DOIT: Logger, proposer à nouveau plus tard

  // ───────────────────────────────────────────────────────────────
  // HOOK 5: CONTEXTUAL MESSAGES
  // ───────────────────────────────────────────────────────────────
  onContextTriggered: (context: string) => Promise<NovaMessage | null>;
  // Appelé quand un contexte est détecté
  // RETOURNE: Message Nova à afficher ou null

  // ───────────────────────────────────────────────────────────────
  // HOOK 6: FEATURE UNLOCKS
  // ───────────────────────────────────────────────────────────────
  onFeatureUnlocked: (feature: ModuleFeature) => Promise<void>;
  // Appelé quand une feature est débloquée
  // DOIT: Notifier user, mettre à jour UI
  
  checkFeatureAccess: (featureId: string) => Promise<boolean>;
  // Vérifie si user a accès à une feature
  // RETOURNE: true si accès autorisé

  // ───────────────────────────────────────────────────────────────
  // HOOK 7: ANALYTICS
  // ───────────────────────────────────────────────────────────────
  trackEvent: (event: AnalyticsEvent) => Promise<void>;
  // Track un événement analytics
  // DOIT: Envoyer au système analytics
}
```

## 4.2 Implémentation Type

```typescript
// modules/[module-name]/nova-hooks.ts

import { NovaRegistry } from '@chenu/nova-core';
import { ModuleManifest } from './module.manifest';

export class ModuleNovaHooks implements NovaHooks {
  private manifest: ModuleManifest;
  private registry: NovaRegistry;
  
  constructor(manifest: ModuleManifest) {
    this.manifest = manifest;
    this.registry = NovaRegistry.getInstance();
  }

  // ═══════════════════════════════════════════════════════════════
  // LIFECYCLE HOOKS
  // ═══════════════════════════════════════════════════════════════
  
  async onModuleLoad(): Promise<void> {
    // 1. Enregistrer dans Nova Registry
    await this.registry.registerModule(this.manifest);
    
    // 2. Charger état utilisateur
    const userState = await this.registry.getUserModuleState(this.manifest.identity.id);
    
    // 3. Vérifier si première visite
    if (!userState.hasVisited) {
      await this.registry.queueNovaMessage({
        type: 'first_discovery',
        moduleId: this.manifest.identity.id,
        message: this.manifest.nova.explanations.firstDiscovery,
      });
    }
    
    // 4. Vérifier tutoriels à proposer
    const pendingTutorials = await this.registry.getPendingTutorials(
      this.manifest.identity.id
    );
    if (pendingTutorials.length > 0) {
      await this.registry.notifyTutorialsAvailable(pendingTutorials);
    }
    
    console.log(`[Nova] Module ${this.manifest.identity.id} loaded`);
  }

  async onModuleUnload(): Promise<void> {
    // Sauvegarder état
    await this.registry.saveModuleState(this.manifest.identity.id);
    console.log(`[Nova] Module ${this.manifest.identity.id} unloaded`);
  }

  async onModuleError(error: ModuleError): Promise<void> {
    // Logger erreur
    await this.registry.logError({
      moduleId: this.manifest.identity.id,
      error,
      timestamp: new Date(),
    });
    
    // Si erreur critique, notifier Nova
    if (error.severity === 'critical') {
      await this.registry.queueNovaMessage({
        type: 'error',
        moduleId: this.manifest.identity.id,
        message: {
          fr: "Un problème est survenu. Je travaille à le résoudre.",
          en: "An issue occurred. I'm working to resolve it.",
        },
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // USER ACTION HOOKS
  // ═══════════════════════════════════════════════════════════════
  
  async onUserAction(action: UserAction): Promise<void> {
    // 1. Envoyer à Nova pour pattern detection
    await this.registry.recordAction({
      moduleId: this.manifest.identity.id,
      action,
      timestamp: new Date(),
    });
    
    // 2. Vérifier triggers de détection
    for (const trigger of this.manifest.nova.puzzle.detectionTriggers) {
      if (this.matchesTrigger(action, trigger)) {
        await this.onPuzzlePieceDetected({
          id: trigger.pieceId,
          value: this.extractValue(action, trigger),
          source: 'detection',
        });
      }
    }
    
    // 3. Vérifier messages contextuels
    const contextMessage = await this.onContextTriggered(action.type);
    if (contextMessage) {
      await this.registry.queueNovaMessage(contextMessage);
    }
  }

  async onFirstAction(actionType: string): Promise<void> {
    // Chercher tutoriel associé
    const tutorials = [
      ...this.manifest.nova.tutorials.features,
      ...this.manifest.nova.tutorials.advanced,
    ];
    
    const tutorial = tutorials.find(t => 
      t.unlockCondition === `${actionType}_first_time`
    );
    
    if (tutorial) {
      await this.onTutorialUnlocked(tutorial);
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // DISCOVERY HOOKS
  // ═══════════════════════════════════════════════════════════════
  
  async onPuzzlePieceDetected(piece: DetectedPiece): Promise<void> {
    // 1. Mettre à jour profil utilisateur
    await this.registry.updateUserPuzzle(
      this.manifest.identity.id,
      piece
    );
    
    // 2. Vérifier déblocages conditionnels
    for (const unlock of this.manifest.nova.puzzle.conditionalUnlocks) {
      if (this.matchesUnlockCondition(piece, unlock.condition)) {
        // Débloquer features
        for (const featureId of unlock.unlocks.filter(u => u.startsWith('feature-'))) {
          const feature = this.manifest.features.find(f => f.id === featureId);
          if (feature) {
            await this.onFeatureUnlocked(feature);
          }
        }
        
        // Débloquer tutoriels
        for (const tutorialId of unlock.unlocks.filter(u => u.startsWith('tut-'))) {
          const tutorial = this.findTutorial(tutorialId);
          if (tutorial) {
            await this.onTutorialUnlocked(tutorial);
          }
        }
      }
    }
    
    // 3. Logger découverte
    await this.trackEvent({
      event: 'puzzle_piece_detected',
      category: 'discovery',
      data: { pieceId: piece.id, value: piece.value },
    });
  }

  async onQuestionAnswered(
    question: DiscoveryQuestion, 
    answer: any
  ): Promise<void> {
    // 1. Stocker réponse
    await this.registry.storeQuestionAnswer(
      this.manifest.identity.id,
      question.id,
      answer
    );
    
    // 2. Mettre à jour pièce du puzzle
    await this.onPuzzlePieceDetected({
      id: question.pieceId,
      value: answer,
      source: 'question',
    });
    
    // 3. Logger
    await this.trackEvent({
      event: 'question_answered',
      category: 'discovery',
      data: { questionId: question.id },
    });
  }

  async onQuestionSkipped(question: DiscoveryQuestion): Promise<void> {
    // Marquer comme skippé avec timestamp
    await this.registry.markQuestionSkipped(
      this.manifest.identity.id,
      question.id
    );
    
    // Logger
    await this.trackEvent({
      event: 'question_skipped',
      category: 'discovery',
      data: { questionId: question.id },
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // TUTORIAL HOOKS
  // ═══════════════════════════════════════════════════════════════
  
  async onTutorialUnlocked(tutorial: ModuleTutorial): Promise<void> {
    // 1. Marquer comme débloqué
    await this.registry.unlockTutorial(
      this.manifest.identity.id,
      tutorial.id
    );
    
    // 2. Notifier utilisateur (badge)
    await this.registry.notifyTutorialUnlocked(tutorial);
    
    // 3. Logger
    await this.trackEvent({
      event: 'tutorial_unlocked',
      category: 'learning',
      data: { tutorialId: tutorial.id },
    });
  }

  async onTutorialStarted(tutorial: ModuleTutorial): Promise<void> {
    await this.registry.startTutorial(
      this.manifest.identity.id,
      tutorial.id
    );
    
    await this.trackEvent({
      event: 'tutorial_started',
      category: 'learning',
      data: { tutorialId: tutorial.id },
    });
  }

  async onTutorialCompleted(tutorial: ModuleTutorial): Promise<void> {
    // 1. Marquer complété
    await this.registry.completeTutorial(
      this.manifest.identity.id,
      tutorial.id
    );
    
    // 2. Vérifier tutoriels imbriqués à débloquer
    const nested = this.manifest.nova.tutorials.nested.filter(
      n => n.parentId === tutorial.id && n.unlockAfterCompletion
    );
    
    for (const nestedConfig of nested) {
      const childTutorial = this.findTutorial(nestedConfig.childId);
      if (childTutorial) {
        if (nestedConfig.delay) {
          // Déblocage différé
          await this.registry.scheduleUnlock(
            nestedConfig.childId,
            nestedConfig.delay
          );
        } else {
          await this.onTutorialUnlocked(childTutorial);
        }
      }
    }
    
    // 3. Logger
    await this.trackEvent({
      event: 'tutorial_completed',
      category: 'learning',
      data: { tutorialId: tutorial.id },
    });
  }

  async onTutorialSkipped(tutorial: ModuleTutorial): Promise<void> {
    await this.registry.skipTutorial(
      this.manifest.identity.id,
      tutorial.id
    );
    
    await this.trackEvent({
      event: 'tutorial_skipped',
      category: 'learning',
      data: { tutorialId: tutorial.id },
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // CONTEXTUAL MESSAGE HOOK
  // ═══════════════════════════════════════════════════════════════
  
  async onContextTriggered(context: string): Promise<NovaMessage | null> {
    // Chercher message contextuel correspondant
    const contextualMessage = this.manifest.nova.explanations.contextual.find(
      cm => cm.trigger === context
    );
    
    if (!contextualMessage) return null;
    
    // Vérifier si déjà affiché récemment
    const lastShown = await this.registry.getLastMessageShown(
      this.manifest.identity.id,
      contextualMessage.id
    );
    
    // Ne pas re-afficher avant 24h
    if (lastShown && Date.now() - lastShown.getTime() < 24 * 60 * 60 * 1000) {
      return null;
    }
    
    return {
      type: 'contextual',
      moduleId: this.manifest.identity.id,
      messageId: contextualMessage.id,
      message: contextualMessage.message,
    };
  }

  // ═══════════════════════════════════════════════════════════════
  // FEATURE HOOKS
  // ═══════════════════════════════════════════════════════════════
  
  async onFeatureUnlocked(feature: ModuleFeature): Promise<void> {
    await this.registry.unlockFeature(
      this.manifest.identity.id,
      feature.id
    );
    
    // Message Nova
    await this.registry.queueNovaMessage({
      type: 'feature_unlocked',
      moduleId: this.manifest.identity.id,
      message: {
        fr: `Nouvelle fonctionnalité débloquée: ${feature.name.fr}`,
        en: `New feature unlocked: ${feature.name.en}`,
      },
    });
    
    await this.trackEvent({
      event: 'feature_unlocked',
      category: 'feature_adoption',
      data: { featureId: feature.id },
    });
  }

  async checkFeatureAccess(featureId: string): Promise<boolean> {
    return this.registry.checkFeatureAccess(
      this.manifest.identity.id,
      featureId
    );
  }

  // ═══════════════════════════════════════════════════════════════
  // ANALYTICS HOOK
  // ═══════════════════════════════════════════════════════════════
  
  async trackEvent(event: AnalyticsEvent): Promise<void> {
    await this.registry.trackAnalytics({
      moduleId: this.manifest.identity.id,
      ...event,
      timestamp: new Date(),
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // HELPERS
  // ═══════════════════════════════════════════════════════════════
  
  private matchesTrigger(action: UserAction, trigger: DetectionTrigger): boolean {
    // Logique de matching trigger
    return action.type === trigger.event;
  }
  
  private extractValue(action: UserAction, trigger: DetectionTrigger): any {
    // Extraire valeur selon config trigger
    if (trigger.aggregation === 'count') {
      return action.count || 1;
    }
    if (trigger.pattern) {
      const match = action.data?.match(new RegExp(trigger.pattern, 'i'));
      return match ? trigger.value : null;
    }
    return action.data;
  }
  
  private matchesUnlockCondition(piece: DetectedPiece, condition: any): boolean {
    if (condition.piece !== piece.id) return false;
    if (condition.value && piece.value !== condition.value) return false;
    if (condition.minValue && piece.value < condition.minValue) return false;
    if (condition.maxValue && piece.value > condition.maxValue) return false;
    return true;
  }
  
  private findTutorial(tutorialId: string): ModuleTutorial | undefined {
    return [
      this.manifest.nova.tutorials.intro,
      ...this.manifest.nova.tutorials.features,
      ...this.manifest.nova.tutorials.advanced,
    ].find(t => t.id === tutorialId);
  }
}
```

---

# 5. PIÈCES DU PUZZLE À DÉFINIR

## 5.1 Template Pièce du Puzzle

```typescript
interface PuzzlePiece {
  // ═══════════════════════════════════════════════════════════════
  // IDENTIFICATION
  // ═══════════════════════════════════════════════════════════════
  id: string;                      // "piece-[module]-[name]"
  name: string;                    // Nom lisible
  description: string;             // Description pour admin
  
  // ═══════════════════════════════════════════════════════════════
  // PRIORITÉ
  // ═══════════════════════════════════════════════════════════════
  priority: 'essential' | 'useful' | 'optional';
  // essential = Change significativement l'expérience
  // useful = Améliore l'expérience
  // optional = Nice to have
  
  // ═══════════════════════════════════════════════════════════════
  // SOURCE DE COLLECTE
  // ═══════════════════════════════════════════════════════════════
  source: 'detection' | 'question' | 'import' | 'inference';
  // detection = Observé automatiquement
  // question = Question Nova
  // import = Importé depuis service externe
  // inference = Déduit d'autres pièces
  
  // ═══════════════════════════════════════════════════════════════
  // TYPE DE DONNÉE
  // ═══════════════════════════════════════════════════════════════
  dataType: 'boolean' | 'string' | 'number' | 'enum' | 'array' | 'object';
  
  // Pour enum
  options?: {
    value: string;
    label: { fr: string; en: string };
  }[];
  
  // Pour number
  range?: { min?: number; max?: number };
  thresholds?: { value: number; label: string }[];
  
  // ═══════════════════════════════════════════════════════════════
  // COMPORTEMENT
  // ═══════════════════════════════════════════════════════════════
  
  // Impact si manquant
  affectsExperience: boolean;
  fallbackBehavior?: string;       // Comportement par défaut
  
  // Mise à jour
  mutable: boolean;                // Peut changer?
  updateFrequency?: 'once' | 'daily' | 'weekly' | 'on_action';
  
  // Dépendances
  dependsOn?: string[];            // IDs autres pièces requises avant
  
  // ═══════════════════════════════════════════════════════════════
  // GOUVERNANCE
  // ═══════════════════════════════════════════════════════════════
  storage: {
    location: 'profile' | 'dataspace' | 'session';
    retention: 'permanent' | 'session' | 'ttl';
    ttlDays?: number;
    exportable: boolean;
    deletable: boolean;
  };
  
  // ═══════════════════════════════════════════════════════════════
  // DÉBLOCAGES
  // ═══════════════════════════════════════════════════════════════
  unlocks: {
    features: string[];            // Features débloquées quand collectée
    tutorials: string[];           // Tutoriels débloqués
    questions: string[];           // Questions suivantes débloquées
    modules: string[];             // Modules débloqués
  };
}
```

## 5.2 Ordre de Collecte Standard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              ORDRE DE COLLECTE STANDARD PAR NIVEAU                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  NIVEAU 0: PIÈCES SYSTÈME (Collectées à l'inscription)                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  0.1 Identité → 0.2 Langue → 0.3 Timezone → 0.4 Conditions          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  NIVEAU 1: PIÈCES CONTEXTUELLES (Jour 1-7)                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1.1 Sphère principale (détection: plus visitée)                    │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  1.2 Contexte sphère (question: solo/équipe si Business)            │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  1.3 Type contenu principal (détection: types fichiers uploadés)    │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  1.4 Niveau expertise (inférence: complexité actions)               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  NIVEAU 2: PIÈCES DOMAINE (Semaine 2-4)                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  2.1 Domaine métier (détection: vocabulaire, documents)             │   │
│  │       │                                                              │   │
│  │       ├─▶ Si Construction: 2.2a Type entreprise → 2.3a Licences    │   │
│  │       │                                                              │   │
│  │       ├─▶ Si Immobilier: 2.2b Type propriétés → 2.3b Juridiction   │   │
│  │       │                                                              │   │
│  │       ├─▶ Si Créatif: 2.2c Type création → 2.3c Outils             │   │
│  │       │                                                              │   │
│  │       └─▶ Si Autre: 2.2d Secteur → 2.3d Spécificités               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  NIVEAU 3: PIÈCES OPTIMISATION (Mois 2+)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  3.1 Préférences workflow (détection: patterns usage)               │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  3.2 Préférences agents (détection: agents utilisés)                │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  3.3 Intégrations souhaitées (question si pattern externe)          │   │
│  │       │                                                              │   │
│  │       ▼                                                              │   │
│  │  3.4 Automatisations (proposition si pattern répétitif)             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 6. SYSTÈME DE TUTORIELS MODULE

## 6.1 Hiérarchie des Tutoriels

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HIÉRARCHIE TUTORIELS MODULE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  NIVEAU 0: TUTORIEL INTRODUCTION (Obligatoire)                             │
│  ├── Automatiquement proposé à la première visite                          │
│  ├── Skippable mais tracké                                                  │
│  └── Durée: 1-2 min max                                                    │
│                                                                             │
│  NIVEAU 1: TUTORIELS FEATURES (Par feature majeure)                        │
│  ├── Débloqués par première utilisation feature                            │
│  ├── Skippable                                                              │
│  └── Durée: 30s-2min                                                       │
│                                                                             │
│  NIVEAU 2: TUTORIELS AVANCÉS (Conditionnels)                               │
│  ├── Débloqués par pièces du puzzle                                        │
│  ├── Skippable                                                              │
│  └── Durée: 2-5min                                                         │
│                                                                             │
│  NIVEAU 3: TUTORIELS IMBRIQUÉS (Sous-tutoriels)                            │
│  ├── Débloqués par completion parent                                       │
│  ├── Peuvent avoir délai                                                    │
│  └── Durée: variable                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Template Tutoriel Module

```typescript
interface ModuleTutorial {
  // Identification
  id: string;                       // "tut-[module]-[name]"
  moduleId: string;                 // Module parent
  
  // Contenu
  title: { fr: string; en: string };
  description?: { fr: string; en: string };
  duration: '30s' | '1min' | '2min' | '3min' | '5min';
  
  // Niveau
  level: 0 | 1 | 2 | 3;
  
  // Déblocage
  unlockCondition: TutorialUnlockCondition;
  
  // Steps
  steps: TutorialStep[];
  
  // Comportement
  skippable: boolean;
  resumable: boolean;               // Peut reprendre où on était
  repeatable: boolean;              // Peut refaire
  
  // Après completion
  onComplete?: {
    message?: { fr: string; en: string };
    unlocksTutorials?: string[];
    unlocksFeatures?: string[];
    achievement?: string;
  };
}

type TutorialUnlockCondition = 
  | 'first_visit'                   // Première visite module
  | 'manual'                        // Déclenché manuellement
  | `${string}_first_time`          // Première action de type
  | `after_tutorial_${string}`      // Après completion autre tutoriel
  | { piece: string; value?: any; minValue?: number };  // Pièce puzzle

interface TutorialStep {
  id: string;
  title: { fr: string; en: string };
  content: { fr: string; en: string };
  
  // Visuel
  image?: string;                   // URL image/gif
  video?: string;                   // URL vidéo courte
  highlight?: string;               // CSS selector à highlight
  
  // Interaction
  action?: 'click' | 'input' | 'wait' | 'observe' | 'none';
  actionTarget?: string;            // Si action requise
  actionValidation?: string;        // Fonction validation
  
  // Durée step
  autoAdvance?: boolean;            // Avance auto après délai
  autoAdvanceDelay?: number;        // ms
}
```

## 6.3 Arbre de Déblocage Tutoriels

```
                    ┌─────────────────────┐
                    │  TUT-INTRO (N0)     │
                    │  "Introduction"     │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │ TUT-FEAT-1    │   │ TUT-FEAT-2    │   │ TUT-FEAT-3    │
   │ (N1)          │   │ (N1)          │   │ (N1)          │
   │ 1ère action A │   │ 1ère action B │   │ 1ère action C │
   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
           │                   │                   │
           │                   │                   │
   ┌───────┴───────┐           │           ┌───────┴───────┐
   │               │           │           │               │
   ▼               ▼           ▼           ▼               ▼
┌──────┐      ┌──────┐    ┌──────┐    ┌──────┐       ┌──────┐
│N1-a  │      │N1-b  │    │N2    │    │N1-c  │       │N2    │
│Nested│      │Nested│    │Avancé│    │Nested│       │Avancé│
│7j    │      │      │    │Pièce │    │      │       │Pièce │
│delay │      │      │    │X=Y   │    │      │       │Z>10  │
└──────┘      └──────┘    └──────┘    └──────┘       └──────┘
```

---

# 7. QUESTIONS DE DÉCOUVERTE MODULE

## 7.1 Template Question

```typescript
interface DiscoveryQuestion {
  // Identification
  id: string;                       // "q-[module]-[topic]"
  moduleId: string;
  pieceId: string;                  // Pièce puzzle associée
  
  // Question
  question: { fr: string; en: string };
  
  // Type réponse
  type: 'single' | 'multiple' | 'freetext' | 'scale' | 'boolean';
  
  // Options (si applicable)
  options?: {
    value: string;
    label: { fr: string; en: string };
    icon?: string;
  }[];
  
  // Scale (si type = 'scale')
  scale?: {
    min: number;
    max: number;
    minLabel: { fr: string; en: string };
    maxLabel: { fr: string; en: string };
  };
  
  // Déclenchement
  trigger: QuestionTrigger;
  timing: 'immediate' | 'after_action' | 'session_end' | 'next_session';
  
  // Comportement
  skippable: boolean;
  maxAsks: number;                  // Combien de fois max proposer
  cooldownDays: number;             // Jours avant re-proposer si skippé
  
  // Conditions
  conditions?: {
    requiresPieces?: string[];      // Pièces requises avant
    excludeIfPieces?: string[];     // Ne pas poser si ces pièces existent
    userSegment?: string;           // Segment utilisateur
  };
  
  // Actions post-réponse
  onAnswer?: {
    [value: string]: {
      unlocksTutorials?: string[];
      unlocksFeatures?: string[];
      nextQuestion?: string;
      novaMessage?: { fr: string; en: string };
    };
  };
}

type QuestionTrigger = 
  | 'first_module_visit'
  | 'after_tutorial_intro'
  | `after_action_${string}`
  | `action_count_${string}_${number}`  // Ex: "action_count_upload_3"
  | `piece_collected_${string}`;
```

## 7.2 Flow des Questions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FLOW DES QUESTIONS NOVA                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. TRIGGER DÉTECTÉ                                                         │
│     │                                                                       │
│     ▼                                                                       │
│  2. VÉRIFIER CONDITIONS                                                     │
│     ├── Pièces requises présentes?                                         │
│     ├── Pièces excluantes absentes?                                        │
│     ├── Cooldown respecté?                                                  │
│     └── Max asks pas atteint?                                              │
│     │                                                                       │
│     ├─▶ Si NON: Skip silencieusement                                       │
│     │                                                                       │
│     ▼                                                                       │
│  3. VÉRIFIER TIMING                                                         │
│     ├── immediate → Afficher maintenant                                    │
│     ├── after_action → Attendre fin action                                 │
│     ├── session_end → Queue pour fin session                               │
│     └── next_session → Queue pour prochaine session                        │
│     │                                                                       │
│     ▼                                                                       │
│  4. AFFICHER QUESTION                                                       │
│     │                                                                       │
│     ├─▶ USER RÉPOND                                                        │
│     │   │                                                                   │
│     │   ▼                                                                   │
│     │   5a. STOCKER RÉPONSE                                                │
│     │   │                                                                   │
│     │   ▼                                                                   │
│     │   6a. EXÉCUTER onAnswer ACTIONS                                      │
│     │       ├── Débloquer tutoriels                                        │
│     │       ├── Débloquer features                                         │
│     │       ├── Poser question suivante                                    │
│     │       └── Afficher message Nova                                      │
│     │                                                                       │
│     └─▶ USER SKIP                                                          │
│         │                                                                   │
│         ▼                                                                   │
│         5b. ENREGISTRER SKIP                                               │
│         │                                                                   │
│         ▼                                                                   │
│         6b. PLANIFIER RE-ASK (si maxAsks pas atteint)                      │
│             └── Attendre cooldownDays                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 8. REGISTRY CENTRAL NOVA

## 8.1 Architecture du Registry

```typescript
// core/nova/registry.ts

export class NovaRegistry {
  private static instance: NovaRegistry;
  
  // ═══════════════════════════════════════════════════════════════
  // STORAGE
  // ═══════════════════════════════════════════════════════════════
  
  // Modules enregistrés
  private modules: Map<string, RegisteredModule> = new Map();
  
  // Tutoriels globaux (tous modules)
  private tutorials: Map<string, ModuleTutorial> = new Map();
  
  // Questions globales (tous modules)
  private questions: Map<string, DiscoveryQuestion> = new Map();
  
  // Pièces puzzle globales
  private puzzlePieces: Map<string, PuzzlePiece> = new Map();
  
  // Messages contextuels globaux
  private contextualMessages: Map<string, NovaContextualMessage> = new Map();

  // ═══════════════════════════════════════════════════════════════
  // MODULE REGISTRATION
  // ═══════════════════════════════════════════════════════════════
  
  async registerModule(manifest: ModuleManifest): Promise<void> {
    // 1. Valider manifest
    this.validateManifest(manifest);
    
    // 2. Enregistrer module
    this.modules.set(manifest.identity.id, {
      manifest,
      registeredAt: new Date(),
      active: true,
    });
    
    // 3. Enregistrer tutoriels
    this.registerTutorials(manifest);
    
    // 4. Enregistrer questions
    this.registerQuestions(manifest);
    
    // 5. Enregistrer pièces puzzle
    this.registerPuzzlePieces(manifest);
    
    // 6. Enregistrer messages contextuels
    this.registerContextualMessages(manifest);
    
    console.log(`[NovaRegistry] Module ${manifest.identity.id} registered`);
  }
  
  // ═══════════════════════════════════════════════════════════════
  // TUTORIAL MANAGEMENT
  // ═══════════════════════════════════════════════════════════════
  
  private registerTutorials(manifest: ModuleManifest): void {
    const allTutorials = [
      manifest.nova.tutorials.intro,
      ...manifest.nova.tutorials.features,
      ...manifest.nova.tutorials.advanced,
    ];
    
    for (const tutorial of allTutorials) {
      this.tutorials.set(tutorial.id, {
        ...tutorial,
        moduleId: manifest.identity.id,
      });
    }
  }
  
  getTutorial(tutorialId: string): ModuleTutorial | undefined {
    return this.tutorials.get(tutorialId);
  }
  
  getTutorialsForModule(moduleId: string): ModuleTutorial[] {
    return Array.from(this.tutorials.values())
      .filter(t => t.moduleId === moduleId);
  }
  
  getUnlockedTutorials(userId: string): ModuleTutorial[] {
    // Query user state + filter tutorials
    // ...
  }
  
  // ═══════════════════════════════════════════════════════════════
  // QUESTION MANAGEMENT
  // ═══════════════════════════════════════════════════════════════
  
  private registerQuestions(manifest: ModuleManifest): void {
    for (const question of manifest.nova.puzzle.discoveryQuestions) {
      this.questions.set(question.id, {
        ...question,
        moduleId: manifest.identity.id,
      });
    }
  }
  
  getPendingQuestions(userId: string, context: string): DiscoveryQuestion[] {
    // Query user state + filter questions ready to ask
    // ...
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PUZZLE MANAGEMENT
  // ═══════════════════════════════════════════════════════════════
  
  private registerPuzzlePieces(manifest: ModuleManifest): void {
    for (const piece of manifest.nova.puzzle.requiredPieces) {
      this.puzzlePieces.set(piece.id, {
        ...piece,
        moduleId: manifest.identity.id,
      });
    }
  }
  
  getUserPuzzleState(userId: string): UserPuzzleState {
    // Query user puzzle pieces collected
    // ...
  }
  
  // ═══════════════════════════════════════════════════════════════
  // CONTEXTUAL MESSAGES
  // ═══════════════════════════════════════════════════════════════
  
  private registerContextualMessages(manifest: ModuleManifest): void {
    for (const msg of manifest.nova.explanations.contextual) {
      this.contextualMessages.set(msg.id, {
        ...msg,
        moduleId: manifest.identity.id,
      });
    }
  }
  
  getContextualMessage(context: string): NovaContextualMessage | undefined {
    return Array.from(this.contextualMessages.values())
      .find(msg => msg.trigger === context);
  }
  
  // ═══════════════════════════════════════════════════════════════
  // GLOBAL QUERIES
  // ═══════════════════════════════════════════════════════════════
  
  // Obtenir TOUS les tutoriels intro disponibles pour onboarding
  getAllIntroTutorials(): ModuleTutorial[] {
    return Array.from(this.tutorials.values())
      .filter(t => t.level === 0);
  }
  
  // Obtenir ordre global de collecte pièces
  getGlobalPuzzleCollectionOrder(): PuzzlePiece[] {
    return Array.from(this.puzzlePieces.values())
      .sort((a, b) => {
        const priorityOrder = { essential: 0, useful: 1, optional: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });
  }
  
  // Obtenir tous les messages première découverte
  getAllFirstDiscoveryMessages(): Map<string, FirstDiscoveryMessage> {
    const messages = new Map();
    for (const [id, module] of this.modules) {
      messages.set(id, module.manifest.nova.explanations.firstDiscovery);
    }
    return messages;
  }
  
  // ═══════════════════════════════════════════════════════════════
  // VALIDATION
  // ═══════════════════════════════════════════════════════════════
  
  private validateManifest(manifest: ModuleManifest): void {
    const errors: string[] = [];
    
    // Vérifier identité
    if (!manifest.identity.id) errors.push('Missing identity.id');
    if (!manifest.identity.name) errors.push('Missing identity.name');
    
    // Vérifier Nova integration
    if (!manifest.nova) errors.push('Missing nova integration');
    if (!manifest.nova.explanations.short.fr) errors.push('Missing short description FR');
    if (!manifest.nova.explanations.firstDiscovery.fr) errors.push('Missing first discovery FR');
    if (!manifest.nova.tutorials.intro) errors.push('Missing intro tutorial');
    
    // Vérifier tutoriels ont des steps
    const allTutorials = [
      manifest.nova.tutorials.intro,
      ...manifest.nova.tutorials.features,
      ...manifest.nova.tutorials.advanced,
    ];
    for (const tut of allTutorials) {
      if (!tut.steps || tut.steps.length === 0) {
        errors.push(`Tutorial ${tut.id} has no steps`);
      }
    }
    
    if (errors.length > 0) {
      throw new Error(`Invalid module manifest:\n${errors.join('\n')}`);
    }
  }
  
  // ═══════════════════════════════════════════════════════════════
  // SINGLETON
  // ═══════════════════════════════════════════════════════════════
  
  static getInstance(): NovaRegistry {
    if (!NovaRegistry.instance) {
      NovaRegistry.instance = new NovaRegistry();
    }
    return NovaRegistry.instance;
  }
}
```

## 8.2 Auto-Discovery des Modules

```typescript
// core/nova/module-loader.ts

export class NovaModuleLoader {
  private registry: NovaRegistry;
  
  constructor() {
    this.registry = NovaRegistry.getInstance();
  }
  
  /**
   * Charge automatiquement tous les modules avec manifest
   */
  async loadAllModules(): Promise<void> {
    // Pattern: modules/*/module.manifest.ts
    const moduleManifests = await this.discoverModules();
    
    for (const manifest of moduleManifests) {
      try {
        await this.registry.registerModule(manifest);
      } catch (error) {
        console.error(`Failed to load module ${manifest.identity.id}:`, error);
      }
    }
    
    console.log(`[NovaModuleLoader] Loaded ${moduleManifests.length} modules`);
  }
  
  /**
   * Découvre tous les manifests dans le dossier modules
   */
  private async discoverModules(): Promise<ModuleManifest[]> {
    // En dev: import dynamique
    // En prod: liste précompilée
    
    const manifests: ModuleManifest[] = [];
    
    // Liste des modules (générée au build)
    const moduleIds = [
      'mod-dataspace',
      'mod-documents',
      'mod-tasks',
      'mod-projects',
      'mod-calendar',
      'mod-immobilier-rental',
      'mod-construction',
      'mod-creative-studio',
      // ... etc
    ];
    
    for (const moduleId of moduleIds) {
      try {
        const { default: manifest } = await import(
          `@/modules/${moduleId}/module.manifest`
        );
        manifests.push(manifest);
      } catch (error) {
        console.warn(`Module ${moduleId} not found or invalid`);
      }
    }
    
    return manifests;
  }
  
  /**
   * Génère la liste des présentations Nova pour tous modules
   */
  generateNovaPresentation(): NovaPresentationList {
    const modules = Array.from(this.registry.modules.values());
    
    return {
      // Pour chaque sphère, liste des modules
      bySphere: this.groupModulesBySphere(modules),
      
      // Tous les tutoriels intro
      introTutorials: this.registry.getAllIntroTutorials(),
      
      // Ordre de présentation recommandé
      presentationOrder: this.calculatePresentationOrder(modules),
      
      // Messages première découverte
      firstDiscoveryMessages: this.registry.getAllFirstDiscoveryMessages(),
    };
  }
  
  private groupModulesBySphere(modules: RegisteredModule[]): Map<SphereId, ModulePresentation[]> {
    const result = new Map();
    
    for (const module of modules) {
      for (const sphere of module.manifest.placement.spheres) {
        if (!result.has(sphere)) {
          result.set(sphere, []);
        }
        result.get(sphere).push({
          moduleId: module.manifest.identity.id,
          name: module.manifest.identity.name,
          icon: module.manifest.identity.icon,
          shortDescription: module.manifest.nova.explanations.short,
          isPrimary: sphere === module.manifest.placement.primarySphere,
        });
      }
    }
    
    return result;
  }
  
  private calculatePresentationOrder(modules: RegisteredModule[]): string[] {
    // Ordre basé sur:
    // 1. Core modules first
    // 2. Then by category
    // 3. Then alphabetical
    
    return modules
      .sort((a, b) => {
        // Core first
        if (a.manifest.identity.category === 'core' && b.manifest.identity.category !== 'core') return -1;
        if (b.manifest.identity.category === 'core' && a.manifest.identity.category !== 'core') return 1;
        
        // Then by name
        return a.manifest.identity.name.localeCompare(b.manifest.identity.name);
      })
      .map(m => m.manifest.identity.id);
  }
}
```

---

# 9. TEMPLATES & EXEMPLES

## 9.1 Template Vide — Nouveau Module

```typescript
// modules/[new-module]/module.manifest.ts

import { ModuleManifest } from '@chenu/module-system';

export const NewModuleManifest: ModuleManifest = {
  // ═══════════════════════════════════════════════════════════════
  // IDENTITÉ — Modifier ces valeurs
  // ═══════════════════════════════════════════════════════════════
  identity: {
    id: 'mod-new-module',               // CHANGER
    name: 'Nouveau Module',             // CHANGER
    nameFr: 'Nouveau Module',           // CHANGER
    nameEn: 'New Module',               // CHANGER
    version: '1.0.0',
    icon: '📦',                         // CHANGER
    color: '#3F7249',                   // CHANGER si besoin
    author: 'Votre nom',                // CHANGER
    category: 'domain',                 // 'core' | 'domain' | 'addon'
  },

  // ═══════════════════════════════════════════════════════════════
  // PLACEMENT — Où apparaît le module
  // ═══════════════════════════════════════════════════════════════
  placement: {
    spheres: ['business'],              // CHANGER: sphères concernées
    primarySphere: 'business',          // CHANGER: sphère principale
    bureauSection: 'projects',          // CHANGER: section bureau
    navigation: {
      showInSidebar: true,
      showInQuickAccess: false,
      menuOrder: 10,                    // CHANGER: position menu
    },
    routes: {
      base: '/new-module',              // CHANGER: route base
      children: [
        // AJOUTER vos routes
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // DÉPENDANCES
  // ═══════════════════════════════════════════════════════════════
  dependencies: {
    required: [
      // AJOUTER modules requis
    ],
    optional: [
      // AJOUTER modules optionnels
    ],
    conflicts: [],
  },

  // ═══════════════════════════════════════════════════════════════
  // GOUVERNANCE
  // ═══════════════════════════════════════════════════════════════
  governance: {
    tokenCost: {
      base: 5,                          // AJUSTER
      perItem: 1,                       // AJUSTER
      aiFeatures: {
        // AJOUTER features IA avec coûts
      },
    },
    permissions: {
      required: ['dataspace.read', 'dataspace.write'],
      optional: [],
    },
    dataScope: {
      identityBound: true,
      crossIdentityAllowed: false,
      exportable: true,
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // NOVA INTEGRATION — SECTION CRITIQUE
  // ═══════════════════════════════════════════════════════════════
  nova: {
    // EXPLICATIONS
    explanations: {
      short: {
        fr: "Description courte du module en moins de 50 mots.",  // ÉCRIRE
        en: "Short module description in less than 50 words.",    // ÉCRIRE
      },
      long: {
        fr: `Description longue du module en moins de 200 mots. 
             Expliquer ce que fait le module, pour qui, et les 
             principales fonctionnalités.`,                       // ÉCRIRE
        en: `Long module description in less than 200 words.
             Explain what the module does, for whom, and the
             main features.`,                                     // ÉCRIRE
      },
      firstDiscovery: {
        fr: "Bienvenue dans [Module]! Message de première découverte.", // ÉCRIRE
        en: "Welcome to [Module]! First discovery message.",           // ÉCRIRE
        displayTrigger: 'first_visit',
      },
      contextual: [
        // AJOUTER messages contextuels
        {
          id: 'ctx-example',
          trigger: 'example_action',
          message: {
            fr: "Message contextuel exemple",
            en: "Example contextual message",
          },
        },
      ],
      tooltips: {
        // AJOUTER tooltips pour chaque élément UI
        'btn-main-action': {
          fr: "Description du bouton principal",
          en: "Main button description",
        },
      },
    },

    // PUZZLE INFORMATIONNEL
    puzzle: {
      requiredPieces: [
        // DÉFINIR les pièces d'information nécessaires
        {
          id: 'piece-example',
          name: 'Exemple de pièce',
          priority: 'essential',
          source: 'detection',
          affectsExperience: true,
        },
      ],
      collectionOrder: [
        'piece-example',
        // DÉFINIR l'ordre de collecte
      ],
      discoveryQuestions: [
        // DÉFINIR les questions de découverte
        {
          id: 'q-example',
          pieceId: 'piece-example',
          trigger: 'first_visit',
          question: {
            fr: "Question exemple?",
            en: "Example question?",
          },
          options: [
            { value: 'opt1', label: { fr: 'Option 1', en: 'Option 1' } },
            { value: 'opt2', label: { fr: 'Option 2', en: 'Option 2' } },
          ],
          skippable: true,
          timing: 'after_action',
        },
      ],
      detectionTriggers: [
        // DÉFINIR les triggers de détection automatique
      ],
      conditionalUnlocks: [
        // DÉFINIR les déblocages conditionnels
      ],
    },

    // TUTORIELS
    tutorials: {
      intro: {
        id: 'tut-new-module-intro',
        title: { fr: 'Introduction', en: 'Introduction' },
        duration: '2min',
        unlockCondition: 'first_visit',
        steps: [
          {
            id: 'step-1',
            title: { fr: 'Bienvenue', en: 'Welcome' },
            content: {
              fr: "Contenu de l'étape 1",
              en: "Step 1 content",
            },
          },
          // AJOUTER plus d'étapes
        ],
      },
      features: [
        // AJOUTER tutoriels features
      ],
      advanced: [
        // AJOUTER tutoriels avancés
      ],
      nested: [
        // DÉFINIR tutoriels imbriqués si nécessaire
      ],
    },

    // HOOKS
    hooks: {
      emits: [
        // DÉFINIR événements émis
      ],
      listensTo: [
        // DÉFINIR événements écoutés
      ],
      callbacks: {
        onModuleLoad: 'initializeModule',
        onModuleUnload: 'cleanupModule',
        onUserAction: 'trackAction',
        onError: 'handleError',
      },
    },

    // VARIANTES
    variants: {
      userProfiles: [],
      contexts: [],
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // FEATURES
  // ═══════════════════════════════════════════════════════════════
  features: [
    // DÉFINIR les fonctionnalités
  ],

  // ═══════════════════════════════════════════════════════════════
  // ANALYTICS
  // ═══════════════════════════════════════════════════════════════
  analytics: {
    trackingEvents: [
      { event: 'module_opened', category: 'engagement' },
      // AJOUTER événements tracking
    ],
    kpis: [
      { id: 'adoption_rate', name: 'Taux adoption', target: 0.7 },
      // AJOUTER KPIs
    ],
  },
};

export default NewModuleManifest;
```

---

# 10. VALIDATION & CERTIFICATION

## 10.1 Tests Automatisés

```typescript
// core/nova/validation/module-validator.ts

export class ModuleValidator {
  
  /**
   * Valide un manifest complet
   * Retourne liste d'erreurs (vide = valide)
   */
  validate(manifest: ModuleManifest): ValidationResult {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];
    
    // ═══════════════════════════════════════════════════════════════
    // PHASE 1: STRUCTURE
    // ═══════════════════════════════════════════════════════════════
    
    // 1.1 Identité
    if (!manifest.identity?.id) {
      errors.push({ code: 'E001', message: 'Missing identity.id' });
    }
    if (!manifest.identity?.id?.startsWith('mod-')) {
      errors.push({ code: 'E002', message: 'identity.id must start with "mod-"' });
    }
    
    // 1.2 Placement
    if (!manifest.placement?.spheres?.length) {
      errors.push({ code: 'E003', message: 'Must specify at least one sphere' });
    }
    if (!manifest.placement?.primarySphere) {
      errors.push({ code: 'E004', message: 'Must specify primarySphere' });
    }
    
    // ═══════════════════════════════════════════════════════════════
    // PHASE 2: NOVA INTEGRATION
    // ═══════════════════════════════════════════════════════════════
    
    // 2.1 Explications
    if (!manifest.nova?.explanations?.short?.fr) {
      errors.push({ code: 'E010', message: 'Missing short description FR' });
    }
    if (!manifest.nova?.explanations?.short?.en) {
      errors.push({ code: 'E011', message: 'Missing short description EN' });
    }
    if (manifest.nova?.explanations?.short?.fr?.split(' ').length > 50) {
      warnings.push({ code: 'W010', message: 'Short description FR exceeds 50 words' });
    }
    
    if (!manifest.nova?.explanations?.firstDiscovery?.fr) {
      errors.push({ code: 'E012', message: 'Missing first discovery message FR' });
    }
    
    // 2.2 Tutoriels
    if (!manifest.nova?.tutorials?.intro) {
      errors.push({ code: 'E020', message: 'Missing intro tutorial' });
    }
    if (manifest.nova?.tutorials?.intro?.steps?.length === 0) {
      errors.push({ code: 'E021', message: 'Intro tutorial has no steps' });
    }
    
    // Vérifier chaque tutoriel
    const allTutorials = [
      manifest.nova?.tutorials?.intro,
      ...(manifest.nova?.tutorials?.features || []),
      ...(manifest.nova?.tutorials?.advanced || []),
    ].filter(Boolean);
    
    for (const tutorial of allTutorials) {
      if (!tutorial.id) {
        errors.push({ code: 'E022', message: `Tutorial missing id` });
      }
      if (!tutorial.id?.startsWith('tut-')) {
        errors.push({ code: 'E023', message: `Tutorial id must start with "tut-": ${tutorial.id}` });
      }
      if (!tutorial.steps?.length) {
        errors.push({ code: 'E024', message: `Tutorial ${tutorial.id} has no steps` });
      }
      for (const step of tutorial.steps || []) {
        if (!step.content?.fr) {
          errors.push({ code: 'E025', message: `Tutorial ${tutorial.id} step ${step.id} missing FR content` });
        }
      }
    }
    
    // 2.3 Puzzle
    if (!manifest.nova?.puzzle?.requiredPieces?.length) {
      warnings.push({ code: 'W020', message: 'No puzzle pieces defined' });
    }
    
    for (const piece of manifest.nova?.puzzle?.requiredPieces || []) {
      if (!piece.id?.startsWith('piece-')) {
        errors.push({ code: 'E030', message: `Piece id must start with "piece-": ${piece.id}` });
      }
    }
    
    // 2.4 Questions
    for (const question of manifest.nova?.puzzle?.discoveryQuestions || []) {
      if (!question.id?.startsWith('q-')) {
        errors.push({ code: 'E040', message: `Question id must start with "q-": ${question.id}` });
      }
      if (!question.pieceId) {
        errors.push({ code: 'E041', message: `Question ${question.id} missing pieceId` });
      }
    }
    
    // 2.5 Hooks
    if (!manifest.nova?.hooks?.callbacks?.onModuleLoad) {
      errors.push({ code: 'E050', message: 'Missing onModuleLoad callback' });
    }
    
    // ═══════════════════════════════════════════════════════════════
    // PHASE 3: GOUVERNANCE
    // ═══════════════════════════════════════════════════════════════
    
    if (manifest.governance?.tokenCost?.base === undefined) {
      errors.push({ code: 'E060', message: 'Missing token cost base' });
    }
    
    // ═══════════════════════════════════════════════════════════════
    // RÉSULTAT
    // ═══════════════════════════════════════════════════════════════
    
    return {
      valid: errors.length === 0,
      errors,
      warnings,
      score: this.calculateScore(errors, warnings),
    };
  }
  
  private calculateScore(errors: ValidationError[], warnings: ValidationWarning[]): number {
    // 100 points de base
    // -10 par erreur
    // -2 par warning
    return Math.max(0, 100 - (errors.length * 10) - (warnings.length * 2));
  }
}

interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  score: number;  // 0-100, doit être 100 pour déployer
}

interface ValidationError {
  code: string;
  message: string;
}

interface ValidationWarning {
  code: string;
  message: string;
}
```

## 10.2 Checklist de Certification

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CERTIFICATION MODULE CHE·NU                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Module: _________________________ Version: _________ Date: __________      ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ VALIDATION AUTOMATIQUE                                      Score: __/100│ ║
║  ├────────────────────────────────────────────────────────────────────────┤ ║
║  │ □ Pas d'erreurs de validation (E00x)                                    │ ║
║  │ □ Warnings acceptables (W00x)                                           │ ║
║  │ □ Score minimum 100/100                                                 │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ REVIEW MANUELLE                                                         │ ║
║  ├────────────────────────────────────────────────────────────────────────┤ ║
║  │ □ Descriptions claires et utiles                                        │ ║
║  │ □ Tutoriels compréhensibles                                            │ ║
║  │ □ Questions non intrusives                                              │ ║
║  │ □ Flux utilisateur logique                                              │ ║
║  │ □ Intégration cohérente avec CHE·NU                                    │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ TESTS UTILISATEUR                                                       │ ║
║  ├────────────────────────────────────────────────────────────────────────┤ ║
║  │ □ Test nouvel utilisateur (onboarding)                                  │ ║
║  │ □ Test utilisateur existant                                             │ ║
║  │ □ Test parcours complet                                                 │ ║
║  │ □ Test skip/ignore questions                                            │ ║
║  │ □ Test déblocages tutoriels                                             │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  DÉCISION:  □ APPROUVÉ   □ MODIFICATIONS REQUISES   □ REJETÉ               ║
║                                                                              ║
║  Commentaires: ________________________________________________________    ║
║  __________________________________________________________________________║
║                                                                              ║
║  Validé par: _________________ Signature: _____________ Date: __________   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# RÉSUMÉ EXÉCUTIF

## Étapes d'Intégration Nouveau Module

```
1. CRÉER module.manifest.ts avec toutes les sections
   │
2. ÉCRIRE explications Nova (short, long, firstDiscovery)
   │
3. DÉFINIR pièces du puzzle et ordre de collecte
   │
4. CRÉER questions de découverte avec triggers
   │
5. CRÉER tutoriels (intro + features)
   │
6. IMPLÉMENTER nova-hooks.ts
   │
7. ENREGISTRER dans NovaRegistry
   │
8. VALIDER avec ModuleValidator
   │
9. TESTER parcours utilisateur
   │
10. CERTIFIER et déployer
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              MODULE INTEGRATION PROTOCOL COMPLETE                            ║
║                                                                              ║
║          Chaque module = Citoyen de l'écosystème Nova                       ║
║          Pas de manifest = Pas d'existence                                   ║
║                                                                              ║
║                          ON CONTINUE! 💪🔥                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
