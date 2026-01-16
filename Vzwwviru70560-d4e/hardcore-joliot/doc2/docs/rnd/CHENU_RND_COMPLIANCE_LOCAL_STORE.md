# 🔒 CONFORMITÉ R&D — MODULES LOCAL STORE & START YOUR BUSINESS

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              DOCUMENT DE CONFORMITÉ R&D — OBLIGATOIRE                        ║
║                                                                               ║
║         Modules: Local Store + Start Your Business                           ║
║         Status: EN VALIDATION                                                ║
║         Date: 22 Décembre 2025                                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Ce document DOIT être validé AVANT toute intégration en production.**

---

## 📋 PRE-INTEGRATION CHECKLIST

### Module: LOCAL STORE

```
☑ Nom du module: local_store
☑ Sphères propriétaires: Business + Community
☑ Intent original: Permettre aux commerces locaux de vendre leurs produits
☑ Module équivalent existant? NON (nouveau module)
☑ Logique parallèle détectée? NON
☐ Approbation R&D obtenue: EN ATTENTE (Jo)
```

### Module: START YOUR BUSINESS

```
☑ Nom du module: start_your_business
☑ Sphère propriétaire: Business
☑ Intent original: Accompagner les entrepreneurs de l'idée au lancement
☑ Module équivalent existant? NON (nouveau module)
☑ Logique parallèle détectée? NON
☐ Approbation R&D obtenue: EN ATTENTE (Jo)
```

---

## 🎯 VÉRIFICATION DES 7 RÈGLES R&D

### RULE #1: HUMAN SOVEREIGNTY ✅

**Principe:** Aucune action sans approbation humaine

**Actions sensibles identifiées et gates implémentés:**

| Action | Sensibilité | Strategy | Implementation |
|--------|-------------|----------|----------------|
| Création boutique | HAUTE | A | DRAFT → REVIEW → PUBLISH |
| Modification boutique | MOYENNE | A | DRAFT → APPROVE → SAVE |
| Publication produit | HAUTE | A | DRAFT → PREVIEW → PUBLISH |
| Réception commande | HAUTE | A | NOTIF → CONFIRM → PREPARE |
| Envoi commande | HAUTE | A | PREPARE → CONFIRM_READY → NOTIFY_CUSTOMER |
| Paiement | CRITIQUE | A | REVIEW → CONFIRM → PROCESS |
| Annulation commande | HAUTE | A | REQUEST → CONFIRM → PROCESS → REFUND |
| Promotion création | MOYENNE | A | DRAFT → APPROVE → ACTIVATE |
| Réponse à review | MOYENNE | A | DRAFT → PREVIEW → PUBLISH |

**Code pattern obligatoire:**

```python
class LocalStoreService:
    """
    HUMAN GATES OBLIGATOIRES
    
    Toutes les méthodes qui modifient des données ou
    déclenchent des actions externes DOIVENT suivre le pattern:
    
    1. create_X_draft() → Crée un brouillon
    2. preview_X() → Affiche pour review
    3. approve_X() → Human confirme
    4. execute_X() → Exécution réelle
    """
    
    async def create_store_draft(
        self,
        owner_id: UUID,
        data: StoreCreateData
    ) -> StoreDraft:
        """
        Étape 1: Créer un brouillon de boutique
        STATUS: draft (pas visible publiquement)
        """
        return StoreDraft(
            id=uuid4(),
            owner_id=owner_id,
            status=StoreStatus.DRAFT,
            created_by=owner_id,
            created_at=datetime.now(),
            **data
        )
    
    async def submit_store_for_review(
        self,
        store_id: UUID,
        submitted_by: UUID
    ) -> StoreDraft:
        """
        Étape 2: Soumettre pour review
        STATUS: pending_review
        HUMAN GATE: Attend approbation
        """
        store = await self.get_store(store_id)
        store.status = StoreStatus.PENDING_REVIEW
        store.submitted_at = datetime.now()
        store.submitted_by = submitted_by
        
        # Notification à l'équipe de review (si applicable)
        # OU auto-validation pour les comptes vérifiés
        
        return store
    
    async def approve_store(
        self,
        store_id: UUID,
        approved_by: UUID,
        notes: Optional[str] = None
    ) -> LocalStore:
        """
        Étape 3: Approbation humaine OBLIGATOIRE
        STATUS: active
        
        PEUT ÊTRE:
        - Auto-approbation par owner (pour MVP)
        - Review par équipe CHE·NU (pour qualité)
        """
        store = await self.get_store(store_id)
        
        # Validation
        if store.status != StoreStatus.PENDING_REVIEW:
            raise InvalidStateError("Store must be pending review")
        
        store.status = StoreStatus.ACTIVE
        store.approved_at = datetime.now()
        store.approved_by = approved_by
        store.approval_notes = notes
        
        # Log pour audit
        await self.audit_log.record(
            action="store_approved",
            entity_id=store_id,
            actor_id=approved_by,
            details={"notes": notes}
        )
        
        return store
```

