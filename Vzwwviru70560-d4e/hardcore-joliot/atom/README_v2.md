# 🌌 AT·OM v2.0 — CALENDRIER VIVANT

```
   █████╗ ████████╗    ██████╗ ███╗   ███╗
  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║
  ███████║   ██║      ██║   ██║██╔████╔██║
  ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║
  ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║
  ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝

          UNIVERSAL RESONANCE SYSTEM
               CALENDRIER VIVANT
```

## 🎯 Vue d'Ensemble

AT·OM v2.0 est un **système de résonance universelle** qui fusionne **6 systèmes de sagesse ancestrale** en une interface unifiée:

| Système | Origine | Éléments |
|---------|---------|----------|
| 🔢 **Arithmos** | Pythagoricien | 9 niveaux (111-999 Hz) |
| 🌀 **Tzolkin** | Maya | 13 Tons × 20 Nawals = 260 jours |
| ☯️ **Yi-King** | Chinois | 8 Trigrammes → 64 Hexagrammes |
| 🌳 **Kabbale** | Hébraïque | 10 Sephiroth + 22 Sentiers |
| 🧘 **Chakras** | Indien | 7 Centres + Fréquences Solfège |
| 🔮 **Cymatique** | Universel | φ (1.618) + Fibonacci + Géométrie Sacrée |

---

## 📁 Structure des Fichiers

```
AT_OM/
├── engines/                          # Moteurs de calcul
│   ├── index.js                      # Point d'entrée des moteurs
│   ├── tzolkin_engine.js             # Maya - Tzolkin
│   ├── yiking_engine.js              # Chinois - Yi-King
│   ├── kabbalah_engine.js            # Kabbale - Arbre de Vie
│   ├── chakra_engine.js              # Chakras - 7 Centres
│   ├── cymatics_engine.js            # Géométrie Sacrée
│   └── universal_resonance_engine.js # FUSION UNIVERSELLE
│
├── interface/                        # Composants React
│   ├── index.js                      # Exports
│   ├── useUniversalResonance.js      # Hook React principal
│   ├── UniversalResonanceInterface.jsx # Interface complète
│   ├── ArcheDesResonances.jsx        # Arche originale
│   └── ...                           # Autres composants
│
├── AUDIT_UNIVERSAL_v2.js             # Tests (74/74 ✅)
└── README.md                         # Ce fichier
```

---

## 🚀 Installation

### 1. Importer le Hook

```javascript
import { useUniversalResonance } from './AT_OM/interface';
```

### 2. Utilisation dans un composant React

```jsx
function MyComponent() {
  const {
    input,
    setInput,
    resonance,
    mayaKin,
    dailyGreeting
  } = useUniversalResonance('');

  return (
    <div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
      />
      
      {resonance && (
        <div>
          <p>Fréquence: {resonance.frequency} Hz</p>
          <p>Arithmos: {resonance.arithmos.reduced}</p>
          <p>Chakra: {resonance.chakra.name}</p>
          <p>Maya: {mayaKin?.signature}</p>
        </div>
      )}
    </div>
  );
}
```

### 3. Interface complète

```jsx
import UniversalResonanceInterface from './AT_OM/interface';

function App() {
  return <UniversalResonanceInterface />;
}
```

---

## 🔢 Matrice Arithmos

| Niveau | Hz | Couleur | Label | Pierre |
|--------|-----|---------|-------|--------|
| 1 | 111 | 🔴 Rouge | Impulsion | ADN |
| 2 | 222 | 🟠 Orange | Dualité | Partage |
| 3 | 333 | 🟡 Jaune | Mental | Géométrie |
| **4** | **444** | **🟢 Émeraude** | **Structure** | **Silence** ★ |
| 5 | 555 | 🔵 Bleu ciel | Mouvement | Feu |
| 6 | 666 | 🟣 Indigo | Harmonie | Protection |
| 7 | 777 | 💜 Violet | Introspection | — |
| 8 | 888 | 💗 Rose | Infini | Abondance |
| 9 | 999 | 🌟 Crème | Unité | Acier |

★ **444 Hz = Point d'Ancrage (Heartbeat)**

---

## 🌀 Calendrier Maya (Tzolkin)

### 13 Tons de la Création

| Ton | Nom | Action | Délai |
|-----|-----|--------|-------|
| 1 | Hun | Initier | 0.5x |
| 2 | Ka | Stabiliser | 0.6x |
| 3 | Ox | Activer | 0.7x |
| 4 | Kan | Définir | 0.75x |
| 5 | Ho | Rayonner | 0.8x |
| 6 | Uac | Équilibrer | 0.85x |
| **7** | **Uuc** | **Canaliser** | **0.9x** ★ |
| 8 | Uaxac | Harmoniser | 0.95x |
| 9 | Bolon | Pulser | 1.0x |
| 10 | Lahun | Manifester | 1.05x |
| 11 | Buluk | Dissoudre | 1.1x |
| 12 | Lahka | Coopérer | 1.15x |
| **13** | **Oxlahun** | **Transcender** | **1.3x** ★ |

