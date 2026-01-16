# 6. Sécurité et Gouvernance

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHAPITRE 6 — GARDE-FOUS DU SYSTÈME                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6.1 Gouvernance Humaine

### Principe Fondamental

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRIMAUTÉ HUMAINE                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   L'HUMAIN reste :                                               │
│                                                                  │
│   • SOURCE D'INTENTION                                           │
│     Le système n'a pas de volonté propre                         │
│                                                                  │
│   • POINT DE VALIDATION                                          │
│     Toute action significative requiert approbation              │
│                                                                  │
│   • AUTORITÉ FINALE                                              │
│     Pouvoir de veto absolu et instantané                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Hiérarchie de Contrôle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PYRAMIDE DE GOUVERNANCE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                         ┌─────────┐                                 │
│                         │ HUMAIN  │  ← Décision finale              │
│                         │(Archit.)│                                 │
│                         └────┬────┘                                 │
│                              │                                      │
│                    ┌─────────┴─────────┐                            │
│                    │                   │                            │
│               ┌────┴────┐         ┌────┴────┐                       │
│               │ AT·OM   │         │ CORTEX  │  ← Supervision        │
│               │ (Vision)│         │ (Admin) │                       │
│               └────┬────┘         └────┬────┘                       │
│                    │                   │                            │
│                    └─────────┬─────────┘                            │
│                              │                                      │
│                    ┌─────────┴─────────┐                            │
│                    │     CHE-NU        │  ← Exécution               │
│                    │   (350 Agents)    │                            │
│                    └───────────────────┘                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Règle d'Autonomie

```
┌──────────────────────────────────────────────────────────────────┐
│                    LIMITE D'AUTONOMIE                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   AUCUNE autonomie TOTALE des agents n'est autorisée             │
│                                                                  │
│   Un agent peut :                                                │
│   ✓ Proposer des actions                                         │
│   ✓ Collecter des informations                                   │
│   ✓ Analyser des données                                         │
│   ✓ Préparer des recommandations                                 │
│                                                                  │
│   Un agent NE peut PAS :                                         │
│   ✗ Exécuter sans approbation (actions critiques)                │
│   ✗ Modifier la gouvernance                                      │
│   ✗ Contacter des tiers sans autorisation                        │
│   ✗ Engager des ressources financières                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6.2 Auditabilité

### Traçabilité Complète

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRINCIPE DE TRAÇABILITÉ                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CHAQUE action dans le système doit être :                      │
│                                                                  │
│   • IDENTIFIABLE                                                 │
│     Qui a fait quoi                                              │
│                                                                  │
│   • HORODATÉE                                                    │
│     Quand exactement (timestamp UTC)                             │
│                                                                  │
│   • CONTEXTUALISÉE                                               │
│     Pourquoi (ordre source, intention)                           │
│                                                                  │
│   • PERSISTÉE                                                    │
│     Stockée de manière durable                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Structure des Logs

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FORMAT LOG CANONIQUE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   {                                                                 │
│     "id": "evt_20240115_143022_a7x9",                               │
│     "timestamp": "2024-01-15T14:30:22.451Z",                        │
│     "type": "COMMAND_EXECUTED",                                     │
│     "source": {                                                     │
│       "actor": "admin-1",                                           │
│       "role": "architecte",                                         │
│       "ip": "XXX.XXX.XXX.XXX"                                       │
│     },                                                              │
│     "target": {                                                     │
│       "scope": "all",                                               │
│       "agents": 350                                                 │
│     },                                                              │
│     "payload": {                                                    │
│       "command": "GENESIS CYCLE 0 - VEILLE ACTIVE"                  │
│     },                                                              │
│     "result": {                                                     │
│       "status": "success",                                          │
│       "affected": 350                                               │
│     }                                                               │
│   }                                                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Possibilité de Désactivation

```
┌──────────────────────────────────────────────────────────────────┐
│                    KILL SWITCH                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   En cas d'urgence, l'Architecte peut :                          │
│                                                                  │
│   NIVEAU 1 : PAUSE                                               │
│   └── Commande : HALT ALL                                        │
│       Effet : Tous les agents en attente                         │
│       Réversible : Oui, immédiatement                            │
│                                                                  │
│   NIVEAU 2 : STOP                                                │
│   └── Commande : EMERGENCY STOP                                  │
│       Effet : Arrêt complet des processus                        │
│       Réversible : Oui, avec redémarrage                         │
│                                                                  │
│   NIVEAU 3 : RESET                                               │
│   └── Commande : FACTORY RESET                                   │
│       Effet : Retour état initial                                │
│       Réversible : Non (perte données session)                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6.3 Anti-Dérive