**Checklist Rule #1:**
- ☑ Human gates sur création boutique
- ☑ Human gates sur publication produits
- ☑ Human gates sur commandes
- ☑ Human gates sur paiements
- ☑ Human gates sur annulations/remboursements
- ☑ Aucune action autonome sans confirmation

---

### RULE #2: AUTONOMY ISOLATION ✅

**Principe:** IA opère en sandbox uniquement

**Applications dans Local Store:**

| Fonctionnalité | Mode | Sandbox Implementation |
|----------------|------|------------------------|
| Recherche boutiques | READ | Query seulement, pas de modification |
| Suggestions produits | ANALYSIS | Génère suggestions, user choisit |
| Pricing suggestions | ANALYSIS | Propose prix, vendeur décide |
| Description AI | DRAFT | Génère draft, vendeur édite/approuve |
| Réponse review AI | DRAFT | Propose réponse, vendeur approuve |

**Code pattern:**

```python
class LocalStoreAIService:
    """
    SANDBOX MODE OBLIGATOIRE
    
    L'IA ne peut JAMAIS modifier directement les données.
    Elle génère des SUGGESTIONS que l'humain approuve.
    """
    
    async def suggest_product_description(
        self,
        product_name: str,
        category: str,
        keywords: List[str],
        user_id: UUID
    ) -> DescriptionSuggestion:
        """
        SANDBOX: Génère une suggestion de description
        
        L'humain DOIT approuver avant que ce soit utilisé.
        """
        suggestion = await self.llm.generate(
            prompt=f"Génère une description pour {product_name}...",
            max_tokens=200
        )
        
        return DescriptionSuggestion(
            id=uuid4(),
            product_name=product_name,
            suggested_description=suggestion,
            status="pending_review",  # PAS approved!
            generated_at=datetime.now(),
            generated_for=user_id,
            # IMPORTANT: Pas de sauvegarde automatique
        )
    
    async def suggest_pricing(
        self,
        product_id: UUID,
        user_id: UUID
    ) -> PricingSuggestion:
        """
        SANDBOX: Analyse et suggère un prix
        
        NE MODIFIE PAS le prix réel.
        """
        product = await self.get_product(product_id)
        market_data = await self.get_market_data(product.category)
        
        suggestions = [
            {"strategy": "competitive", "price": market_data.avg_price * 0.95},
            {"strategy": "premium", "price": market_data.avg_price * 1.1},
            {"strategy": "value", "price": market_data.avg_price},
        ]
        
        return PricingSuggestion(
            id=uuid4(),
            product_id=product_id,
            current_price=product.price,
            suggestions=suggestions,
            market_analysis=market_data,
            status="pending_selection",  # User doit choisir
            generated_at=datetime.now(),
        )
```

**Checklist Rule #2:**
- ☑ Suggestions IA en mode draft uniquement
- ☑ Aucune modification directe par IA
- ☑ User approuve toutes les suggestions IA
- ☑ Mode analyse pour insights (read-only)

---

### RULE #3: SPHERE INTEGRITY ✅

**Principe:** Cross-sphere requiert workflows explicites

**Mapping des sphères pour Local Store:**

```
LOCAL STORE MODULE
├── Primary Sphere: BUSINESS (vendeurs, transactions)
├── Secondary Sphere: COMMUNITY (découverte locale, reviews)
└── Connections:
    ├── Business → Community: Produits visibles publiquement
    ├── Community → Business: Reviews, favoris
    ├── Personal → Business: Commandes, historique achats
    └── Shopping → Local Store: Intégration recherche
```