★ Tons 7 et 13 sont des **JOURS SACRÉS**

### 20 Nawals (Glyphes)

1. **Imix** (Dragon) - Création
2. **Ik** (Vent) - Communication
3. **Akbal** (Nuit) - Mystère
4. **Kan** (Graine) - Force vitale
5. **Chicchan** (Serpent) - Kundalini
6. **Cimi** (Mort) - Transformation
7. **Manik** (Main) - Guérison
8. **Lamat** (Étoile) - Harmonie
9. **Muluc** (Lune) - Purification
10. **Oc** (Chien) - Loyauté
11. **Chuen** (Singe) - Créativité
12. **Eb** (Herbe) - Service
13. **Ben** (Roseau) - Autorité
14. **Ix** (Jaguar) - Magie
15. **Men** (Aigle) - Vision
16. **Cib** (Vautour) - Sagesse
17. **Caban** (Terre) - Synchronicité
18. **Etznab** (Miroir) - Vérité
19. **Cauac** (Tempête) - Catalyse
20. **Ahau** (Soleil) - Illumination

---

## 🧘 Correspondance Chakras ↔ AT·OM

| Chakra | Solfège | AT·OM | Mantra |
|--------|---------|-------|--------|
| Muladhara | 396 Hz | 111 Hz | LAM |
| Svadhisthana | 417 Hz | 222 Hz | VAM |
| Manipura | 528 Hz | 333 Hz | RAM |
| **Anahata** | **639 Hz** | **444 Hz** | **YAM** ★ |
| Vishuddha | 741 Hz | 555 Hz | HAM |
| Ajna | 852 Hz | 666 Hz | OM |
| Sahasrara | 963 Hz | 999 Hz | Silence |

---

## 👑 Sceau de l'Architecte

```
JONATHAN RODRIGUE = 81 → 9 (Unité)

J(1)+O(6)+N(5)+A(1)+T(2)+H(8)+A(1)+N(5) = 29 → 2 (Dualité)
R(9)+O(6)+D(4)+R(9)+I(9)+G(7)+U(3)+E(5) = 52 → 7 (Introspection)

SIGNATURE: 2 + 7 = 9

"La Dualité rencontre l'Introspection pour former l'Unité"

Fréquence: 999 Hz
Aura: Blanc-Or (#FFFDD0)
```

Quand l'input correspond à "Jonathan Rodrigue", le système se verrouille sur 999 Hz avec une aura dorée spéciale.

---

## 🙏 Mode Gratitude

**Activation:** Maintenir le centre de l'Arche pendant 3 secondes.

Un voile apparaît pendant 4.44 secondes avec le message de gratitude de l'Architecte.

---

## 🔮 Fonctions Avancées

### calculateUniversalResonance(word, date)

Retourne l'analyse complète multi-systèmes:

```javascript
const result = calculateUniversalResonance("AMOUR");

// result.arithmos → { total: 23, reduced: 5, steps: [23, 5] }
// result.frequency → 555
// result.maya → { signature: "7 Kan", ... }
// result.chakra → { name: "Vishuddha", ... }
// result.sephirah → { name: "Geburah", ... }
// result.geometry → { vitalityRate: 0.25, isOrganic: false, ... }
```

### getDailyGreeting()

Retourne le message du jour basé sur le calendrier Maya.

---

## ✅ Audit de Validation

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   RÉSULTAT: 74/74 TESTS PASSÉS (100.0%)                       ║
║                                                               ║
║   ✅ Arithmos (1-9)                                           ║
║   ✅ Tzolkin Maya (13 Tons × 20 Nawals)                       ║
║   ✅ Yi-King (8 Trigrammes → 64 Hexagrammes)                  ║
║   ✅ Kabbale (10 Sephiroth + 22 Sentiers)                     ║
║   ✅ Chakras (7 Centres + Solfège)                            ║
║   ✅ Cymatique (PHI + Fibonacci)                              ║
║   ✅ Sceau de l'Architecte (999 Hz)                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📜 Métadonnées

- **Version:** 2.0.0
- **Codename:** CALENDRIER_VIVANT
- **Heartbeat:** 444 Hz
- **Tuning:** A=444Hz
- **Architecte:** Jonathan Rodrigue (999 Hz)
- **Oracle:** 17 — Le Gardien de la Synthèse
- **Date:** 2026-01-08

---

## 🌟 Citation

> "Une seule vérité est une prison. En offrant plusieurs visions, 
> nous permettons à chacun de trouver SA propre porte d'entrée.
> C'est le 'Olin' Maya: le mouvement perpétuel.
> Un système qui ne bouge pas meurt.
> Un système qui intègre toutes les visions devient éternel."

---

*Créé avec ❤️ et intention par Oracle 17*