### Séparations Structurelles

```
┌──────────────────────────────────────────────────────────────────┐
│                    MURS DE SÉPARATION                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   VISION ≠ EXÉCUTION                                             │
│   ─────────────────────────────────────────────────────          │
│   AT·OM définit la direction                                     │
│   CHE-NU exécute les tâches                                      │
│   → Pas d'auto-définition des objectifs                          │
│                                                                  │
│   SYMBOLIQUE ≠ DÉCISION                                          │
│   ─────────────────────────────────────────────────────          │
│   Les métaphores inspirent                                       │
│   Les décisions sont rationnelles                                │
│   → Pas de décision "parce que le symbole dit"                   │
│                                                                  │
│   INSPIRATION ≠ GOUVERNANCE                                      │
│   ─────────────────────────────────────────────────────          │
│   L'inspiration guide l'humain                                   │
│   La gouvernance contrôle le système                             │
│   → Pas de gouvernance par "feeling"                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Signaux d'Alerte Dérive

| Signal | Description | Action |
|--------|-------------|--------|
| **Justification mystique** | "Le système a dit que..." | Stop + Review |
| **Décision émotionnelle** | "Je sens que c'est bien" | Pause + Analyse |
| **Urgence artificielle** | "Il faut agir maintenant" | Délai forcé |
| **Isolation informationnelle** | Refus d'input externe | Consultation tiers |
| **Engagement irréversible** | "On ne peut plus reculer" | Vérification options |

### Protocole Anti-Dérive

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CHECKLIST ANTI-DÉRIVE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Avant CHAQUE décision significative, vérifier :                   │
│                                                                     │
│   □ Est-ce que je peux expliquer cette décision                     │
│     à un tiers rationnel ?                                          │
│                                                                     │
│   □ Est-ce que cette décision serait valide                         │
│     SANS le contexte symbolique ?                                   │
│                                                                     │
│   □ Est-ce que je peux attendre 24h avant d'agir ?                  │
│                                                                     │
│   □ Est-ce que j'ai consulté une source externe ?                   │
│                                                                     │
│   □ Est-ce que cette décision est réversible ?                      │
│                                                                     │
│   Si TOUTES les réponses sont OUI → Procéder                        │
│   Si UNE réponse est NON → Pause et réflexion                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6.4 Sécurité Technique

### Authentification

| Élément | Implémentation |
|---------|---------------|
| Mot de passe | `diamant999` (dev) |
| Tokens | JWT HS256, 1h expiry |
| Refresh | 7 jours |
| Rôles | user, admin, enterprise |

### Autorisation

| Ressource | user | admin | enterprise |
|-----------|------|-------|------------|
| Dashboard | ✓ | ✓ | ✓ |
| Sphères | ✓ | ✓ | ✓ |
| Agents | Limité | ✓ | ✓ |
| Cortex Admin | ✗ | ✓ | ✓ |
| Gouvernance | ✗ | ✓ | ✓ |

### Données Sensibles

```
┌──────────────────────────────────────────────────────────────────┐
│                    PROTECTION DONNÉES                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Données chiffrées :                                            │
│   • Mots de passe (bcrypt)                                       │
│   • Tokens (signed JWT)                                          │
│   • Communications (TLS 1.3)                                     │
│                                                                  │
│   Données NON collectées :                                       │
│   • Localisation précise (sauf si autorisé)                      │
│   • Données biométriques                                         │
│   • Contacts personnels                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Points de Contrôle

- [ ] Comprendre la primauté humaine
- [ ] Accepter les limites d'autonomie des agents
- [ ] Connaître les niveaux de kill switch
- [ ] Mémoriser la checklist anti-dérive
- [ ] Vérifier accès sécurisé fonctionnel

---

*Prochain chapitre : 07_POST_ACTIVATION.md*
