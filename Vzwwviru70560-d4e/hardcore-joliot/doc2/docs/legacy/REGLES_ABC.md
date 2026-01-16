# 📜 CHE·NU V25 — RÈGLES FONDAMENTALES (A, B, C)

> Ces règles sont **IMMUABLES** et s'appliquent à tout le système CHE·NU.

---

## 🅰️ RÈGLES A — STRUCTURE

| # | Règle | Description |
|---|-------|-------------|
| A.1 | **Chemin universel** | ESPACE → CATÉGORIE → MODULE → ACTION |
| A.2 | **10 Espaces immuables** | Les 10 espaces ne peuvent pas être modifiés |
| A.3 | **6 Actions universelles** | CREER, MODIFIER, IMPORTER, EXPORTER, ANALYSER, PUBLIER |
| A.4 | **Appartenance unique** | Toute création appartient à UN seul espace |
| A.5 | **Classification modules** | NOYAU (intouchable) vs DYNAMIQUE (modifiable) |
| A.6 | **Création d'espace** | Mode Architecte uniquement |

### Les 10 Espaces

| # | ID | Emoji | Label |
|---|-----|-------|-------|
| 1 | PERSONNEL | 👤 | Personnel |
| 2 | SOCIAL_DIVERTISSEMENT | 🎉 | Social & Divertissement |
| 3 | SCHOLAR | 📚 | Scholar |
| 4 | MAISON | 🏠 | Maison |
| 5 | ENTREPRISE | 🏢 | Entreprise |
| 6 | PROJETS | 📁 | Projets |
| 7 | CREATIVE_STUDIO | 🎨 | Creative Studio |
| 8 | GOUVERNEMENT | 🏛️ | Gouvernement |
| 9 | IMMOBILIER | 🏘️ | Immobilier |
| 10 | ASSOCIATIONS | 🤝 | Associations |

### Les 6 Actions

| Action | Emoji | Description |
|--------|-------|-------------|
| CREER | ➕ | Créer un nouvel élément |
| MODIFIER | ✏️ | Modifier un élément existant |
| IMPORTER | 📥 | Importer des données |
| EXPORTER | 📤 | Exporter des données |
| ANALYSER | 🔍 | Analyser des données |
| PUBLIER | 📢 | Publier/partager |

---

## 🅱️ RÈGLES B — VALIDATION

| # | Règle | Description |
|---|-------|-------------|
| B.1 | **Contrôleur central** | TOUTE action passe par le contrôleur |
| B.2 | **Niveaux de review** | Selon la visibilité (voir tableau) |
| B.3 | **Critères** | Structure, unicité, conflits, docs, tests, sécurité |
| B.4 | **Rejet automatique** | Module noyau, nom dupliqué, structure invalide, code malveillant |
| B.5 | **Audit complet** | Toute action est loggée |

### Niveaux de Validation

| Visibilité | Review par | Délai |
|------------|------------|-------|
| PRIVÉ | Auto-validé | Immédiat |
| ÉQUIPE | Agent IA | Minutes |
| COMMUNAUTÉ | Architecte | Heures |
| OFFICIEL | Architecte + Nova | Jours |

### Critères de Validation

| Critère | Description |
|---------|-------------|
| ✓ Structure | Conforme à A.1 (ESPACE → CATÉGORIE → MODULE → ACTION) |
| ✓ Unicité | Nom unique dans l'espace |
| ✓ Conflits | Pas de conflit avec modules existants |
| ✓ Documentation | Documentation minimale présente |
| ✓ Tests | Tests de base réussis |
| ✓ Sécurité | Pas de code malveillant |

---

## 🅲 RÈGLES C — PUBLICATION

| # | Règle | Description |
|---|-------|-------------|
| C.1 | **Types de visibilité** | Privé, Équipe, Communauté, Officiel |
| C.2 | **Process communauté** | Soumission → Review IA → Votes → Architecte → Publication |
| C.3 | **Process officiel** | Équipe CHE·NU → Tests → Docs → Architecte en Chef → Intégration |
| C.4 | **Modifications post-pub** | Dépublier, Forker, Mettre à jour, Archiver |
| C.5 | **Attribution** | Créateur TOUJOURS crédité, licence CHE·NU |

### Types de Visibilité

| Type | Qui peut voir | Qui peut créer |
|------|---------------|----------------|
| 🔒 PRIVÉ | Créateur uniquement | Mode User |
| 👥 ÉQUIPE | Équipe/entreprise | Mode User |
| 🌍 COMMUNAUTÉ | Tous les utilisateurs | Mode Creator |
| ⭐ OFFICIEL | Intégré au noyau | Mode Architect |

### Processus de Publication Communauté

```
1. 📤 Soumission par créateur
2. 🤖 Review automatique (IA)
3. 👥 Review communautaire (votes)
4. 🏛️ Validation finale Architecte
5. ✅ Publication dans la bibliothèque
```

### Processus de Publication Officielle

```
1. 👷 Création par équipe CHE·NU ou proposition validée
2. 🧪 Tests exhaustifs
3. 📝 Documentation complète
4. 🏛️ Approbation Architecte en Chef
5. ⚙️ Intégration au noyau
```

---

## 📊 RÉSUMÉ VISUEL

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CHE·NU - FLUX DE CRÉATION                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   UTILISATEUR                                                           │
│       │                                                                 │
│       ▼                                                                 │
│   ┌───────────────┐                                                    │
│   │ CREATION ROOM │  ←─── Règles A (Structure)                         │
│   └───────┬───────┘                                                    │
│           │                                                             │
│           ▼                                                             │
│   ┌───────────────────┐                                                │
│   │ CONTRÔLEUR CENTRAL│  ←─── Règles B (Validation)                    │
│   └───────┬───────────┘                                                │
│           │                                                             │
│      ┌────┴────┐                                                       │
│      ▼         ▼                                                       │
│   ┌─────┐   ┌─────┐                                                    │
│   │PRIVÉ│   │PUBLIC│  ←─── Règles C (Publication)                      │
│   └─────┘   └──┬──┘                                                    │
│                │                                                        │
│           ┌────┴────┐                                                  │
│           ▼         ▼                                                  │
│      ┌────────┐ ┌────────┐                                             │
│      │COMMUNAU│ │OFFICIEL│                                             │
│      │  TÉ    │ │        │                                             │
│      └────────┘ └────────┘                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ VIOLATIONS ET CONSÉQUENCES

| Violation | Conséquence |
|-----------|-------------|
| Modifier un module NOYAU sans autorisation | Rejet + alerte sécurité |
| Nom déjà existant | Rejet automatique |
| Structure invalide | Rejet + suggestions de correction |
| Code malveillant détecté | Rejet + blocage temporaire |
| Contourner le contrôleur | Rejet + audit |

---

## 🔐 MODULES NOYAU (PROTÉGÉS)

Ces modules ne peuvent JAMAIS être modifiés sans validation Architecte + Nova:

- `auth` - Authentification
- `controller` - Contrôleur central
- `types` - Types et enums
- `spaces` - Définition des espaces
- `config` - Configuration système

---

**CHE·NU V25** — *"Structure, Validation, Publication"* 📜
