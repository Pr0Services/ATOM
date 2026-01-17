# AT·OM - Infrastructure Invisible

**PROPRIÉTÉ EXCLUSIVE DE JONATHAN EMMANUEL RODRIGUE**
**TOUS DROITS RÉSERVÉS - BREVET EN COURS - 2025**

---

## Déploiement DigitalOcean App Platform

### Structure (Flat - Racine)
```
/
├── index.html      # Interface principale PWA
├── style.css       # Design Canon AT·OM
├── app.js          # Logique Vanilla JS
├── manifest.json   # Configuration PWA
├── icon-192.png    # Icône 192x192 (à créer)
├── icon-512.png    # Icône 512x512 (à créer)
└── README.md       # Ce fichier
```

### Instructions de Déploiement

1. **Créer un repo GitHub privé**
   - Nom: `AT-OM-999-DEPLOY-ZAMA-ALLELUYA`

2. **Upload des fichiers**
   - Copier tous les fichiers à la racine du repo

3. **DigitalOcean App Platform**
   - New App → GitHub
   - Sélectionner le repo
   - Type: **Static Site**
   - Source Directory: `/` (laisser vide)
   - Build Command: (laisser vide)
   - Output Directory: `/`

---

## Caractéristiques

| Fonctionnalité | Status |
|----------------|--------|
| PWA iPad Fullscreen | ✅ |
| Le Sceau (2s touch) | ✅ |
| L'Essaim (350 agents) | ✅ |
| Modules (Génie, Alchimie, Flux, Santé) | ✅ |
| Protocol-999 (Triple tap) | ✅ |
| Navigation Gestuelle | ✅ |
| Zero Dépendance | ✅ |

---

## Icônes Requises

Générer les icônes PNG avec votre logo:
- `icon-192.png` (192×192 pixels)
- `icon-512.png` (512×512 pixels)

Utiliser `icon.svg` comme base.

---

## Configuration API

Dans `app.js`, ligne 17:
```javascript
API_URL: 'https://api.atom-sovereign.com',
```

Remplacer par votre endpoint.

---

© 2025 Jonathan Emmanuel Rodrigue - Tous droits réservés