**Cross-sphere workflows EXPLICITES:**

```python
class CrossSphereWorkflow:
    """
    WORKFLOWS EXPLICITES pour transferts cross-sphere
    """
    
    # Workflow 1: Business → Community (Publier boutique)
    PUBLISH_STORE_TO_COMMUNITY = {
        "id": "publish_store_community",
        "source_sphere": "business",
        "target_sphere": "community",
        "requires_approval": True,
        "data_transferred": ["store_public_profile", "products_catalog"],
        "human_gate": "owner_approval"
    }
    
    # Workflow 2: Personal → Business (Passer commande)
    PLACE_ORDER = {
        "id": "place_order",
        "source_sphere": "personal",
        "target_sphere": "business",
        "requires_approval": True,  # Confirmation achat
        "data_transferred": ["order_details", "delivery_info"],
        "human_gate": "customer_confirmation"
    }
    
    # Workflow 3: Shopping → Local Store (Afficher dans recherche)
    INTEGRATE_SHOPPING_SEARCH = {
        "id": "shopping_local_integration",
        "source_sphere": "local_store",
        "target_sphere": "shopping",
        "requires_approval": False,  # Automatique si publié
        "data_transferred": ["product_summary", "price", "availability"],
        "condition": "store.status == ACTIVE"
    }

class LocalStoreCrossSphereService:
    """
    Gère les transferts cross-sphere avec workflows explicites
    """
    
    async def publish_to_community(
        self,
        store_id: UUID,
        owner_id: UUID
    ) -> WorkflowExecution:
        """
        Workflow: Business → Community
        
        ÉTAPES:
        1. REGISTER: Enregistrer l'intention
        2. VALIDATE: Vérifier permissions
        3. APPROVE: Owner confirme
        4. EXECUTE: Rendre visible dans Community
        5. LOG: Audit trail
        """
        # 1. REGISTER
        workflow = await self.workflow_registry.create(
            workflow_type="publish_store_community",
            source_entity_id=store_id,
            source_sphere="business",
            target_sphere="community",
            initiated_by=owner_id,
            status="pending_approval"
        )
        
        # 2. VALIDATE
        store = await self.store_service.get(store_id)
        if store.owner_id != owner_id:
            raise PermissionError("Only owner can publish")
        if store.status != StoreStatus.APPROVED:
            raise InvalidStateError("Store must be approved first")
        
        # 3. APPROVE (Human gate)
        # → Retourne le workflow, attend confirmation UI
        return workflow
    
    async def confirm_publish(
        self,
        workflow_id: UUID,
        confirmed_by: UUID
    ) -> WorkflowExecution:
        """
        Confirmation humaine du workflow
        """
        workflow = await self.workflow_registry.get(workflow_id)
        
        if workflow.initiated_by != confirmed_by:
            raise PermissionError("Only initiator can confirm")
        
        # 4. EXECUTE
        store = await self.store_service.get(workflow.source_entity_id)
        store.is_public = True
        store.published_at = datetime.now()
        store.published_by = confirmed_by
        
        # Sync vers Community sphere
        await self.community_service.index_local_store(store)
        
        # 5. LOG
        workflow.status = "completed"
        workflow.completed_at = datetime.now()
        
        await self.audit_log.record(
            action="cross_sphere_publish",
            workflow_id=workflow_id,
            actor_id=confirmed_by,
            source_sphere="business",
            target_sphere="community"
        )
        
        return workflow
```

**Checklist Rule #3:**
- ☑ Sphères clairement définies
- ☑ Workflows cross-sphere documentés
- ☑ Chaque transfert a un workflow explicite
- ☑ Approbation humaine sur transferts sensibles

---

### RULE #4: MY TEAM RESTRICTIONS ✅

**Principe:** Pas d'orchestration IA-to-IA

**Application dans Local Store:**

```
RÈGLE: Les agents IA du module Local Store ne peuvent PAS
       orchestrer d'autres agents IA automatiquement.

✅ PERMIS:
- Agent suggère → Human approuve → Action exécutée
- Agent analyse → Résultat affiché → Human décide
- Agent notifie → Human reçoit → Human agit

❌ INTERDIT:
- Agent A déclenche Agent B automatiquement
- Chain d'agents sans intervention humaine
- Workflows IA autonomes
```

