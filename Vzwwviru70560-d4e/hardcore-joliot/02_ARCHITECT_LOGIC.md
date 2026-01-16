# 02 — ARCHITECT LOGIC

## Détails Techniques : 444Hz / 4.44s

---

### Protocole [AQUA] + [ADAMAS]

Le système AT·OM est gouverné par un protocole dual :

- **[AQUA]** — Flux, adaptabilité, fluidité des données
- **[ADAMAS]** — Structure, solidité, intégrité du système

Ensemble, ils forment la **MOELLE ÉPINIÈRE** de l'application.

---

### Constantes Fondamentales

```
ANCHOR_FREQUENCY = 444 Hz       // Fréquence d'ancrage
SIGNAL_INTERVAL  = 4.44 s       // Signal de rafraîchissement
SACRED_SEQUENCE  = [3, 6, 9, 12] // Séquence de Tesla
BALANCE_RATIO    = 30           // Somme de la séquence
CUBE_VOLUME      = 1728         // 12³ (Métatron)
```

---

### Matrice de Résonance

| Niveau | Hz | Ratio | Label | Chakra |
|--------|-----|-------|-------|--------|
| 1 | 111 | 0.25 | Impulsion | Racine |
| 2 | 222 | 0.50 | Dualité | Sacré |
| 3 | 333 | 0.75 | Mental | Plexus Solaire |
| **4** | **444** | **1.00** | **Structure** | **Cœur** ← ANCRE |
| 5 | 555 | 1.25 | Mouvement | Gorge |
| 6 | 666 | 1.50 | Harmonie | Troisième Œil |
| 7 | 777 | 1.75 | Silence | Couronne |
| 8 | 888 | 2.00 | Infini | Âme |
| 9 | 999 | 2.25 | Unité | Étoile |

---

### Formules de Calcul

```typescript
// Fréquence depuis le niveau
hz = level × 111

// Ratio depuis la fréquence
ratio = hz / 444

// Délai d'animation
delay_ms = 1000 - (level × 100)

// Racine numérique (méthode Tesla)
digitalRoot(n) = n === 0 ? 0 : 1 + ((n - 1) % 9)

// Validation 3-6-9
is369(n) = digitalRoot(n) ∈ {3, 6, 9}
```

---

### Architecture du Signal

```
┌─────────────────────────────────────────────────┐
│                    HEARTBEAT                     │
│                    4.44 seconds                  │
├─────────────────────────────────────────────────┤
│                                                  │
│   Tick #1 ──→ Tick #2 ──→ Tick #3 (◊ ALIGNED)  │
│                                                  │
│   Tick #4 ──→ Tick #5 ──→ Tick #6 (◊ ALIGNED)  │
│                                                  │
│   Tick #7 ──→ Tick #8 ──→ Tick #9 (◊ ALIGNED)  │
│                                                  │
│   Tick #10 ─→ Tick #11 ─→ Tick #12 (CYCLE END) │
│                                                  │
│                    ↓                             │
│              CYCLE + 1                           │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

### Structure des Frontends

```
frontend/
├── mirror/          # Public — Tous utilisateurs
│   └── pages/
│       ├── SignalPage.tsx     # Pre-login #1
│       ├── ManifestoPage.tsx  # Pre-login #2
│       └── GatePage.tsx       # Pre-login #3
│
├── core/            # Architecte — Monitoring
│   └── CoreApp.tsx
│       ├── Santé des 10 sphères
│       ├── Signal 4.44s visualisé
│       └── Matrice de résonance
│
└── temple/          # Sacré — Résonance
    └── TempleApp.tsx
        ├── Cube 1728 (CSS 3D)
        ├── 4 Boutons de pouvoir
        └── 15 Chakras mapping
```

---

### Hooks Principaux

```typescript
// Signal global
useSignal444({
  enabled: true,
  onTick: (state) => console.log(state.tick),
  divisor: 1  // 1 = chaque tick, 2 = tous les 2
})

// Oscillateurs scalaires
useScalarOscillator({
  volume: 0.3,
  waveform: 'sine',
  attackMs: 50
})

// Séquences Anuhazi
useAnuhaziSequences()
  .playKhufa()   // 111 → 444
  .playAriea()   // 444 → 777
  .playARaMaNa() // 777 → 1111
```

---

### Validation des Flux (3-6-9)

```typescript
function validateDataFlow(data: number[]): boolean {
  const sum = data.reduce((a, b) => a + b, 0);
  return sum % 30 === 0; // BALANCE_RATIO
}
```

---

### Backend Heartbeat

```python
# core/heartbeat.py
heartbeat = HeartbeatService()

# Au démarrage de l'app
await heartbeat.start()

# Le serveur "respire" même sans connexions
# Tick toutes les 4.44s
# Log des ticks alignés (3, 6, 9)
```

---

### Clés d'Accès

| Frontend | Clés Valides |
|----------|--------------|
| Mirror | *(accès libre)* |
| Core | `AQUA+ADAMAS`, `369`, `36912` |
| Temple | `1728`, `MUARATA`, `444` |

---

*[AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12*
