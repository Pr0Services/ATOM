# 🔌 CHE·NU — Architecture Hiérarchique des Connexions

## 📐 Principe Fondamental

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           COMPTE PRINCIPAL                                    ║
║                    (Vue GLOBALE - Contrôle TOTAL)                            ║
║                                                                               ║
║  📊 Base de données utilisateur                                              ║
║  🔌 TOUTES les connexions plateformes                                        ║
║  🔑 TOUTES les clés API                                                      ║
║  ⚙️ Contrôle des accès par sphère                                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                   │                                           ║
║         ┌─────────────────────────┼─────────────────────────┐                 ║
║         ▼                         ▼                         ▼                 ║
║  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐         ║
║  │ 🏠 Personal │           │ 💼 Business │           │ 🎨 Studio   │  ...    ║
║  │             │           │             │           │             │         ║
║  │ Voit SES    │           │ Voit SES    │           │ Voit SES    │         ║
║  │ connexions  │           │ connexions  │           │ connexions  │         ║
║  │ autorisées  │           │ autorisées  │           │ autorisées  │         ║
║  └─────────────┘           └─────────────┘           └─────────────┘         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 Deux Niveaux d'Accès

### 1️⃣ Niveau COMPTE (Global)
**Localisation:** `Paramètres → Connexions`

| Fonctionnalité | Description |
|----------------|-------------|
| Vue globale | Voit TOUTES les connexions |
| Ajouter | Peut connecter de nouvelles plateformes |
| Supprimer | Peut déconnecter toute plateforme |
| Accorder accès | Donne accès à une sphère |
| Révoquer accès | Retire l'accès d'une sphère |
| Permissions | Configure read/write par sphère |

### 2️⃣ Niveau SPHÈRE (Filtré)
**Localisation:** Dans chaque Bureau → section "Connexions"

| Fonctionnalité | Description |
|----------------|-------------|
| Vue filtrée | Voit SEULEMENT ses connexions autorisées |
| Utiliser | Peut utiliser les connexions selon permissions |
| Demander | Peut demander accès à d'autres connexions |
| ❌ Ajouter | NE PEUT PAS ajouter de nouvelles connexions |
| ❌ Supprimer | NE PEUT PAS supprimer de connexions |

---

## 🗂️ Catégories de Connexions

| Catégorie | Exemples | Sphères typiques |
|-----------|----------|------------------|
| **storage** | Google Drive, Dropbox, OneDrive | Personal, Business |
| **calendar** | Google Calendar, Outlook | Personal, Business |
| **email** | Gmail, Outlook Mail | Personal, Business |
| **communication** | Slack, Discord, Teams | Business, My Team |
| **productivity** | Notion, Trello, Asana | Business, Studio |
| **social** | Instagram, Twitter, LinkedIn | Social & Media |
| **development** | GitHub, GitLab | Studio, My Team |
| **finance** | QuickBooks, Stripe | Business |
| **government** | Services gouv. | Government |
| **creative** | Figma, Adobe, Canva | Studio |
| **entertainment** | Spotify, Netflix | Entertainment |
| **llm** | Anthropic, OpenAI | Toutes (via My Team) |
| **voice** | ElevenLabs, Deepgram | Studio, My Team |
| **image** | Stability AI, Midjourney | Studio |

---

## 🔐 Permissions par Sphère

Chaque sphère peut avoir des permissions différentes pour la même connexion:

```
Connexion Google:
├── Personal → read: ✅, write: ✅
├── Business → read: ✅, write: ❌ (lecture seule)
└── Studio   → (pas d'accès)
```

### Table d'association
```sql
connection_sphere_access:
├── connection_id
├── sphere_id
├── permissions (JSON: {read, write, delete})
├── granted_at
└── granted_by
```

---

## 🛠️ API Backend

### Routes Niveau COMPTE
```
GET  /account/connections           → Liste TOUTES les connexions
GET  /account/connections/{id}      → Détails complets avec sphères
POST /account/connections/{id}/grant-sphere   → Accorder accès
POST /account/connections/{id}/revoke-sphere  → Révoquer accès
GET  /account/connections/summary   → Résumé par catégorie/sphère
```

### Routes Niveau SPHÈRE
```
GET  /sphere/{id}/connections              → Liste connexions de la sphère
GET  /sphere/{id}/connections/{conn_id}    → Détails (permissions sphère)
GET  /sphere/{id}/available-connections    → Connexions demandables
```

---

## 🖥️ Composants Frontend

### Niveau Compte
```
frontend/src/pages/settings/
├── AccountConnectionsPage.tsx    ← Vue globale toutes connexions
├── APIKeysSettings.tsx           ← Gestion clés API
└── SettingsPage.tsx              ← Page settings principale
```

### Niveau Sphère
```
frontend/src/components/sphere/
└── SphereConnections.tsx         ← Vue filtrée par sphère

frontend/src/components/connections/
└── ConnectionsManager.tsx        ← Modal ajout connexion OAuth
```

---

## 📊 Modèle de Données

```python
class PlatformConnection:
    id: UUID
    user_id: UUID              # Propriétaire
    provider: str              # google, slack, github...
    category: ConnectionCategory
    status: ConnectionStatus
    
    # Credentials (chiffrés)
    access_token: str
    refresh_token: str
    api_key: str
    
    # Permissions globales
    permissions: {read, write, delete}
    
    # Relation many-to-many
    authorized_spheres: List[Sphere]
```

---

## 🔄 Flux d'Utilisation

### Ajouter une nouvelle connexion
```
1. Utilisateur va dans Compte → Connexions
2. Clique "Ajouter connexion"
3. Sélectionne le provider (ex: Slack)
4. OAuth / Entre API key
5. Connexion créée (status: active)
6. Choisit les sphères autorisées
7. Configure permissions par sphère
```

### Utiliser une connexion dans une sphère
```
1. Utilisateur dans Sphère Business
2. Ouvre Bureau → Section Connexions
3. Voit seulement connexions autorisées pour Business
4. Utilise Slack pour envoyer message
5. Action effectuée selon permissions (read/write)
```

### Demander accès supplémentaire
```
1. Utilisateur dans Sphère Studio
2. Voit qu'il n'a pas accès à Slack
3. Clique "Demander accès"
4. Notification envoyée (ou auto-accordé si même user)
5. Accès ajouté avec permissions configurées
```

---

## ✅ Résumé

| Niveau | Voit | Peut faire |
|--------|------|------------|
| **COMPTE** | Toutes connexions | Tout (CRUD, permissions) |
| **SPHÈRE** | Ses connexions | Utiliser, demander |

**Principe de gouvernance:** Le compte contrôle, les sphères utilisent!

---

*Architecture CHE·NU v29 — Décembre 2025*
