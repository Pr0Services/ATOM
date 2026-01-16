# 🏠 CHE·NU Demo System V51

[![Version](https://img.shields.io/badge/version-51.0.0-blue.svg)](https://chenu.ai)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Language](https://img.shields.io/badge/language-fr--CA-green.svg)](locales/fr)

> **Governed Intelligence Operating System** for the Construction Industry

---

## 🌳 The Tree Laws

```
┌─────────────────────────────────────────────────────────────────┐
│  🌳 TREE LAW 1: No Automatic Memory Write                       │
│     → No persistent change without explicit human approval       │
├─────────────────────────────────────────────────────────────────┤
│  🌳 TREE LAW 2: No Autonomous Decision                          │
│     → AI proposes, human disposes - always                       │
├─────────────────────────────────────────────────────────────────┤
│  🌳 TREE LAW 3: Total Transparency                              │
│     → Every event traced, nothing hidden                         │
└─────────────────────────────────────────────────────────────────┘
```

**These laws are CONSTITUTIONAL and IMMUTABLE.**

---

## 📊 Dataset Contents

| Category | Count | Description |
|----------|-------|-------------|
| Memory Units | 75 | Core knowledge units across 6 spheres |
| Agents | 168 | Hierarchical AI agents (L0-L3) |
| Decisions | 15 | Sample governance decisions |
| Sessions | 12 | Demo session recordings |
| Projects | 10 | Sample Quebec construction projects |
| Events | 2,000+ | System event fixtures |

---

## 🔮 Core Modules

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| **Reflection Room** | Cognitive entry point | Context-free by default |
| **Memory Inspector** | Browse memory | Read-only always |
| **Incident Mode** | Forensic audit | Total transparency |
| **Demo Replay** | Session navigation | Forensic, not cinematic |
| **Presenter Mode** | Presentation overlay | Notes for presenter only |

---

## 🏗️ Quebec Construction Focus

Built-in compliance support for:
- **RBQ** - Régie du bâtiment du Québec
- **CNESST** - Workplace safety
- **CCQ** - Construction industry relations
- **Novoclimat 2.0** - Energy efficiency

---

## 📁 Structure

```
CHENU_DEMO_SYSTEM_V51/
├── data/datasets/       # Core JSON datasets
├── ui/components/       # React components
├── ui/themes/           # CSS themes (dark, light, incident)
├── demo/flows/          # Presentation flows
├── exports/templates/   # Export HTML templates
├── crypto/              # Signing utilities
├── tests/fixtures/      # Test data (10k+ events)
├── config/              # App configuration
├── locales/             # i18n (fr, en)
└── docs/                # Documentation
```

---

## 🎬 Demo Flows

### Ultra-Short (90 seconds)
Quick elevator pitch covering essential concepts.

### Live Demo (5-15 minutes)
Full interactive exploration of all modules.

---

## 🔐 Security

- **Signing**: HMAC-SHA256 (demo) / Ed25519 (production)
- **Audit**: Append-only, immutable event log
- **Verification**: Cryptographic signature on all exports

---

## 🚀 Quick Start

```javascript
// Load dataset
import dataset from './data/datasets/memory_units.json';

// Access spheres
const spheres = dataset.spheres;

// Iterate memory units
dataset.memory_units.forEach(unit => {
  console.log(`${unit.unit_id}: ${unit.content.title}`);
});
```

---

## 📜 Philosophy

> "CHE·NU is not alive because it acts. 
>  It is alive because it remembers, exposes, and waits."

The system is **semi-living** through:
1. **Memory** - Persistent, governed knowledge
2. **Trace** - Complete event history
3. **Wait** - Always awaits human decision

---

## 📄 License

Proprietary - Demo Use Only

© 2025 CHE·NU - Governed Intelligence Operating System

---

*Built for Quebec construction. Governed by humans. Always.*
