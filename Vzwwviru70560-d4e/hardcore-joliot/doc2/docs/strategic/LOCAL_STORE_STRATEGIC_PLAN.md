# 🎯 PLANIFICATION STRATÉGIQUE — LOCAL STORE

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║            ANALYSE COMPLÈTE AVANT DÉVELOPPEMENT                               ║
║                                                                               ║
║         "Bien penser avant de coder"                                         ║
║                                                                               ║
║         Date: 22 Décembre 2025                                               ║
║         Status: DRAFT - En attente validation Jo                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 TABLE DES MATIÈRES

1. [Analyse des Utilisateurs](#1-analyse-des-utilisateurs)
2. [Hiérarchie Informationnelle](#2-hiérarchie-informationnelle)
3. [Parcours Utilisateur (User Journeys)](#3-parcours-utilisateur)
4. [Architecture Technique](#4-architecture-technique)
5. [Intégration avec l'Écosystème](#5-intégration-avec-lécosystème)
6. [Plan de Développement](#6-plan-de-développement)
7. [Validation R&D](#7-validation-rd)

---

## 1. ANALYSE DES UTILISATEURS

### 1.1 Les Deux Côtés du Marché

Local Store est un **marketplace deux côtés**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│     VENDEURS (Offre)                    ACHETEURS (Demande)                │
│     ═══════════════                     ═════════════════                  │
│                                                                             │
│     • Commerçants locaux                • Consommateurs locaux             │
│     • Artisans                          • Familles                         │
│     • Fermiers                          • Restaurateurs                    │
│     • Producteurs                       • Entreprises                      │
│                                                                             │
│     OBJECTIF:                           OBJECTIF:                          │
│     Vendre + Fidéliser                  Trouver + Acheter local            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Personas Détaillées

#### VENDEURS

**PERSONA V1: Marie - Boulangère Artisanale**
```yaml
Profil:
  Âge: 45 ans
  Business: Boulangerie "Au Pain Doré" depuis 15 ans
  Équipe: 3 employés
  CA: ~300K$/an
  
Besoins Prioritaires:
  1. Visibilité locale (être trouvée facilement)
  2. Commandes en ligne (pain du matin)
  3. Fidélisation clients (10% reviennent chaque semaine)
  4. Gestion simple (pas le temps pour tech compliquée)
  
Pain Points:
  - Concurrence grandes surfaces
  - Pas de présence web
  - Gestion stock manuelle
  - Pas de données clients
  
Ce qu'elle veut VOIR EN PREMIER:
  1. "Combien j'ai vendu aujourd'hui?"
  2. "Quelles commandes à préparer?"
  3. "Mon stock est OK?"
  
Technologie: Smartphone moyen, pas à l'aise avec tech
```

**PERSONA V2: Jean - Fermier Maraîcher**
```yaml
Profil:
  Âge: 52 ans
  Business: Ferme familiale 50 hectares
  Équipe: Famille + 2 saisonniers
  CA: ~150K$/an
  
Besoins Prioritaires:
  1. Vente directe (éviter intermédiaires)
  2. Paniers hebdomadaires (revenus prévisibles)
  3. Marchés fermiers (présence multi-lieux)
  4. Communication saisonnière
  
Pain Points:
  - Dépendance aux grossistes
  - Revenus imprévisibles
  - Pas de relation directe consommateur
  - Logistique livraison
  
Ce qu'il veut VOIR EN PREMIER:
  1. "Combien d'abonnements actifs?"
  2. "Quels paniers préparer cette semaine?"
  3. "Quel marché demain?"
  
Technologie: Tablette, utilise Facebook pour promo
```

**PERSONA V3: Sophie - Artisane Bijoux**
```yaml
Profil:
  Âge: 35 ans
  Business: Créatrice bijoux artisanaux
  Équipe: Solo
  CA: ~60K$/an
  
Besoins Prioritaires:
  1. Portfolio en ligne (montrer son travail)
  2. Commandes personnalisées
  3. Événements/salons
  4. Histoire de marque
  
Pain Points:
  - Commission Etsy 15%
  - Pas de clientèle locale fidèle
  - Difficile de se différencier
  - Livraison coûteuse
  
Ce qu'elle veut VOIR EN PREMIER:
  1. "Nouvelles demandes de devis?"
  2. "Commandes en cours?"
  3. "Mes meilleures ventes?"
  
Technologie: MacBook Pro, Instagram power user
```

#### ACHETEURS

**PERSONA A1: Famille Tremblay**
```yaml
Profil:
  Type: Famille 4 personnes (2 adultes, 2 enfants)
  Revenu: 120K$/an
  Localisation: Banlieue Montréal
  
Besoins Prioritaires:
  1. Produits frais de qualité
  2. Savoir d'où vient la nourriture
  3. Praticité (pas le temps de courir partout)
  4. Budget raisonnable
  
Pain Points:
  - Supermarché = qualité variable
  - Marchés = horaires contraignants
  - Bio = trop cher
  - Pas de relation avec producteurs
  
Ce qu'ils veulent VOIR EN PREMIER:
  1. "Qu'est-ce qui est disponible près de moi?"
  2. "C'est ouvert maintenant?"
  3. "Je peux commander et récupérer?"
  
Comportement Achat:
  - Hebdomadaire pour frais
  - Compare prix mais prêt à payer +20% pour qualité
  - Veut connaître l'histoire du produit
```

**PERSONA A2: Chef Restaurant**
```yaml
Profil:
  Type: Chef propriétaire restaurant 40 places
  Budget achat: ~8K$/mois
  
Besoins Prioritaires:
  1. Fournisseurs locaux fiables
  2. Qualité constante
  3. Livraison régulière
  4. Traçabilité pour menu
  
Ce qu'il veut VOIR EN PREMIER:
  1. "Qui peut me livrer X produit demain?"
  2. "Quel est le prix au volume?"
  3. "Quelle est l'origine exacte?"
  
Comportement:
  - Commandes récurrentes (même fournisseurs)
  - Teste puis fidélise
  - Veut pouvoir mettre "de chez Jean" sur menu
```

---

## 2. HIÉRARCHIE INFORMATIONNELLE

### 2.1 Principe Fondamental

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  "L'information la plus importante doit être la plus visible"                ║
║                                                                               ║
║  Priorité = Fréquence d'utilisation × Impact sur décision                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Hiérarchie VENDEUR

```
DASHBOARD VENDEUR - Par priorité d'affichage
═══════════════════════════════════════════

NIVEAU 1 - CRITIQUE (Visible immédiatement)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  📊 AUJOURD'HUI                                                 │
│  ├── Ventes du jour: 847,50$                                   │
│  ├── Commandes à traiter: 5 nouvelles                          │
│  └── Alertes: 2 produits stock bas                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NIVEAU 2 - IMPORTANT (Un clic de distance)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  📦 COMMANDES           📦 PRODUITS          ⭐ RÉPUTATION     │
│  En attente: 5          Actifs: 45           Note: 4.8/5       │
│  En préparation: 3      Stock bas: 2         Avis: 127         │
│  Prêtes: 2              Rupture: 0           Ce mois: +8       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NIVEAU 3 - UTILE (Navigation secondaire)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  📈 Stats              🛒 Boutique           💰 Finances        │
│  │                     │                     │                  │
│  ├── Cette semaine     ├── Profil            ├── Revenus        │
│  ├── Ce mois           ├── Horaires          ├── Retraits       │
│  └── Tendances         └── Livraison         └── Factures       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NIVEAU 4 - OCCASIONNEL (Menu/Paramètres)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ⚙️ Paramètres | 🎯 Marketing | 📊 Rapports | ❓ Aide          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Hiérarchie ACHETEUR

```
PARCOURS ACHETEUR - Par priorité d'affichage
════════════════════════════════════════════

NIVEAU 1 - CRITIQUE (Visible immédiatement)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🔍 RECHERCHE                                                   │
│  ├── "Qu'est-ce que tu cherches?"                              │
│  └── [Catégories visuelles]                                    │
│                                                                 │
│  📍 PRÈS DE MOI (si localisation)                              │
│  ├── Commerces ouverts maintenant                              │
│  └── Distance + Disponibilité                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NIVEAU 2 - IMPORTANT (Résultats de recherche)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  CARTE DE COMMERCE/PRODUIT                                      │
│  ┌───────────────────────────────────────┐                     │
│  │  [Image]                              │                     │
│  │                                       │                     │
│  │  Boulangerie Au Pain Doré            │                     │
│  │  ★★★★☆ 4.8 (127 avis)                │                     │
│  │  📍 1.2 km • 🟢 Ouvert jusqu'à 18h   │                     │
│  │  🏷️ Bio • Artisanal                  │                     │
│  │                                       │                     │
│  │  [Commander]  [Voir]                 │                     │
│  └───────────────────────────────────────┘                     │
│                                                                 │
│  PRIORITÉ INFO:                                                │
│  1. Image (reconnaissance visuelle)                            │
│  2. Nom (identification)                                       │
│  3. Note + Avis (confiance)                                    │
│  4. Distance + Ouvert (disponibilité)                          │
│  5. Badges (différenciation)                                   │
│  6. Actions (conversion)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NIVEAU 3 - DÉTAIL (Page commerce)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Cover image]                                                  │
│                                                                 │
│  SECTION 1: Identité + Confiance                               │
│  - Logo, Nom, Tagline                                          │
│  - Note, Avis, Badges                                          │
│                                                                 │
│  SECTION 2: Disponibilité                                      │
│  - Ouvert/Fermé + Horaires                                     │
│  - Modes de récupération                                       │
│                                                                 │
│  SECTION 3: Catalogue                                          │
│  - Produits par catégorie                                      │
│  - Prix, Stock                                                 │
│                                                                 │
│  SECTION 4: Histoire                                           │
│  - Description, Photos                                         │
│  - Certifications                                              │
│                                                                 │
│  SECTION 5: Pratique                                           │
│  - Carte, Adresse                                              │
│  - Contact                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Mapping Info → Données

```
INFORMATION AFFICHÉE          →    DONNÉE EN BD
═══════════════════════════════════════════════════════════════════

VENDEUR:
"Ventes aujourd'hui: 847$"    →    SUM(orders.total) WHERE date=today
"5 commandes à traiter"       →    COUNT(orders) WHERE status IN (pending, confirmed)
"2 produits stock bas"        →    COUNT(products) WHERE stock < threshold
"Note: 4.8/5"                 →    stores.avg_rating
"127 avis"                    →    stores.total_reviews

ACHETEUR:
"1.2 km"                      →    distance(user.location, store.location)
"Ouvert jusqu'à 18h"          →    store_hours WHERE day=today
"★★★★☆ 4.8"                  →    stores.avg_rating
"Bio • Artisanal"             →    stores.certifications[]
```

---

## 3. PARCOURS UTILISATEUR (User Journeys)

### 3.1 Journey V1: Marie Crée sa Boutique

```
JOURNEY: ONBOARDING VENDEUR
════════════════════════════

Objectif: Marie passe de "je n'ai pas de boutique en ligne" à "je reçois ma première commande"

ÉTAPE 1: DÉCOUVERTE (5 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  "Vendez vos produits aux clients de votre quartier"           │
│                                                                 │
│  ✓ Gratuit pour commencer                                      │
│  ✓ Pas besoin de site web                                      │
│  ✓ Recevez des commandes en ligne                              │
│                                                                 │
│  [Créer ma boutique] ← CTA principal                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 2: INFORMATIONS DE BASE (3 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Parlez-nous de votre commerce                                  │
│                                                                 │
│  Nom: [Au Pain Doré________________]                           │
│  Type: [Boulangerie ▼]                                         │
│  Téléphone: [514-555-1234___________]                          │
│                                                                 │
│  [Continuer]                                                    │
│                                                                 │
│  HUMAN GATE: Sauvegarde en DRAFT, pas encore publique          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 3: LOCALISATION (2 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Où se trouve votre commerce?                                   │
│                                                                 │
│  [Carte avec pin draggable]                                    │
│                                                                 │
│  Adresse: [123 rue Principale, Montréal]                       │
│                                                                 │
│  [Continuer]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 4: HORAIRES (2 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Quand êtes-vous ouvert?                                        │
│                                                                 │
│  ○ Horaires réguliers                                          │
│    Lun-Ven: [6:00] à [18:00]                                   │
│    Sam: [7:00] à [14:00]                                       │
│    Dim: Fermé                                                  │
│                                                                 │
│  [Continuer]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 5: PREMIER PRODUIT (5 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Ajoutez votre premier produit                                  │
│                                                                 │
│  📷 [Glisser une photo]                                        │
│                                                                 │
│  Nom: [Pain de campagne____________]                           │
│  Prix: [5.50$_______]                                          │
│  Description: [Pain rustique cuit au four à bois...]           │
│                                                                 │
│  [Ajouter] [+ Ajouter un autre]                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 6: PREVIEW + PUBLICATION (2 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🎉 Votre boutique est prête!                                  │
│                                                                 │
│  [Preview de la boutique]                                      │
│                                                                 │
│  Vérifiez que tout est correct, puis publiez.                  │
│                                                                 │
│  [Modifier]   [✓ Publier ma boutique]                          │
│                                                                 │
│  ⚠️ HUMAN GATE: Publication = action sensible                  │
│     Confirmation explicite requise                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 7: CONFIRMATION
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ✅ Félicitations! Votre boutique est en ligne!                │
│                                                                 │
│  Partagez votre lien:                                          │
│  localstore.chenu.app/au-pain-dore                             │
│                                                                 │
│  [Copier] [Partager sur Facebook] [WhatsApp]                   │
│                                                                 │
│  Prochaine étape: Ajoutez plus de produits                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

TEMPS TOTAL: ~15 minutes
HUMAN GATES: 2 (création draft, publication)
```

### 3.2 Journey A1: Famille Commande

```
JOURNEY: PREMIÈRE COMMANDE ACHETEUR
═══════════════════════════════════

Objectif: Famille Tremblay trouve et commande du pain artisanal

ÉTAPE 1: DÉCOUVERTE (1 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Recherche: "pain artisanal"]                                 │
│                                                                 │
│  📍 Près de: Laval, QC [Modifier]                              │
│                                                                 │
│  3 résultats à moins de 5 km                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 2: COMPARAISON (2 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Carte avec 3 pins]                                           │
│                                                                 │
│  1. Au Pain Doré • ★4.8 • 1.2km • 🟢 Ouvert                   │
│  2. Boulangerie Chez Paul • ★4.5 • 2.1km • 🟢 Ouvert          │
│  3. La Mie Dorée • ★4.6 • 3.4km • 🔴 Fermé                    │
│                                                                 │
│  [Filtres: Bio | Livraison | Ouvert maintenant]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 3: SÉLECTION BOUTIQUE (1 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Au Pain Doré                                                   │
│  ★★★★★ 4.8 (127 avis)                                         │
│  "Boulangerie artisanale depuis 15 ans"                        │
│                                                                 │
│  🏷️ Bio certifié | Artisanal | Fait maison                    │
│                                                                 │
│  📍 123 rue Principale • 1.2 km                                │
│  🕐 Ouvert jusqu'à 18h                                         │
│  🚗 Ramassage disponible                                       │
│                                                                 │
│  [Voir les produits]                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 4: SÉLECTION PRODUITS (3 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PAINS                           VIENNOISERIES                  │
│                                                                 │
│  [Pain campagne]  [Baguette]    [Croissant]  [Pain choco]     │
│   5.50$            2.00$         2.50$        2.75$            │
│   [+ Panier]       [+ Panier]   [+ Panier]   [+ Panier]       │
│                                                                 │
│  ────────────────────────────────────────────────              │
│  🛒 Panier: 3 articles • 10.00$                                │
│  [Voir panier]                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 5: PANIER (1 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Votre panier                                                   │
│                                                                 │
│  ☐ Pain de campagne          5.50$ × 1     5.50$               │
│  ☐ Baguette tradition        2.00$ × 2     4.00$               │
│  ☐ Croissant                 2.50$ × 2     5.00$               │
│                                                                 │
│  ─────────────────────────────────────────                     │
│  Sous-total                              14.50$                 │
│  TPS (5%)                                 0.73$                 │
│  TVQ (9.975%)                             1.45$                 │
│  ─────────────────────────────────────────                     │
│  Total                                   16.68$                 │
│                                                                 │
│  [Commander]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 6: MODE DE RÉCUPÉRATION (1 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Comment voulez-vous récupérer?                                 │
│                                                                 │
│  ● Ramassage en boutique (Gratuit)                             │
│    📍 123 rue Principale, Montréal                             │
│    Disponible dans 30 min                                       │
│                                                                 │
│  ○ Livraison (5.00$)                                           │
│    Livré en 45-60 min                                          │
│                                                                 │
│  Quand?                                                         │
│  [Aujourd'hui ▼] [Dès que possible ▼]                          │
│                                                                 │
│  [Continuer]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 7: PAIEMENT (1 min)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Paiement                                                       │
│                                                                 │
│  ● Carte de crédit                                             │
│    [**** **** **** 4242] [Modifier]                            │
│                                                                 │
│  ○ Payer sur place                                             │
│                                                                 │
│  ─────────────────────────────────────────                     │
│  Total à payer: 16.68$                                         │
│                                                                 │
│  [Confirmer et payer]                                          │
│                                                                 │
│  ⚠️ HUMAN GATE: Confirmation paiement explicite               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ÉTAPE 8: CONFIRMATION
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ✅ Commande confirmée!                                        │
│                                                                 │
│  Commande #LS-20251222-001                                     │
│                                                                 │
│  📍 À récupérer à:                                             │
│     Au Pain Doré                                                │
│     123 rue Principale, Montréal                               │
│                                                                 │
│  🕐 Prête vers 15h30                                           │
│                                                                 │
│  [Suivre ma commande]                                          │
│                                                                 │
│  Tu recevras une notification quand ce sera prêt!              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

TEMPS TOTAL: ~10 minutes
HUMAN GATES: 1 (confirmation paiement)
```

---

## 4. ARCHITECTURE TECHNIQUE

### 4.1 Structure des Fichiers

```
backend/
├── models/
│   └── local_store/
│       ├── __init__.py
│       ├── store_models.py          # LocalStore, StoreHours, etc.
│       ├── product_models.py        # LocalProduct, ProductVariant
│       ├── order_models.py          # LocalOrder, OrderItem
│       ├── market_models.py         # LocalMarket, MarketVendor
│       └── subscription_models.py   # Subscription
│
├── services/
│   └── local_store/
│       ├── __init__.py
│       ├── store_service.py         # CRUD boutiques
│       ├── catalog_service.py       # Gestion produits
│       ├── order_service.py         # Gestion commandes
│       ├── search_service.py        # Recherche géolocalisée
│       ├── payment_service.py       # Stripe integration
│       └── analytics_service.py     # Stats vendeur
│
├── agents/
│   └── local_store/
│       ├── __init__.py
│       ├── discovery_agent.py       # Aide acheteur trouver
│       ├── vendor_assistant.py      # Aide vendeur gérer
│       ├── pricing_advisor.py       # Suggestions prix
│       └── marketing_advisor.py     # Suggestions promo
│
├── api/
│   └── local_store/
│       ├── __init__.py
│       ├── store_routes.py          # /stores/*
│       ├── product_routes.py        # /stores/{id}/products/*
│       ├── order_routes.py          # /orders/*
│       ├── search_routes.py         # /search/*
│       └── vendor_routes.py         # /vendor/* (dashboard)
│
└── integrations/
    └── local_store/
        ├── __init__.py
        ├── stripe_integration.py    # Paiements
        ├── maps_integration.py      # Géolocalisation
        └── notification_service.py  # Push/SMS/Email
```

### 4.2 Séparation des Responsabilités

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  COUCHE                    RESPONSABILITÉ                                  │
│  ══════                    ══════════════                                  │
│                                                                             │
│  Models                    Définition des données                          │
│                            Validation (Pydantic)                           │
│                            Pas de logique métier                           │
│                                                                             │
│  Services                  Logique métier                                  │
│                            Règles de gestion                               │
│                            Human gates                                     │
│                            Orchestration                                   │
│                                                                             │
│  Agents                    Intelligence (IA)                               │
│                            Suggestions (SANDBOX ONLY)                      │
│                            Analyse (READ ONLY)                             │
│                                                                             │
│  API                       Endpoints HTTP                                  │
│                            Validation entrées                              │
│                            Auth/Permissions                                │
│                            Transformation réponses                         │
│                                                                             │
│  Integrations              Services externes                               │
│                            Abstraction APIs tierces                        │
│                            Retry/Error handling                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Flux de Données Principaux

```
FLUX 1: CRÉATION BOUTIQUE
═════════════════════════

Frontend                API                   Service               Database
   │                     │                      │                      │
   │  POST /stores       │                      │                      │
   │────────────────────>│                      │                      │
   │                     │  create_store_draft  │                      │
   │                     │─────────────────────>│                      │
   │                     │                      │  INSERT (status=DRAFT)
   │                     │                      │─────────────────────>│
   │                     │                      │<─────────────────────│
   │                     │<─────────────────────│                      │
   │  {store_id, DRAFT}  │                      │                      │
   │<────────────────────│                      │                      │
   │                     │                      │                      │
   │  POST /stores/{id}/publish                 │                      │
   │────────────────────>│                      │                      │
   │                     │  submit_for_publish  │                      │
   │                     │─────────────────────>│                      │
   │                     │                      │  HUMAN GATE CHECK    │
   │                     │                      │  UPDATE status=ACTIVE│
   │                     │                      │─────────────────────>│
   │                     │<─────────────────────│<─────────────────────│
   │  {store, ACTIVE}    │                      │                      │
   │<────────────────────│                      │                      │


FLUX 2: COMMANDE
════════════════

Acheteur             API                Service              Vendeur
   │                  │                    │                    │
   │ POST /orders     │                    │                    │
   │─────────────────>│                    │                    │
   │                  │ create_order       │                    │
   │                  │───────────────────>│                    │
   │                  │                    │ INSERT order       │
   │                  │                    │ (status=PENDING)   │
   │                  │                    │                    │
   │                  │                    │ notify_vendor ─────┼───────>│
   │                  │                    │                    │        │
   │ {order_id}       │                    │                    │        │
   │<─────────────────│<───────────────────│                    │        │
   │                  │                    │                    │        │
   │                  │                    │    [Vendeur voit]  │        │
   │                  │                    │    [notification]  │<───────│
   │                  │                    │                    │
   │                  │ POST /orders/{id}/confirm               │
   │                  │<────────────────────────────────────────│
   │                  │                    │                    │
   │                  │ confirm_order      │                    │
   │                  │───────────────────>│                    │
   │                  │                    │ UPDATE status      │
   │                  │                    │ =CONFIRMED         │
   │                  │                    │                    │
   │ [Notification    │                    │ notify_customer    │
   │  "Confirmée!"]   │<───────────────────│<───────────────────│
   │<─────────────────│                    │                    │
```

---

## 5. INTÉGRATION AVEC L'ÉCOSYSTÈME

### 5.1 Connexions avec Modules Existants

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        ÉCOSYSTÈME CHE·NU                                   │
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│  │  SHOPPING   │────>│ LOCAL STORE │<────│   START     │                  │
│  │  (Acheter)  │     │  (Vendre)   │     │  BUSINESS   │                  │
│  └─────────────┘     └─────────────┘     └─────────────┘                  │
│        │                    │                    │                         │
│        │                    │                    │                         │
│        v                    v                    v                         │
│  ┌─────────────────────────────────────────────────────────┐              │
│  │                      BUSINESS SPHERE                    │              │
│  │                                                         │              │
│  │  • CRM (clients)                                       │              │
│  │  • Invoicing (factures)                                │              │
│  │  • Analytics (stats)                                   │              │
│  └─────────────────────────────────────────────────────────┘              │
│                              │                                             │
│                              v                                             │
│  ┌─────────────────────────────────────────────────────────┐              │
│  │                    COMMUNITY SPHERE                     │              │
│  │                                                         │              │
│  │  • Découverte locale                                   │              │
│  │  • Reviews                                             │              │
│  │  • Événements                                          │              │
│  └─────────────────────────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Workflows Cross-Module

```yaml
WORKFLOW 1: Shopping → Local Store
  Trigger: User recherche produit dans Shopping
  Action: Inclure résultats Local Store si pertinent
  Data: Produits locaux avec badge "Achetez Local"
  Human Gate: Non (lecture seule)

WORKFLOW 2: Local Store → Start Business
  Trigger: User clique "Créer ma boutique"
  Action: Si pas d'entreprise, proposer Start Business
  Data: Passage au parcours entrepreneur
  Human Gate: Oui (choix explicite user)

WORKFLOW 3: Local Store → Business Sphere
  Trigger: Vendeur veut voir stats avancées
  Action: Rediriger vers Business Analytics
  Data: Données ventes agrégées
  Human Gate: Oui (cross-sphere transfer)

WORKFLOW 4: Local Store → Community Sphere
  Trigger: Boutique publiée
  Action: Indexer dans découverte locale
  Data: Profil public boutique
  Human Gate: Oui (publication = gate)
```

### 5.3 Partage de Données

```
DONNÉES PARTAGÉES (Read)          DONNÉES PRIVÉES (Write)
═══════════════════════           ════════════════════════

• Profil public boutique          • Revenus détaillés
• Catalogue produits              • Marge par produit
• Horaires                        • Clients individuels
• Localisation                    • Historique commandes
• Avis publics                    • Notes internes
• Certifications                  • Paramètres compte

RÈGLE: Données privées NE SORTENT PAS de la sphère Business
       sans workflow explicite et approbation.
```

---

## 6. PLAN DE DÉVELOPPEMENT

### 6.1 Phases

```
PHASE 1: FONDATIONS (Semaine 1)
════════════════════════════════
Objectif: Structure et modèles de base

□ Database schema (V45_002_local_store.sql) ✅ FAIT
□ Models Python compliant R&D
□ Services de base (CRUD)
□ Tests unitaires modèles

Livrable: Peut créer/lire/modifier une boutique en DB


PHASE 2: CORE FEATURES (Semaine 2)  
══════════════════════════════════
Objectif: Parcours vendeur complet

□ Store service avec human gates
□ Catalog service (produits)
□ Search service (géolocalisation)
□ API routes (store, products)

Livrable: Vendeur peut créer boutique et ajouter produits


PHASE 3: TRANSACTIONS (Semaine 3)
═════════════════════════════════
Objectif: Parcours acheteur complet

□ Order service avec workflow
□ Payment integration (Stripe)
□ Notification service
□ API routes (orders, checkout)

Livrable: Acheteur peut commander et payer


PHASE 4: INTELLIGENCE (Semaine 4)
═════════════════════════════════
Objectif: Agents IA en sandbox

□ Discovery agent (recherche intelligente)
□ Vendor assistant (aide gestion)
□ Pricing advisor (suggestions prix)
□ Analytics service

Livrable: IA aide vendeurs et acheteurs


PHASE 5: POLISH (Semaine 5)
═══════════════════════════
Objectif: Production ready

□ Tests E2E
□ Documentation API
□ Performance optimization
□ Security audit
□ Cross-module integration tests

Livrable: Module prêt pour production
```

### 6.2 Ordre de Développement des Fichiers

```
SEMAINE 1 (Fondations):
  1. local_store/store_models.py
  2. local_store/product_models.py
  3. local_store/order_models.py
  4. tests/models/test_local_store_models.py

SEMAINE 2 (Core):
  1. services/store_service.py
  2. services/catalog_service.py
  3. services/search_service.py
  4. api/store_routes.py
  5. api/product_routes.py
  6. api/search_routes.py

SEMAINE 3 (Transactions):
  1. services/order_service.py
  2. services/payment_service.py
  3. integrations/stripe_integration.py
  4. integrations/notification_service.py
  5. api/order_routes.py

SEMAINE 4 (Intelligence):
  1. agents/discovery_agent.py
  2. agents/vendor_assistant.py
  3. agents/pricing_advisor.py
  4. services/analytics_service.py
  5. api/vendor_routes.py

SEMAINE 5 (Polish):
  1. tests/e2e/test_local_store_journeys.py
  2. docs/local_store_api.md
  3. Performance tests
  4. Security review
```

---

## 7. VALIDATION R&D

### 7.1 Checklist par Fichier

```
POUR CHAQUE FICHIER, VÉRIFIER:

□ Rule #1 - Human Sovereignty
  □ Actions sensibles ont human gates
  □ Pattern DRAFT → APPROVE → EXECUTE
  □ Pas d'exécution autonome

□ Rule #2 - Autonomy Isolation
  □ IA en mode suggestion/analyse
  □ Pas de modification directe
  □ User approuve suggestions

□ Rule #3 - Sphere Integrity
  □ Sphère clairement identifiée
  □ Cross-sphere = workflow explicite
  □ Data transfer = approbation

□ Rule #4 - My Team
  □ Pas d'agent → agent direct
  □ Human entre chaque étape

□ Rule #5 - Social
  □ Tris explicites
  □ Pas de ranking caché
  □ Chronologique par défaut

□ Rule #6 - Traceability
  □ id, created_at, created_by
  □ updated_at, updated_by si modifiable
  □ Audit log si sensible

□ Rule #7 - Continuity
  □ Aligné architecture existante
  □ Utilise patterns existants
  □ Pas de contradiction R&D
```

### 7.2 Tests de Conformité

```python
# tests/rnd/test_local_store_compliance.py

def test_human_gate_on_store_publish():
    """Rule #1: Publication boutique requiert approbation"""
    store = create_draft_store()
    
    # Tenter de publier sans approbation
    with pytest.raises(HumanApprovalRequired):
        store_service.publish(store.id)
    
    # Approuver puis publier
    store_service.approve(store.id, approved_by=owner_id)
    result = store_service.publish(store.id)
    assert result.status == StoreStatus.ACTIVE


def test_ai_suggestions_are_sandbox():
    """Rule #2: IA ne modifie pas directement"""
    product = create_product(price=10.00)
    
    # Suggestion IA
    suggestion = pricing_agent.suggest_price(product.id)
    
    # Vérifier que le prix n'a pas changé
    product_after = product_service.get(product.id)
    assert product_after.price == 10.00
    
    # Suggestion est un draft
    assert suggestion.status == "pending_review"


def test_no_ranking_algorithm():
    """Rule #5: Pas de ranking caché"""
    stores = search_service.search(
        query="boulangerie",
        sort_by="distance"
    )
    
    # Vérifier tri explicite par distance
    distances = [s.distance_km for s in stores]
    assert distances == sorted(distances)


def test_traceability_on_all_entities():
    """Rule #6: Traçabilité complète"""
    store = create_store()
    
    assert store.id is not None
    assert store.created_at is not None
    assert store.created_by is not None
```

---

## 8. QUESTIONS POUR JO

Avant de continuer le développement, j'aimerais ta validation sur:

### 8.1 Priorités Business

```
1. Quel persona vendeur prioriser?
   □ Marie (Boulangère) - Simple, volume
   □ Jean (Fermier) - Abonnements, marchés
   □ Sophie (Artisane) - Portfolio, personnalisé

2. Quel marché géographique d'abord?
   □ Montréal
   □ Québec ville
   □ Tout le Québec
```

### 8.2 Fonctionnalités MVP

```
Pour le MVP, on inclut:
□ Création boutique ✅
□ Catalogue produits ✅
□ Commandes en ligne ✅
□ Paiement Stripe ✅

On reporte à V2:
□ Abonnements/paniers récurrents?
□ Marchés multi-vendeurs?
□ Livraison (vs pickup only)?
□ Agents IA?
```

### 8.3 Intégrations

```
Priorité intégrations:
□ Shopping (afficher produits locaux)
□ Start Business (parcours entrepreneur)
□ Autre?
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    ⏳ EN ATTENTE VALIDATION JO ⏳                             ║
║                                                                               ║
║  Document: Planification Stratégique Local Store                             ║
║  Status: DRAFT                                                               ║
║  Prochaine étape: Validation puis développement                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Jo, ce plan te convient? Des ajustements avant qu'on commence à coder?** 🎯