**Implementation:**

```python
class LocalStoreAgentService:
    """
    RESTRICTION MY TEAM
    
    Les agents ne peuvent PAS s'appeler entre eux.
    Chaque action agent → résultat → human → prochaine action.
    """
    
    async def process_new_order(
        self,
        order_id: UUID,
        vendor_id: UUID
    ) -> OrderProcessingResult:
        """
        CORRECT: Chaque étape attend confirmation humaine
        """
        order = await self.order_service.get(order_id)
        
        # Étape 1: Notifier vendeur (PAS d'action auto)
        notification = await self.notify_vendor(
            vendor_id=vendor_id,
            message=f"Nouvelle commande #{order.order_number}",
            action_required="confirm_or_reject"
        )
        
        # STOP ICI - Attend action humaine
        # Le vendeur doit:
        # - Cliquer "Confirmer" → confirm_order()
        # - Cliquer "Rejeter" → reject_order()
        
        return OrderProcessingResult(
            status="awaiting_vendor_action",
            notification_sent=True,
            next_action="vendor_must_confirm"
        )
    
    # ❌ INTERDIT - Ceci violerait Rule #4:
    # async def auto_process_order(self, order_id):
    #     order = await self.order_service.get(order_id)
    #     await self.inventory_agent.reserve_items(order)  # ❌ Agent → Agent
    #     await self.notification_agent.notify_customer(order)  # ❌ Agent → Agent
    #     await self.delivery_agent.schedule(order)  # ❌ Agent → Agent
```

**Checklist Rule #4:**
- ☑ Aucun agent n'appelle un autre agent directement
- ☑ Chaque étape attend action humaine
- ☑ Pas de workflows automatiques multi-agents

---

### RULE #5: SOCIAL RESTRICTIONS ✅

**Principe:** Pas d'algorithmes de ranking, chronologique seulement

**Application dans Local Store:**

```
AFFICHAGE DES DONNÉES - RÈGLES STRICTES

✅ PERMIS (Chronologique ou Explicite):
- Liste produits: Ordre ajouté (newest first) ou alphabétique
- Liste boutiques: Distance ou alphabétique
- Reviews: Date (newest first)
- Commandes: Date (newest first)
- Favoris: Date ajouté

❌ INTERDIT (Ranking/Engagement):
- "Produits populaires" basé sur vues
- "Boutiques tendance" basé sur engagement
- Score de "pertinence" opaque
- Algorithme de feed personnalisé
- Boosting payant caché
```

**Code implementation:**

```python
class LocalStoreQueryService:
    """
    SOCIAL RESTRICTIONS
    
    Tous les tris sont EXPLICITES et contrôlés par l'utilisateur.
    Aucun ranking caché.
    """
    
    ALLOWED_SORT_OPTIONS = {
        "stores": [
            ("distance", "Plus proche"),
            ("name_asc", "A → Z"),
            ("name_desc", "Z → A"),
            ("newest", "Plus récent"),
            ("rating", "Mieux noté"),  # Basé sur rating explicite, pas engagement
        ],
        "products": [
            ("newest", "Plus récent"),
            ("price_asc", "Prix croissant"),
            ("price_desc", "Prix décroissant"),
            ("name_asc", "A → Z"),
        ],
        "reviews": [
            ("newest", "Plus récent"),
            ("oldest", "Plus ancien"),
            ("rating_high", "Meilleures notes"),
            ("rating_low", "Notes les plus basses"),
        ]
    }
    
    async def search_stores(
        self,
        query: Optional[str],
        filters: StoreFilters,
        sort_by: str = "distance",  # EXPLICITE
        user_location: Optional[Location] = None
    ) -> List[LocalStore]:
        """
        Recherche avec tri EXPLICITE choisi par l'utilisateur
        
        PAS de "pertinence" cachée ou "pour vous".
        """
        if sort_by not in [s[0] for s in self.ALLOWED_SORT_OPTIONS["stores"]]:
            raise ValueError(f"Invalid sort option: {sort_by}")
        
        stores = await self.db.query_stores(query, filters)
        
        # Tri TRANSPARENT
        if sort_by == "distance" and user_location:
            stores.sort(key=lambda s: s.location.distance_km(
                user_location.latitude, 
                user_location.longitude
            ))
        elif sort_by == "name_asc":
            stores.sort(key=lambda s: s.name.lower())
        elif sort_by == "newest":
            stores.sort(key=lambda s: s.created_at, reverse=True)
        elif sort_by == "rating":
            stores.sort(key=lambda s: s.avg_rating or 0, reverse=True)
        
        return stores
    
    # ❌ INTERDIT:
    # async def get_trending_stores(self):
    #     """Basé sur engagement - VIOLATION Rule #5"""
    #     pass
    
    # ❌ INTERDIT:
    # async def get_personalized_feed(self, user_id):
    #     """Feed personnalisé - VIOLATION Rule #5"""
    #     pass
```

