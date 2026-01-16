# CHE·NU Demo System V51

## 🏠 Governed Intelligence Operating System

**CHE·NU** (prononcé "Chez Nous") est un système d'exploitation d'intelligence artificielle constitutionnellement gouverné, conçu pour l'industrie de la construction au Québec.

> "CHE·NU is not alive because it acts. It is alive because it remembers, exposes, and waits."

---

## 🌳 Les Tree Laws

Trois lois fondamentales et **immuables** gouvernent tout comportement du système:

| Loi | Nom | Description |
|-----|-----|-------------|
| **1** | Pas d'écriture mémoire automatique | Aucune modification de la mémoire persistante sans approbation humaine explicite |
| **2** | Pas de décision autonome | Le système ne prend jamais de décision ayant un impact réel sans validation humaine |
| **3** | Transparence totale | Chaque événement est tracé et auditable. Le Mode Incident révèle tout. |

Ces lois sont **constitutionnelles** et ne peuvent jamais être modifiées, contournées ou ignorées.

---

## 📦 Structure du Dataset V51

```
CHENU_DEMO_SYSTEM_V51/
├── data/
│   ├── datasets/           # Données principales
│   │   ├── memory_units.json      (75 unités)
│   │   ├── decisions.json         (15 décisions)
│   │   ├── sessions.json          (12 sessions)
│   │   ├── archives.json          (8 archives)
│   │   ├── sphere_mappings.json   (6 sphères)
│   │   ├── agent_configs.json     (168 agents)
│   │   └── project_details.json   (10 projets)
│   ├── fixtures/           # Fixtures de test
│   └── seeds/              # Données d'initialisation
├── ui/
│   ├── components/         # Composants React
│   ├── layouts/            # Layouts d'application
│   └── themes/             # Thèmes CSS
├── demo/
│   ├── flows/              # Parcours de démonstration
│   ├── replay/             # Sessions enregistrées
│   └── recordings/         # Captures vidéo/audio
├── exports/
│   ├── templates/          # Templates HTML
│   ├── samples/            # Exemples d'exports
│   └── signed/             # Exports signés
├── crypto/
│   ├── keys/               # Clés de signature
│   └── verification/       # Rapports de vérification
├── tests/
│   ├── unit/               # Tests unitaires
│   ├── integration/        # Tests d'intégration
│   ├── e2e/                # Tests end-to-end
│   └── fixtures/           # Fixtures de test (10k+ events)
├── config/                 # Configuration
├── locales/                # Traductions (fr/en)
└── docs/                   # Documentation
```

---

## 🔮 Modules Principaux

### 1. Salle de Réflexion
Point d'entrée principal. Espace cognitif **sans contexte imposé** où l'utilisateur peut réfléchir librement. Les propositions de mémoire sont générées mais **attendent toujours** l'approbation humaine.

### 2. Inspecteur Mémoire
Vue **lecture seule** de la structure mémoire. Navigation par sphères, visualisation des relations, recherche avancée.

### 3. Mode Incident
Visualisation **forensique** de tous les événements système. Timeline interactive, filtrage avancé, export pour audit.

### 4. Relecture Démo
Navigation **temporelle** dans les événements enregistrés. Mode forensique - navigation seulement, pas de replay d'actions.

### 5. Mode Présentateur
Overlay UI pour guider les présentations. Notes et cues visibles uniquement par le présentateur.

---

## 🤖 Architecture des Agents

**168+ agents** organisés en 4 niveaux hiérarchiques:

| Niveau | Rôle | Nombre |
|--------|------|--------|
| L0 | Orchestrateur Principal | 1 |
| L1 | Directeurs de Département | 8 |
| L2 | Chefs d'Équipe | 24 |
| L3 | Spécialistes | 135 |

### Départements
- 📅 **Planification** (18 agents)
- 💰 **Estimation** (15 agents)
- 📋 **Conformité** (20 agents)
- ✅ **Qualité** (12 agents)
- 🦺 **Sécurité** (16 agents)
- 📄 **Documentation** (14 agents)
- 📢 **Communication** (10 agents)
- 🎨 **Studio Créatif** (38 agents, 7 sous-studios)

### Routage Multi-LLM
Support pour Claude, GPT-4, Gemini, et Ollama avec routage intelligent basé sur le type de tâche.

---

## 📊 Sphères de Connaissances

| Sphère | Description | Couleur |
|--------|-------------|---------|
| 🏠 Système | Configuration et état | `#4a9eff` |
| 🌳 Gouvernance | Tree Laws, contrats | `#81c784` |
| 🤖 Agents | 168+ agents spécialisés | `#9e4aff` |
| 🏗️ Projets | Projets de construction | `#ff9e4a` |
| 📋 Conformité | RBQ, CNESST, CCQ | `#e57373` |
| 📚 Connaissances | Base métier construction | `#4dd0e1` |

---

## 🔐 Signature Cryptographique

Tous les exports sont signés cryptographiquement:

- **Algorithme**: HMAC-SHA256 (production: Ed25519)
- **Vérification**: Incluse dans chaque export
- **Audit Trail**: Permanent et immuable

---

## 🎬 Demo Flows

### Ultra-Court (90 secondes)
Pour elevator pitch. 5 étapes couvrant les concepts essentiels.

### Live Demo (5-15 minutes)
Présentation interactive complète. 13 étapes avec exploration de tous les modules.

---

## 📜 Conformité Québec

Support intégré pour:
- **RBQ** - Régie du bâtiment du Québec
- **CNESST** - Santé et sécurité du travail
- **CCQ** - Commission de la construction du Québec
- **Code du bâtiment** - Normes de construction
- **Novoclimat 2.0** - Efficacité énergétique

---

## 🚀 Utilisation

```bash
# Charger les données
import data from './data/datasets/memory_units.json'

# Accéder aux sphères
const spheres = data.spheres

# Parcourir les unités mémoire
data.memory_units.forEach(unit => {
  console.log(unit.unit_id, unit.content.title)
})
```

---

## 📄 Licence

Propriétaire - Usage démo uniquement

© 2025 CHE·NU - Governed Intelligence Operating System
