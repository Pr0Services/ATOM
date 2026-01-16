# CHE·NU — PRIVACY MANIFEST
## Privacy et Gouvernance des Données
### Foundation Freeze V1.0.0 — FROZEN

---

## 1. Philosophie

CHE·NU applique une politique de **privacy-by-default**.

> "La vie privée n'est pas une fonctionnalité. C'est un droit fondamental."

---

## 2. Principes de Privacy (FROZEN)

| Principe | Application |
|----------|-------------|
| **Private by default** | Tout est privé sauf décision contraire |
| **Minimal collection** | Seules les données nécessaires sont collectées |
| **Purpose limitation** | Les données servent uniquement leur but déclaré |
| **User ownership** | L'utilisateur possède ses données |

---

## 3. Classification des Données

| Niveau | Description | Accès |
|--------|-------------|-------|
| **Personnel** | Données de la sphère Personnel | Utilisateur uniquement |
| **Privé** | Données des autres sphères | Utilisateur + agents autorisés |
| **Partagé** | Données explicitement partagées | Destinataires choisis |
| **Public** | Données publiées | Tous |

---

## 4. Droits de l'Utilisateur

| Droit | Description |
|-------|-------------|
| **Accès** | Consulter toutes ses données |
| **Export** | Télécharger ses données dans un format standard |
| **Rectification** | Corriger des données erronées |
| **Suppression** | Effacer ses données |
| **Portabilité** | Transférer ses données vers un autre système |
| **Opposition** | Refuser certains traitements |

---

## 5. Données JAMAIS Collectées

CHE·NU ne collecte **jamais** :

| Donnée | Raison |
|--------|--------|
| Données biométriques comportementales | Loi 2 |
| Profils psychologiques | Loi 2 |
| Scores de productivité | Loi 2 |
| Métriques d'attention | Loi 3 |
| Graphes d'influence | Loi 2 |
| Historique de navigation externe | Privacy |
| Contacts non autorisés | Loi 4 |

---

## 6. Isolation des Données par Sphère

```
┌─────────────────────────────────────────────────────────┐
│               DATA ISOLATION MODEL                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  DB     │  │  DB     │  │  DB     │  │  DB     │    │
│  │Personal │  │Business │  │ Scholar │  │Creative │    │
│  │ 🔒🔒🔒  │  │  🔒🔒   │  │  🔒🔒   │  │  🔒🔒   │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │            │          │
│       ╳            ▼            ▼            ▼          │
│   ISOLATED   ┌─────────────────────────────────────┐   │
│              │          CONTEXT BRIDGE              │   │
│              │    (seul pont autorisé)             │   │
│              │    (avec consentement)              │   │
│              └─────────────────────────────────────┘   │
│                                                         │
│  ╳ = Aucun accès possible (sphère Personnel)           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Chiffrement

| Contexte | Chiffrement |
|----------|-------------|
| **Au repos** | AES-256 |
| **En transit** | TLS 1.3 |
| **Sphère Personnel** | Chiffrement utilisateur (E2E) |
| **Backups** | Chiffrés avec clé utilisateur |

---

## 8. Audit et Traçabilité

| Propriété | Valeur |
|-----------|--------|
| **Traçabilité** | Toutes les actions sont tracées |
| **Explicabilité** | Chaque décision est explicable |
| **Revue utilisateur** | L'utilisateur peut auditer son système |
| **Transparence** | Pas d'opération cachée |

---

## 9. Gouvernance

```
┌─────────────────────────────────────────────────────────┐
│                  GOVERNANCE MODEL                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    ┌──────────────┐                     │
│                    │    USER      │                     │
│                    │  (Souverain) │                     │
│                    └──────┬───────┘                     │
│                           │                             │
│                           │ Contrôle total              │
│                           ▼                             │
│                    ┌──────────────┐                     │
│                    │   DONNÉES    │                     │
│                    │  (Propriété) │                     │
│                    └──────┬───────┘                     │
│                           │                             │
│              ┌────────────┼────────────┐                │
│              ▼            ▼            ▼                │
│       ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│       │  Accès   │ │  Export  │ │Suppression│           │
│       └──────────┘ └──────────┘ └──────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 10. Conformité Réglementaire

CHE·NU est conçu pour faciliter la conformité avec :

| Réglementation | Région |
|----------------|--------|
| **RGPD** | Europe |
| **Loi 25** | Québec |
| **CCPA** | Californie |
| **PIPEDA** | Canada |

---

## 11. Rétention des Données

| Type | Rétention |
|------|-----------|
| **Données utilisateur** | Jusqu'à suppression par l'utilisateur |
| **Logs techniques** | 30 jours max |
| **Données de session** | Durée de session uniquement |
| **Données supprimées** | Purge effective sous 30 jours |

---

## 12. Déclaration de Privacy

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   CHE·NU s'engage à :                                     ║
║                                                           ║
║   ✓ Ne jamais vendre les données utilisateur              ║
║   ✓ Ne jamais partager sans consentement                  ║
║   ✓ Ne jamais profiler les utilisateurs                   ║
║   ✓ Toujours permettre l'export                           ║
║   ✓ Toujours permettre la suppression                     ║
║   ✓ Toujours être transparent                             ║
║                                                           ║
║   Ces engagements sont IMMUABLES.                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

*Document Status: FROZEN — Foundation Freeze V1.0.0*
