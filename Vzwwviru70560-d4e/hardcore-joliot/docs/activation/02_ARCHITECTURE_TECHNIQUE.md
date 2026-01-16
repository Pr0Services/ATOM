# 2. Architecture Technique

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHAPITRE 2 — ARCHITECTURE TECHNIQUE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 2.1 Déploiement Cloud (Vercel)

### Infrastructure de Production

| Composant | Technologie | État |
|-----------|-------------|------|
| Frontend | React 18 + TypeScript | Déployé |
| API | FastAPI (Python) | Déployé |
| Base de données | PostgreSQL | Configuré |
| Cache | Redis | Configuré |
| CDN | Vercel Edge | Actif |

### Configuration SSL/TLS

```
┌─────────────────────────────────────────────────────────────┐
│                    SÉCURITÉ TRANSPORT                       │
├─────────────────────────────────────────────────────────────┤
│  • HTTPS obligatoire (TLS 1.3)                              │
│  • Certificat auto-renouvelé (Let's Encrypt)                │
│  • HSTS activé                                              │
│  • CSP configuré                                            │
└─────────────────────────────────────────────────────────────┘
```

### Checklist Déploiement

- [x] HTTPS actif sur tous les endpoints
- [x] DNS propre configuré
- [x] Rollback disponible (versions précédentes)
- [x] Build reproductible (CI/CD)
- [x] Variables d'environnement séparées par contexte
- [x] Monitoring activé

---

## 2.2 Cortex Admin 2 — Centre de Commande

Le **Cortex Admin 2** est le centre de commande humain du système CHE-NU.

### Architecture du Cortex

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CORTEX ADMIN 2                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │
│  │ Neural Swarm  │  │   Command     │  │  Vibrational  │           │
│  │  Dashboard    │  │    Center     │  │    Overlay    │           │
│  │               │  │               │  │               │           │
│  │  350+ Agents  │  │  Terminal     │  │  Fréquences   │           │
│  │  Vue Essaim   │  │  CHE-NU://    │  │  Sacrées      │           │
│  └───────────────┘  └───────────────┘  └───────────────┘           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SYSTEM HEALTH BAR                         │   │
│  │  [████████████████████░░░░] 85%  │  350/350 Online  │  0 ⚠   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Fonctions Principales

| Module | Fonction | Accès |
|--------|----------|-------|
| **Neural Swarm** | Visualisation des 350 agents | Admin |
| **Command Center** | Envoi d'ordres globaux | Admin |
| **Vibrational Overlay** | Fréquences & Arbre de Vie | Admin |
| **Health Monitor** | Santé système temps réel | Admin |

### Accès Sécurisé

```
Route        : /admin/cortex
Rôles requis : admin | enterprise
Mot de passe : diamant999
Email admin  : admin@chenu.com | architecte@chenu.com
```

### Principe Fondamental

```
┌──────────────────────────────────────────────────────────────────┐
│                    RÈGLE D'OR DU CORTEX                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   AUCUNE action agent n'est déclenchée sans                      │
│   ENVELOPPE DE COMMANDE EXPLICITE                                │
│                                                                  │
│   Tout ordre doit :                                              │
│   • Être tracé dans le journal                                   │
│   • Avoir un identifiant unique                                  │
│   • Être réversible ou annulable                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2.3 Base de Données & Synchronisation

### Modèle Événementiel

Le système utilise un modèle **event-sourcing** pour garantir :
- Auditabilité complète
- Reconstruction d'état
- Résilience aux pannes

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUX DE DONNÉES                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [Action Humaine]                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                           │
│   │   LOCAL     │ ← Capture immédiate                       │
│   │   STORE     │   Résilience offline                      │
│   └──────┬──────┘                                           │
│          │                                                  │
│          │ (sync quand réseau disponible)                   │
│          │                                                  │
│          ▼                                                  │
│   ┌─────────────┐                                           │
│   │   CLOUD     │ ← Reconstruction                          │
│   │   STORE     │   Diffusion multi-device                  │
│   └─────────────┘                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Principe de Résilience

```
┌──────────────────────────────────────────────────────────────────┐
│                    RÉSILIENCE RÉSEAU                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Aucune dépendance temps réel OBLIGATOIRE                       │
│                                                                  │
│   Le système DOIT survivre à :                                   │
│   • Perte réseau prolongée (heures/jours)                        │
│   • Latence élevée                                               │
│   • Connexion intermittente                                      │
│                                                                  │
│   Stratégie : LOCAL-FIRST + SYNC-WHEN-POSSIBLE                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### États de Synchronisation

| État | Description | Action |
|------|-------------|--------|
| `synced` | Local = Cloud | Aucune |
| `pending` | Local > Cloud | Sync en attente |
| `conflict` | Divergence détectée | Résolution manuelle |
| `offline` | Pas de réseau | Mode local actif |

---

## 2.4 Stack Technique Complète

### Frontend

```yaml
Framework: React 18.2
Language: TypeScript 5.x
State: Zustand + React Query
Routing: React Router 6
Styling: TailwindCSS + Framer Motion
Build: Vite
```

### Backend

```yaml
Framework: FastAPI
Language: Python 3.11+
ORM: SQLAlchemy (async)
Auth: JWT (HS256)
Cache: Redis
Queue: (prévu) Celery
```

### Infrastructure

```yaml
Hosting: Vercel
Database: PostgreSQL (Supabase/Neon)
CDN: Vercel Edge Network
Monitoring: Vercel Analytics
Logs: Structured JSON
```

---

## Points de Contrôle

- [ ] Vérifier accès HTTPS
- [ ] Tester login admin (diamant999)
- [ ] Valider accès Cortex Admin 2
- [ ] Confirmer mode offline fonctionnel
- [ ] Vérifier logs et traçabilité

---

*Prochain chapitre : 03_THEORIE_DES_CYCLES.md*
