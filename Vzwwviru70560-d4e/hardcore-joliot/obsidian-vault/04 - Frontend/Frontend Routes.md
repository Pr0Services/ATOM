# Frontend Routes

> Routes Canon AT·OM et navigation

---

## Routes Principales

| Route | Composant | Description |
|-------|-----------|-------------|
| `/` | LeSceau | Activation souveraine (2s touch) |
| `/essaim` | Essaim | Hub des 350 agents |
| `/swarm` | Essaim | Alias anglais |
| `/genie` | Genie | Module Education |
| `/alchimie` | Alchimie | Visualiseur frequences |
| `/flux` | Flux | Mouvements de valeur |
| `/sante` | Sante | Bio-feedback |
| `/protocol-999` | Protocol999 | Kill-Switch (cache) |

---

## Page: Le Sceau (/)

**Fichier**: `src/pages/LeSceau.tsx`

### Fonctionnalite
- Ecran noir avec cercle central pulsant
- Touch 2 secondes pour activer
- Frequence monte de 432Hz a 999Hz
- Explosion de 350 particules

### Animation
```typescript
const SCEAU_DURATION = 2000; // ms
const START_FREQUENCY = 432;
const TARGET_FREQUENCY = 999;

// Progression lineaire
const progress = Math.min(elapsed / SCEAU_DURATION, 1);
const frequency = START_FREQUENCY + (TARGET_FREQUENCY - START_FREQUENCY) * progress;
```

### Sortie
- Succes: Navigation vers `/essaim`
- Echec: Reset animation

---

## Page: L'Essaim (/essaim)

**Fichier**: `src/pages/Essaim.tsx`

### Fonctionnalite
- Visualisation 3D de 350 agents
- Zoom/Pan avec gestes tactiles
- Click sur agent = details

### Structure
```typescript
interface SwarmAgent {
  id: number;
  sphere: string;
  x: number;  // -1 to 1
  y: number;
  z: number;
  frequency: number;
}
```

### WebSocket
```typescript
const ws = new WebSocket(`${WS_URL}/ws/swarm`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateAgents(data.agents);
};
```

---

## Page: Genie (/genie)

**Fichier**: `src/pages/Genie.tsx`

### Fonctionnalite
- Module Education Canon AT·OM
- Clans d'apprentissage
- Agent Mentor
- Tableau blanc infini

### Sections
1. **Clans** - Groupes d'apprentissage
2. **Mentor** - Assistant IA educatif
3. **Whiteboard** - Espace collaboratif
4. **Progress** - Suivi progression

---

## Page: Alchimie (/alchimie)

**Fichier**: `src/pages/Alchimie.tsx`

### Fonctionnalite
- Visualiseur de frequences
- Spectrogramme 432-999Hz
- Structures moleculaires
- Harmonies sonores

### Frequences
| Hz | Nom | Effet |
|----|-----|-------|
| 432 | Base | Fondation |
| 528 | Guerison | Reparation |
| 639 | Connexion | Relations |
| 741 | Eveil | Intuition |
| 852 | Ordre | Retour equilibre |
| 963 | Unite | Conscience |
| 999 | Harmonie | Perfection |

---

## Page: Flux (/flux)

**Fichier**: `src/pages/Flux.tsx`

### Fonctionnalite
- Visualisation des mouvements de valeur
- PAS de termes "debit/credit"
- Particules representant les flux

### Vocabulaire
| Interdit | Utilise |
|----------|---------|
| Debit | Sortie |
| Credit | Entree |
| Balance | Equilibre |
| Transaction | Mouvement |

---

## Page: Sante (/sante)

**Fichier**: `src/pages/Sante.tsx`

### Fonctionnalite
- Interface bio-feedback
- Systemes corporels
- Exercices de respiration
- Coherence cardiaque

### Metriques
- Frequence cardiaque simulee
- Niveau de stress
- Qualite du sommeil
- Activite physique

---

## Page: Protocol-999 (/protocol-999)

**Fichier**: `src/pages/Protocol999.tsx`

### Fonctionnalite
- Interface Kill-Switch
- 3 niveaux de dispersion
- Code de confirmation requis

### Niveaux
| Niveau | % | Description |
|--------|---|-------------|
| Partiel | 20% | Agents non-essentiels |
| Sectoriel | 50% | Sphere complete |
| Total | 100% | Tous les agents |

### Securite
- Route non listee dans navigation
- Confirmation par code
- Log de l'action (sans donnees personnelles)

---

## Navigation par Gestes

### Touch Events
```typescript
// Swipe horizontal: changer de module
onTouchStart -> onTouchMove -> onTouchEnd

// Pinch: zoom dans L'Essaim
onPinchStart -> onPinchMove -> onPinchEnd

// Long press: menu contextuel
setTimeout(2000) -> showContextMenu
```

---

## Liens

- [[System Architecture]]
- [[350 Agents]]
- [[Zero Filter]]

#frontend #routes #navigation #pages
