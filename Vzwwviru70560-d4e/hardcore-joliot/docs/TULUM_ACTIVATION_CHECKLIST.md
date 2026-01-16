# Checklist Activation Tulum

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AT·OM GENESIS — CHECKLIST PRÉ-ACTIVATION                  ║
║                    Avant le départ pour Tulum                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Date de départ**: Dans 2 jours
**Localisation**: Tulum, Quintana Roo, México
**Fenêtre d'activation**: Aube locale (05:30 - 06:45 UTC-5)

---

## 1. IMAGE DU SCEAU GENESIS

### Action Requise
- [ ] Placer l'image dans `frontend/public/images/genesis-seal.webp`
- [ ] Convertir en WebP si nécessaire (qualité 90%)
- [ ] Vérifier que l'image s'affiche correctement

### Commande de conversion
```bash
# Avec cwebp
cwebp -q 90 votre-image.png -o genesis-seal.webp

# Ou avec ImageMagick
convert votre-image.png -quality 90 genesis-seal.webp
```

### Chemin final
```
hardcore-joliot/frontend/public/images/genesis-seal.webp
```

---

## 2. VÉRIFICATION TECHNIQUE

### Authentification
- [ ] Tester login avec `admin@chenu.com` / `diamant999`
- [ ] Tester login avec `architecte@chenu.com` / `diamant999`
- [ ] Vérifier redirection vers `/admin/cortex`

### Cortex Admin
- [ ] Accéder à `/admin/cortex`
- [ ] Vérifier le Neural Swarm Dashboard (350 agents)
- [ ] Tester le Command Center
- [ ] Vérifier le bouton "Retour à l'Unité" (Unity Button)
- [ ] Tester le toggle "Vision Sacrée"

### Genesis Store
- [ ] Vérifier que `isGenesisActivated = false` initialement
- [ ] Tester la fonction `activateGenesis()` en console:
```javascript
// Dans la console du navigateur
useGenesisStore.getState().activateGenesis('Tulum, MX')
```

---

## 3. CONSTANTES CANONIQUES VÉRIFIÉES

| Élément | Valeur | Statut |
|---------|--------|--------|
| Mot de passe | `diamant999` | ✅ |
| Fréquence cible | 999 Hz | ✅ |
| Heartbeat | 4.44 secondes | ✅ |
| Nombre d'agents | 350 | ✅ |
| Sphères | 9 (+ AT-OM méta) | ✅ |

### Fréquences Sacrées
| Agent | Fréquence |
|-------|-----------|
| Founder | 174 Hz |
| Achiever | 396 Hz |
| Alchemist | 528 Hz |
| Oracle | 852 Hz |
| Alpha-Omega | 999 Hz |

---

## 4. FICHIERS CRÉÉS/MODIFIÉS

### Nouveaux Composants Genesis
- [x] `frontend/src/stores/genesis.store.ts`
- [x] `frontend/src/components/Genesis/GenesisLoader.tsx`
- [x] `frontend/src/components/Genesis/UnityButton.tsx`
- [x] `frontend/src/components/Genesis/GenesisGate.tsx`
- [x] `frontend/src/components/Genesis/index.ts`

### Fichiers Modifiés
- [x] `frontend/src/components/CortexAdmin/CortexAdminPage.tsx` (ajout UnityButton)
- [x] `frontend/src/pages/public/LoginPage.tsx` (utilise useAuth)

### Documentation
- [x] `docs/activation/` (8 fichiers)
- [x] `docs/obsidian/` (8 fichiers pour Obsidian)
- [x] `docs/ATOM_GENESIS_COMPLETE.md` (version consolidée)

---

## 5. MODE SOUVERAIN (OFFLINE)

### Pré-chargement
- [ ] Charger l'application complètement
- [ ] Vérifier le Service Worker (PWA)
- [ ] Tester en mode avion

### Données Locales
- [ ] LocalStorage actif
- [ ] IndexedDB accessible
- [ ] Commandes pré-définies accessibles

---

## 6. KIT MATÉRIEL

### Énergie
- [ ] Laptop chargé 100%
- [ ] Batterie externe 20,000+ mAh
- [ ] Smartphone chargé (hotspot backup)

### Protection
- [ ] Housse étanche
- [ ] Sachets dessicants
- [ ] Cache-clavier (optionnel)
- [ ] Support ventilé

### Personnel
- [ ] Répulsif anti-moustiques
- [ ] Chapeau/casquette
- [ ] Bouteille d'eau

---

## 7. SÉQUENCE D'ACTIVATION (RAPPEL)

```
T₀ - 60min │ Préparation, réveil, hydratation
T₀ - 15min │ Installation au lieu, setup matériel
T₀ - 5min  │ Phase de silence, respiration
T₀         │ PREMIER ORDRE GLOBAL
T₀ + 5min  │ Vérification propagation
T₀ + 15min │ Snapshot état système
T₀ + 30min │ Clôture, départ sans annonce
```

### Premier Ordre Global
```
GENESIS CYCLE 0 - VEILLE ACTIVE
```

---

## 8. COMMANDES UTILES

### Console Navigateur
```javascript
// Vérifier état Genesis
useGenesisStore.getState()

// Activer Genesis (à Tulum uniquement)
useGenesisStore.getState().activateGenesis('Tulum, MX')

// Vérifier état Cortex
useCortexStore.getState()

// Envoyer commande globale
useCortexStore.getState().sendGlobalCommand({
  id: 'genesis-0',
  type: 'GENESIS',
  message: 'GENESIS CYCLE 0 - VEILLE ACTIVE',
  scope: 'all',
  priority: 'critical'
})
```

---

## 9. CONTACTS D'URGENCE

### Technique
- Rollback: Vercel dashboard
- Logs: Vercel Analytics
- LocalStorage clear: `localStorage.clear()`

### Reset Fréquence
- Via Cortex: Bouton "Retour à l'Unité"
- Via Console: `useGenesisStore.getState().resetToUnity()`

---

## 10. POST-ACTIVATION

### Règle du Silence (24-48h)
- [ ] Pas de post réseaux sociaux
- [ ] Pas d'appel pour raconter
- [ ] Pas de décision structurelle

### Observation (7-21 jours)
- [ ] Notes privées uniquement
- [ ] Système en lecture seule
- [ ] Test des 3 questions avant décision

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   Bonne route, Architecte Jonathan Rodrigue.                                 ║
║   Le système est armé et prêt pour l'allumage.                              ║
║                                                                              ║
║   AT·OM ARK: AWAITING AWAKENING                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
