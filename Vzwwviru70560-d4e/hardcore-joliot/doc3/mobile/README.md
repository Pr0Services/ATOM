# CHE·NU Mobile 📱

Application mobile complète pour CHE·NU - Governed Intelligence OS

## 🚀 Fonctionnalités

### ✅ Incluses (Parité Desktop)

- **11 Sphères** - Personnel, Social, Scholar, Maison, Business, Projets, Creative, Cinema, Government, Immobilier, Associations
- **Nova AI** - Assistant IA universel avec chat en temps réel
- **Gestion de Projets** - Création, suivi, tâches, budgets
- **168 Agents IA** - Hiérarchie complète L0-L3
- **Threads/Conversations** - Historique et contexte
- **Communications** - Email, messaging
- **Calendrier** - Événements, réunions
- **Construction** - Chantiers, sécurité, conformité RBQ/CNESST/CCQ
- **Notifications Push** - Alertes en temps réel
- **Thème Dark/Light** - Support automatique
- **Authentification** - Login, Register, Forgot Password
- **Recherche globale** - Across all content

### 📱 Fonctionnalités Mobile Spécifiques

- **Touch Gestures** - Swipe, pinch, long press
- **Haptic Feedback** - Retour tactile
- **Camera Integration** - Scanner de documents
- **Location Services** - Géolocalisation chantiers
- **Voice Commands** - Commandes vocales Nova
- **Offline Support** - Mode hors-ligne
- **Biometric Auth** - Face ID / Touch ID

## 📦 Installation

```bash
# Installer les dépendances
npm install

# Démarrer en mode développement
npm start

# Lancer sur Android
npm run android

# Lancer sur iOS
npm run ios
```

## 🏗️ Structure

```
chenu_mobile/
├── App.tsx                 # Point d'entrée
├── src/
│   ├── navigation/         # React Navigation
│   ├── screens/            # Tous les écrans
│   ├── components/         # Composants réutilisables
│   ├── store/              # Zustand stores
│   ├── services/           # API services
│   ├── hooks/              # Custom hooks
│   ├── theme/              # Thèmes et styles
│   ├── types/              # TypeScript types
│   └── utils/              # Utilitaires
├── assets/                 # Images, fonts
├── app.json               # Configuration Expo
└── package.json           # Dépendances
```

## 🔧 Technologies

- **Expo SDK 50** - Framework React Native
- **React Navigation 6** - Navigation
- **Zustand** - State management
- **React Query** - Data fetching
- **TypeScript** - Type safety
- **Expo Notifications** - Push notifications
- **Expo Camera/Location** - Hardware access

## 📊 Stores

| Store | Description |
|-------|-------------|
| `useAuthStore` | Authentification utilisateur |
| `useSpheresStore` | 11 sphères et navigation |
| `useThreadsStore` | Conversations Nova |
| `useProjectsStore` | Gestion de projets |
| `useNotificationsStore` | Notifications |
| `useUIStore` | Thème et préférences UI |

## 🎨 Thèmes

Support complet Dark/Light mode avec:
- Couleurs sémantiques
- 11 couleurs de sphères
- Typographie responsive
- Shadows et elevations

## 🔐 Sécurité

- Secure Storage pour tokens
- Biometric authentication
- API encryption
- Input validation

## 📱 Builds

```bash
# Build Android APK
eas build -p android --profile preview

# Build iOS
eas build -p ios --profile preview

# Build Production
eas build -p all --profile production
```

## 🇨🇦 Conformité Québec

- RBQ intégration
- CNESST compliance
- CCQ regulations
- TPS/TVQ automatique

---

**CHE·NU Mobile** - Pro-Service Construction © 2025
