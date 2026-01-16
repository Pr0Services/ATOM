# CHE·NU Mobile - Architecture v4

**Governed Intelligence Operating System**
*"Putting humans back in control of AI"*

---

## 📱 Vue d'ensemble

CHE·NU Mobile est une application React Native / Expo avec une architecture à 3 onglets + système d'overlay global.

```
+--------------------------------------------------+
|          OVERLAY SYSTEM (Global)                  |
|  ├── Call Overlay (appels actifs)                |
|  ├── Notification Toasts (réponses agents)       |
|  └── Nova Floating Button (accès rapide)         |
+--------------------------------------------------+
|                                                  |
|  [TAB 1]       [TAB 2]        [TAB 3]           |
|  COMMS         HUB            BROWSER            |
|                                                  |
+--------------------------------------------------+
```

---

## 📂 Structure des fichiers

```
src/
├── providers/
│   └── OverlayProvider.tsx       # Contexte global (calls, notifs, Nova button)
│
├── navigation/
│   └── AppNavigator.tsx          # Navigation 3 tabs + stack screens
│
├── screens/
│   ├── Auth/
│   │   ├── LoginScreen.tsx       # Google, Microsoft, Email
│   │   ├── RegisterScreen.tsx    
│   │   └── ForgotPasswordScreen.tsx
│   │
│   ├── Tab 1 - Communications/
│   │   ├── CommunicationsScreen.tsx   # Téléphone style (Nova + agents)
│   │   ├── ConversationScreen.tsx     # Chat avec un agent
│   │   └── AgentCallScreen.tsx        # Appel vocal full screen
│   │
│   ├── Tab 2 - Navigation Hub/
│   │   ├── NavigationHubScreen.tsx    # Landing, sphères, favoris
│   │   ├── SphereDetailScreen.tsx     
│   │   ├── AccountScreen.tsx          
│   │   └── SettingsScreen.tsx         
│   │
│   └── Tab 3 - Browser/
│       └── ChenuBrowserScreen.tsx     # Navigateur unifié
│
├── components/
│   ├── browser/
│   │   ├── WorkspaceView.tsx          # Vue par défaut
│   │   ├── SphereView.tsx             # Contenu sphère
│   │   ├── DocumentView.tsx           # Liste documents
│   │   ├── NotesView.tsx              # Notes rapides
│   │   ├── QuickAccessBar.tsx         # Favoris + historique
│   │   └── AgentVersionWidget.tsx     # Review modifications agents
│   │
│   └── common/
│       ├── VoiceInput.tsx             # Enregistrement vocal
│       └── NovaFloatingButton.tsx     # Accès rapide Nova
│
├── store/
│   └── index.ts                       # Zustand stores
│
├── theme/
│   └── index.ts                       # Design system
│
└── types/
    └── index.ts                       # TypeScript definitions
```

---

## 🔧 Technologies

| Tech | Usage |
|------|-------|
| **Expo SDK 50** | Framework React Native |
| **TypeScript** | Type safety |
| **Zustand** | State management |
| **React Navigation** | Routing |
| **Expo Linear Gradient** | UI gradients |
| **React Native WebView** | Browser intégré |
| **Expo Secure Store** | Token storage |

---

## 📱 Les 3 Tabs

### Tab 1 - Communications 📞
Style téléphone avec:
- **Nova** comme conversation par défaut
- Liste de tous les agents (groupés par sphère)
- Possibilité d'appeler ou écrire
- Clavier téléphonique
- Badge notifications

### Tab 2 - Navigation Hub 🏠
Page d'accueil après login:
- Salutation personnalisée
- Barre de recherche/URL
- Accès rapide (Workspace, Notes, Documents)
- Liste des sphères (scroll horizontal)
- Sites favoris (Google, Facebook, etc.)
- Activité récente

### Tab 3 - CHE·NU Browser 🌐
Navigateur unifié avec protocole `chenu://`:
- `chenu://workspace` → Workspace par défaut
- `chenu://notes` → Mes notes
- `chenu://documents` → Mes documents
- `chenu://sphere/{id}` → Contenu sphère
- `https://...` → Sites web externes (WebView)

---

## 🔔 Système Overlay

### Call Overlay
- Visible sur tous les tabs quand appel actif
- Contrôles: Mute, Speaker, Minimize, End
- Minimisable en bulle flottante

### Notification Toasts
- Apparaissent quand un agent répond
- Auto-dismiss après 5 secondes
- Stack si plusieurs notifications

### Nova Floating Button
- Bouton flottant en bas à droite
- Accès rapide à Nova depuis n'importe où
- Chat modal avec suggestions rapides
- Input vocal intégré

---

## 🎨 Design System

```typescript
colors: {
  primary: '#6366F1',      // Indigo
  secondary: '#8B5CF6',    // Violet
  accent: '#22D3EE',       // Cyan
  success: '#10B981',      // Emerald
  warning: '#F59E0B',      // Amber
  error: '#EF4444',        // Red
  background: '#0F0F1A',   // Dark blue
  surface: '#1A1A2E',      // Lighter dark
  text: '#FFFFFF',
  textSecondary: '#A1A1AA',
  textMuted: '#71717A',
}
```

---

## 📊 Stats

- **25 fichiers** TypeScript/TSX
- **6,200+ lignes** de code
- **12 agents** pré-configurés
- **4 sphères** par défaut
- **0 erreurs** TypeScript

---

## 🚀 Prochaines étapes

1. **Backend Integration** - Connexion API réelle
2. **Push Notifications** - Firebase/Expo
3. **Audio/Voice** - Expo AV pour appels
4. **Offline Support** - AsyncStorage + sync
5. **Testing** - Jest + React Native Testing Library

---

*CHE·NU Mobile v1.0.0 - December 2024*