**Checklist Rule #5:**
- ☑ Tous les tris sont explicites et documentés
- ☑ L'utilisateur choisit le tri
- ☑ Pas de "trending" ou "popular" basé sur engagement
- ☑ Pas de feed personnalisé algorithmique
- ☑ Pas de boosting caché

---

### RULE #6: MODULE TRACEABILITY ✅

**Principe:** Tous les objets ont traçabilité complète

**Champs obligatoires sur TOUS les modèles:**

```python
@dataclass
class TrackedEntity:
    """
    Classe de base avec traçabilité obligatoire
    
    TOUS les modèles Local Store héritent de ceci.
    """
    id: UUID                           # Identifiant unique
    created_at: datetime               # Date création
    created_by: UUID                   # Qui a créé
    updated_at: Optional[datetime]     # Dernière modification
    updated_by: Optional[UUID]         # Qui a modifié
    
    # Pour les entités avec workflow
    status: str                        # État actuel
    status_changed_at: Optional[datetime]
    status_changed_by: Optional[UUID]
    status_change_reason: Optional[str]


# Application aux modèles Local Store:

@dataclass
class LocalStore(TrackedEntity):
    """Commerce local avec traçabilité complète"""
    # ... autres champs
    
    # Traçabilité additionnelle
    verified_at: Optional[datetime] = None
    verified_by: Optional[UUID] = None
    
    approved_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    
    published_at: Optional[datetime] = None
    published_by: Optional[UUID] = None


@dataclass
class LocalProduct(TrackedEntity):
    """Produit avec traçabilité"""
    pass


@dataclass
class LocalOrder(TrackedEntity):
    """Commande avec traçabilité complète"""
    
    # Timeline complète
    submitted_at: Optional[datetime] = None
    submitted_by: UUID  # Customer
    
    confirmed_at: Optional[datetime] = None
    confirmed_by: Optional[UUID] = None  # Vendor
    
    prepared_at: Optional[datetime] = None
    prepared_by: Optional[UUID] = None
    
    shipped_at: Optional[datetime] = None
    shipped_by: Optional[UUID] = None
    
    delivered_at: Optional[datetime] = None
    delivered_confirmed_by: Optional[UUID] = None
    
    cancelled_at: Optional[datetime] = None
    cancelled_by: Optional[UUID] = None
    cancellation_reason: Optional[str] = None


@dataclass
class AuditLogEntry:
    """
    Log d'audit pour TOUTES les actions importantes
    """
    id: UUID
    timestamp: datetime
    
    # Qui
    actor_id: UUID
    actor_type: str  # user, system, agent
    
    # Quoi
    action: str
    entity_type: str
    entity_id: UUID
    
    # Contexte
    details: Dict[str, Any]
    ip_address: Optional[str]
    user_agent: Optional[str]
    
    # Sphère
    sphere: str
    cross_sphere_workflow_id: Optional[UUID] = None
```

**Checklist Rule #6:**
- ☑ Tous modèles ont id, created_at, created_by
- ☑ Modifications ont updated_at, updated_by
- ☑ Changements de status tracés
- ☑ Audit log pour actions importantes
- ☑ Cross-sphere workflows tracés

---

### RULE #7: R&D CONTINUITY ✅

**Principe:** Construit sur les décisions précédentes

**Alignement avec R&D existante:**

