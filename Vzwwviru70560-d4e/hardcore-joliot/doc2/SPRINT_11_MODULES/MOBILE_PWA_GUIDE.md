# 📱 CHE·NU™ - Mobile & PWA Guide

## 🎯 Vue d'Ensemble

CHE·NU v40 est maintenant **production-ready** avec support mobile complet et PWA.

### Fonctionnalités Mobile
- ✅ **Responsive Design** (Mobile/Tablet/Desktop)
- ✅ **PWA** (Installable, Offline, Push)
- ✅ **Touch Gestures** (Swipe, Tap, Long-press)
- ✅ **Bottom Navigation** (5 actions principales)
- ✅ **Quick Capture** (Modal optimisé mobile)
- ✅ **Virtual Keyboard** (Gestion automatique)

---

## 📐 Breakpoints

```css
Mobile:   < 768px   (Portrait iPhone, Android)
Tablet:   768-1023px (iPad, Android tablets)
Desktop:  > 1024px  (Laptop, Desktop)
Large:    > 1440px  (Large monitors)
```

---

## 🧩 Composants Mobile

### MobileNav
Navigation latérale avec 2 onglets (Spheres, Menu):

```tsx
import { MobileNav } from '@/components/MobileNav';

<MobileNav 
  isOpen={navOpen}
  onClose={() => setNavOpen(false)}
/>
```

### MobileBottomNav
Barre de navigation fixe en bas:

```tsx
import { MobileBottomNav } from '@/components/MobileBottomNav';

<MobileBottomNav />
```

**Actions:**
1. 🎯 Spheres - Ouvrir sélecteur de sphères
2. 📝 Workspace - Basculer workspace
3. ✨ Nova - Ouvrir Nova (principal)
4. ⚡ Capture - Quick capture
5. 💬 Chat - Communication hub

### MobileQuickCapture
Modal capture rapide avec limite 500 caractères:

```tsx
import { MobileQuickCapture } from '@/components/MobileQuickCapture';

<MobileQuickCapture
  isOpen={captureOpen}
  onClose={() => setCaptureOpen(false)}
  onSubmit={(content) => handleCapture(content)}
/>
```

---

## 🎣 Hooks Mobile

### useMobile
Détection du type de device:

```tsx
import { useMobile } from '@/hooks/useMobile';

const { isMobile, isTablet, isDesktop } = useMobile();
```

### useTouchGestures
Gestion des gestes tactiles:

```tsx
import { useTouchGestures } from '@/hooks/useTouchGestures';

useTouchGestures({
  onSwipeLeft: () => nextSphere(),
  onSwipeRight: () => prevSphere(),
  onSwipeUp: () => openWorkspace(),
  onSwipeDown: () => closeWorkspace()
});
```

### useOrientation
Détection orientation portrait/landscape:

```tsx
import { useOrientation } from '@/hooks/useOrientation';

const orientation = useOrientation();
// 'portrait' | 'landscape'
```

### useOffline
Détection mode hors-ligne:

```tsx
import { useOffline } from '@/hooks/useOffline';

const isOffline = useOffline();
```

### useVirtualKeyboard
Détection clavier virtuel:

```tsx
import { useVirtualKeyboard } from '@/hooks/useVirtualKeyboard';

const { isKeyboardVisible, keyboardHeight } = useVirtualKeyboard();
```

---

## 🌐 PWA Setup

### Service Worker
Enregistrement automatique:

```tsx
import { registerServiceWorker } from '@/pwa/registerServiceWorker';

// Dans App.tsx
useEffect(() => {
  registerServiceWorker();
}, []);
```

### Manifest
Fichier `/public/manifest.json` configuré avec:
- 8 icônes (72px → 512px)
- Shortcuts (Quick Capture, Nova)
- Screenshots (desktop, mobile)
- Theme colors

### Offline Storage
IndexedDB pour données hors-ligne:

```tsx
import { offlineStorage } from '@/pwa/offlineStorage';

// Sauvegarder thread
await offlineStorage.saveThread(thread);

// Récupérer thread
const thread = await offlineStorage.getThread(threadId);

// Actions en attente
await offlineStorage.savePendingAction(action);
const pending = await offlineStorage.getPendingActions();
```

### Push Notifications
Demander permission:

```tsx
import { requestNotificationPermission } from '@/pwa/registerServiceWorker';

const permission = await requestNotificationPermission();
if (permission === 'granted') {
  // Subscribe to push
}
```

---

## 🎨 CSS Mobile

### Imports
```tsx
import '@/styles/mobile.css';
import '@/styles/responsive.css';
```

### Classes Utilitaires

```css
.mobile-only { display: none; }
@media (max-width: 767px) {
  .mobile-only { display: block; }
  .desktop-only { display: none; }
}
```

### Safe Area Insets (iOS)
```css
.mobile-bottom-nav {
  padding-bottom: env(safe-area-inset-bottom);
}
```

### Touch Optimizations
```css
/* Cibles tactiles minimales 44x44px */
button, a, input {
  min-height: 44px;
  min-width: 44px;
}
```

---

## 📲 Installation PWA

### iOS (Safari)
1. Ouvrir chenu.com
2. Appuyer sur bouton "Partager" 
3. "Sur l'écran d'accueil"
4. Confirmer

### Android (Chrome)
1. Ouvrir chenu.com
2. Menu → "Installer l'application"
3. Confirmer

### Desktop (Chrome/Edge)
1. Icône + dans barre d'adresse
2. "Installer"

---

## 🧪 Tests Mobile

### Component Tests
```bash
npm test -- Mobile.test.tsx
```

### E2E Mobile
```bash
# iPhone 12
npx playwright test --project="Mobile Chrome"

# Tous devices
npx playwright test mobile-pwa.spec.ts
```

### Tests PWA
- Manifest valide
- Service Worker enregistré
- Mode offline
- Push notifications
- Background sync

---

## 🚀 Performance Mobile

### Optimisations
- ✅ Code splitting par route
- ✅ Lazy loading composants
- ✅ Images responsive
- ✅ Cache service worker
- ✅ Compression gzip

### Métriques Cibles
- **FCP** (First Contentful Paint): < 1.8s
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **Lighthouse Mobile**: > 90

---

## 🔧 Debug Mobile

### Chrome DevTools
1. F12 → Toggle device toolbar
2. Sélectionner device (iPhone, Pixel, etc.)
3. Tester touch events

### Safari iOS
1. iPhone → Réglages → Safari → Avancé → Web Inspector
2. Mac → Safari → Développement → [Device]

### Remote Debugging Android
1. `chrome://inspect`
2. Connecter device via USB
3. Debugging activé sur Android

---

## 📊 Analytics Mobile

Événements trackés:
- `mobile_install` - Installation PWA
- `mobile_quick_capture` - Utilisation quick capture
- `mobile_swipe` - Gestes swipe
- `mobile_offline` - Mode offline activé
- `mobile_push_enabled` - Notifications activées

---

## 🐛 Issues Connues

### iOS Safari
- Service Worker limité
- Push notifications non supportées
- Add to Home Screen manuel

### Android
- Différences entre browsers
- Permissions notifications

### Workarounds
- Fallback sans service worker
- Détection capabilities
- Progressive enhancement

---

## 📚 Resources

- **MDN PWA**: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps
- **Web.dev Mobile**: https://web.dev/mobile/
- **iOS PWA**: https://developer.apple.com/progressive-web-apps/
- **Android TWA**: https://developer.chrome.com/docs/android/trusted-web-activity/

---

*CHE·NU™ Mobile - Governed Intelligence in your pocket*
