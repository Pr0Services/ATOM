# AT-OM Console Errors - FIXES

## 🔴 Erreurs Identifiées dans la Console

### 1. Service Worker MIME Type Error
```
The script has an unsupported MIME type ('text/html')
Failed to register a ServiceWorker for scope ('https://atom999.vercel.app/')
```

**Cause:** Le fichier `service-worker.js` n'existe pas ou Vercel retourne une page 404 (HTML) au lieu du JS.

**Solution:** Ajouter le fichier `service-worker.js` à la racine du projet.

---

### 2. Meta Tag Deprecated
```
<meta name="apple-mobile-web-app-capable" content="yes"> is deprecated
```

**Solution:** Dans `index.html`, remplacer:
```html
<!-- ANCIEN (déprécié) -->
<meta name="apple-mobile-web-app-capable" content="yes">

<!-- NOUVEAU -->
<meta name="mobile-web-app-capable" content="yes">
```

---

### 3. Logo192.png Missing
```
Error while trying to use the following icon from the Manifest:
https://atom999.vercel.app/logo192.png (Download error or resource isn't a valid image)
```

**Solution:** Ajouter les fichiers `logo192.png` et `logo512.png` à la racine.

Pour convertir le SVG en PNG:
1. Utiliser https://svgtopng.com/
2. Ou avec ImageMagick: `convert logo.svg -resize 192x192 logo192.png`
3. Ou avec Figma/Canva

---

## 📁 Fichiers à Ajouter au Repo

```
/
├── service-worker.js    ← NOUVEAU
├── manifest.json        ← METTRE À JOUR
├── logo192.png          ← NOUVEAU (depuis logo.svg)
├── logo512.png          ← NOUVEAU (depuis logo.svg)
└── index.html           ← MODIFIER meta tag
```

---

## 🔧 Modifications dans index.html

### Head Section - Remplacer/Ajouter:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- PWA Meta Tags - CORRIGÉS -->
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#D8B26A">
    
    <!-- Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <!-- Icons -->
    <link rel="icon" type="image/png" sizes="192x192" href="/logo192.png">
    <link rel="apple-touch-icon" href="/logo192.png">
    
    <title>AT-OM | L'Arche des Résonances</title>
</head>
```

### Service Worker Registration - À la fin du body:

```html
<script>
    // Register Service Worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then((registration) => {
                    console.log('[AT-OM] Service Worker registered:', registration.scope);
                })
                .catch((error) => {
                    console.warn('[AT-OM] Service Worker registration failed:', error);
                });
        });
    }
</script>
```

---

## 🚀 Commit

```bash
git add service-worker.js manifest.json logo192.png logo512.png
git add index.html  # après modifications

git commit -m "fix: resolve service worker and PWA manifest errors

- Add service-worker.js with proper MIME type
- Update manifest.json with correct icon paths  
- Add logo192.png and logo512.png icons
- Replace deprecated apple-mobile-web-app-capable meta tag
- Fix PWA installation support

Fixes: Console errors on atom999.vercel.app"

git push
```

---

## ✅ Vérification Post-Deploy

Après le push, dans la console de https://atom999.vercel.app:

1. Plus d'erreur MIME type
2. Plus d'avertissement meta tag
3. Plus d'erreur logo192.png
4. PWA installable (icône dans la barre d'URL)

---

**AT-OM | L'Arche des Résonances - 444 Hz**