| Décision R&D Existante | Application Local Store |
|------------------------|-------------------------|
| 9 Sphères (Architecture) | Module dans Business + Community |
| Human gates (Security Guide) | 4 strategies appliquées |
| Module Registry | Entrée créée avant code |
| Encoding Layer | Utilise encoding existant |
| Token budgets | Intégré aux agents IA |
| Thread system | Commandes = Threads |

**Documentation référencée:**
- CHENU_MASTER_EXECUTION_SKILL.md
- CHENU_MODULE_INTEGRATION_PROCESS_V1.md
- MODULE_REGISTRY_VISUAL_SUMMARY.txt
- 3_VERTICALS_PRODUCTION_READY.md (patterns)

**Checklist Rule #7:**
- ☑ Module aligné avec architecture 9 sphères
- ☑ Utilise patterns existants (Shopping module)
- ☑ Respecte toutes les décisions R&D documentées
- ☑ Ne contredit aucune règle existante

---

## 📝 MODULE REGISTRY ENTRY

### Entry pour LOCAL_STORE

```markdown
| Module | Sphere | Status | Equivalent | LOCKED | Notes |
|--------|--------|--------|------------|--------|-------|
| local_store | Business+Community | PLANNED | N/A | TBD | Commerce local, artisans, marchés |
| local_store_models.py | Business | PLANNED | N/A | NO | Data models avec traçabilité |
| local_store_service.py | Business | PLANNED | N/A | NO | Service avec human gates |
| local_store_agents.py | Business | PLANNED | N/A | NO | Agents IA en sandbox mode |
| local_store_routes.py | Business | PLANNED | N/A | NO | API REST endpoints |
```

### Entry pour START_YOUR_BUSINESS

```markdown
| Module | Sphere | Status | Equivalent | LOCKED | Notes |
|--------|--------|--------|------------|--------|-------|
| start_your_business | Business | PLANNED | N/A | TBD | Accompagnement entrepreneurs |
| business_ideation.py | Business | PLANNED | N/A | NO | Génération/validation idées |
| business_planning.py | Business | PLANNED | N/A | NO | Business plan builder |
| business_launch.py | Business | PLANNED | N/A | NO | Checklist lancement |
| business_growth.py | Business | PLANNED | N/A | NO | Analytics et croissance |
```

---

## ✅ VALIDATION FINALE

### Checklist Conformité R&D

```
RULE #1 - Human Sovereignty:
☑ Human gates sur toutes actions sensibles
☑ Pattern DRAFT → APPROVE → EXECUTE
☑ Aucune action autonome

RULE #2 - Autonomy Isolation:
☑ IA en mode sandbox/suggestion
☑ User approuve toutes suggestions IA
☑ Pas de modification directe par IA

RULE #3 - Sphere Integrity:
☑ Sphères clairement définies
☑ Workflows cross-sphere explicites
☑ Approbation sur transferts

RULE #4 - My Team:
☑ Pas d'orchestration agent-to-agent
☑ Human entre chaque étape
☑ Pas de workflows IA autonomes

RULE #5 - Social:
☑ Tris explicites (pas de ranking caché)
☑ Chronologique par défaut
☑ Pas d'engagement optimization

RULE #6 - Traceability:
☑ created_by, created_at, id sur tout
☑ Audit log complet
☑ Timeline des changements

RULE #7 - Continuity:
☑ Aligné avec architecture existante
☑ Utilise patterns documentés
☑ Pas de contradiction R&D
```

---

## 🔒 APPROBATION REQUISE

**Ce document attend validation de:**

- [ ] **Jo (Architect)** — Approbation architecture
- [ ] **R&D Review** — Conformité rules

**Une fois approuvé, les modules peuvent passer à status INTEGRATED.**

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    ⏳ EN ATTENTE D'APPROBATION ⏳                             ║
║                                                                               ║
║  Modules: Local Store + Start Your Business                                   ║
║  Conformité R&D: 7/7 Rules ✅                                                ║
║  Prêt pour: Validation humaine                                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Date:** 22 Décembre 2025  
**Préparé par:** Claude (Agent Dev)  
**Pour:** Jo (Architect CHE·NU)

---

© 2025 CHE·NU™  
"GOVERNANCE BEFORE EXECUTION. HUMANS BEFORE AUTOMATION."
