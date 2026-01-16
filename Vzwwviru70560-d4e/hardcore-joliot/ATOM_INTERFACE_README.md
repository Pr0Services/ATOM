# 🌐 AT·OM INTERFACE

> **Sovereign Productivity Platform** - 10 Spheres of Civilization, Offline-First, Zero-Knowledge Architecture

![Version](https://img.shields.io/badge/version-1.0.0-atom)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Status](https://img.shields.io/badge/status-Production%20Ready-green)

---

## 🎯 Overview

AT·OM Interface is an ultra-modern productivity platform built around **10 Spheres of Civilization**. It provides complete data sovereignty through Split Identity encryption, works offline-first for deployment in any location, and features real-time synchronization with a 4.44-second heartbeat cycle.

### Key Differentiators

- **🔐 Split Identity** - Zero-knowledge architecture where your private key never leaves your device
- **📡 Offline-First** - Full functionality without network (Tulum-Ready)
- **💓 Real-Time Sync** - 4.44s heartbeat cycle with WebSocket updates
- **⚖️ Arithmos Engine** - Balance calculation across all spheres
- **🌐 10 Spheres** - Complete life management framework

---

## 🏛️ The 10 Spheres of Civilization

| Sphere | Icon | Color | Domain |
|--------|------|-------|--------|
| **Santé** | ❤️ | Emerald | Personal health and wellness |
| **Finance** | 💰 | Amber | Financial management and wealth |
| **Éducation** | 🎓 | Violet | Continuous learning |
| **Gouvernance** | 🏛️ | Blue | Administration and documents |
| **Énergie** | ⚡ | Red | Energy management |
| **Communication** | 💬 | Cyan | Networks and social |
| **Justice** | ⚖️ | Indigo | Legal aspects |
| **Logistique** | 🚚 | Orange | Transport and organization |
| **Alimentation** | 🍽️ | Green | Nutrition and supply |
| **Technologie** | 💻 | Purple | Digital tools and innovation |

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API (optional for offline mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/atom-interface.git
cd atom-interface

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### Environment Variables

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
VITE_ENABLE_OFFLINE=true
VITE_ENABLE_WEB3=true
```

---

## 📁 Project Structure

```
ATOM_INTERFACE/
├── src/
│   ├── components/          # React components
│   │   ├── Dashboard.tsx    # Main interface
│   │   ├── SphereConfigPanel.tsx
│   │   ├── IdentityPanel.tsx
│   │   ├── CommandPalette.tsx
│   │   ├── NotificationToast.tsx
│   │   ├── LoadingScreen.tsx
│   │   └── ErrorBoundary.tsx
│   │
│   ├── services/            # Core services
│   │   ├── encryption.service.ts  # Split Identity
│   │   ├── offline.service.ts     # IndexedDB & sync
│   │   ├── realtime.service.ts    # WebSocket & heartbeat
│   │   └── api.service.ts         # REST & OAuth
│   │
│   ├── stores/              # State management
│   │   └── atom.store.ts    # Zustand store
│   │
│   ├── hooks/               # Custom hooks
│   │   └── index.ts
│   │
│   ├── utils/               # Utilities
│   │   └── index.ts
│   │
│   ├── types/               # TypeScript definitions
│   │   └── index.ts
│   │
│   ├── styles/              # CSS & Tailwind
│   │   └── globals.css
│   │
│   ├── App.tsx              # App root
│   └── main.tsx             # Entry point
│
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

---

## 🔧 Architecture

### Split Identity (Zero-Knowledge)

```
┌─────────────────────────────────────────────┐
│                USER DEVICE                   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │         SPLIT IDENTITY              │   │
│  │                                     │   │
│  │  Public ID: atom_Xy7k9mN2pQ...     │   │
│  │  Public Key: [shareable]           │   │
│  │  Private Key: [NEVER LEAVES]       │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                    │                        │
│                    ▼                        │
│  ┌─────────────────────────────────────┐   │
│  │      LOCAL ENCRYPTED STORAGE        │   │
│  │                                     │   │
│  │  IndexedDB + NaCl secretbox        │   │
│  │  All data encrypted at rest        │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
                     │
                     ▼ (encrypted blobs only)
┌─────────────────────────────────────────────┐
│               SERVER (OPTIONAL)              │
│                                             │
│  • Stores encrypted data only               │
│  • Cannot decrypt anything                  │
│  • Zero knowledge of content                │
│                                             │
└─────────────────────────────────────────────┘
```

### Offline-First Architecture

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   USER ACTION  │ ──▶ │   IndexedDB    │ ──▶ │  SYNC QUEUE    │
└────────────────┘     └────────────────┘     └────────────────┘
                              │                       │
                              ▼                       ▼
                       ┌────────────────┐     ┌────────────────┐
                       │  LOCAL STATE   │     │ WHEN ONLINE:   │
                       │  (Zustand)     │     │ Process queue  │
                       └────────────────┘     └────────────────┘
```

### Real-Time Services

```
┌─────────────────────────────────────────────────────────────┐
│                     HEARTBEAT (4.44s)                        │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  WEBSOCKET  │──▶│  HEARTBEAT  │──▶│  ARITHMOS   │       │
│  │  Service    │   │  Service    │   │  Engine     │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│         │                │                   │              │
│         ▼                ▼                   ▼              │
│  Real-time events   System status      Balance calc        │
│  Sphere updates     Stability          Recommendations     │
│  Notifications      Efficiency         Harmonic index      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build

# Testing
npm run test         # Run tests
npm run test:e2e     # End-to-end tests

# Linting
npm run lint         # ESLint
npm run typecheck    # TypeScript check
```

---

## 📚 API Integration

AT·OM supports multiple authentication methods:

### OAuth2
```typescript
import { oauth2Service } from '@/services';

// Initiate OAuth flow
await oauth2Service.initiateAuth('google', {
  clientId: 'your-client-id',
  redirectUri: 'http://localhost:3000/callback',
  scope: ['profile', 'email'],
});
```

### Web3
```typescript
import { web3Service } from '@/services';

// Connect wallet
const wallet = await web3Service.connect();

// Sign message
const signature = await web3Service.signMessage('Hello AT·OM');
```

### API Key
```typescript
import { apiConnectionManager } from '@/services';

// Connect with API key
await apiConnectionManager.connect('health', {
  provider: 'withings',
  authType: 'apiKey',
  apiKey: 'your-api-key',
});
```

---

## 🎨 Customization

### Tailwind Theme

The theme is defined in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      atom: {
        50: '#faf5ff',
        500: '#a855f7',  // Primary
        900: '#581c87',
      },
      sphere: {
        health: '#10b981',
        finance: '#f59e0b',
        // ... all 10 spheres
      }
    }
  }
}
```

### Custom Hooks

```typescript
import { useHeartbeat, useArithmos, useSphereData } from '@/hooks';

// Real-time heartbeat
const { cycleNumber, systemStability } = useHeartbeat();

// Arithmos balance
const { globalBalance, recommendations } = useArithmos();

// Sphere data
const { sphere, balance, isHealthy } = useSphereData('health');
```

---

## 🔐 Security

### Encryption

- **Algorithm**: NaCl (TweetNaCl.js)
- **Key Size**: 256-bit
- **Key Derivation**: PBKDF2 (100,000 iterations)
- **At Rest**: All data encrypted with secretbox

### Privacy

- Private keys never transmitted
- No server-side decryption
- Optional recovery phrase
- Export/import your data anytime

---

## 🌐 Deployment

### Static Hosting (Recommended)

```bash
npm run build
# Upload dist/ to any static host
```

### Docker

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

### Vercel

```bash
vercel deploy
```

---

## 📖 Documentation

- [Architecture Guide](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Security Model](./docs/SECURITY.md)
- [Contributing](./CONTRIBUTING.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

Proprietary - All Rights Reserved

---

## 🙏 Acknowledgments

Built with:
- [React](https://react.dev) + [TypeScript](https://typescriptlang.org)
- [Vite](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand](https://zustand-demo.pmnd.rs)
- [Framer Motion](https://framer.com/motion)
- [TweetNaCl](https://tweetnacl.js.org)
- [Socket.io](https://socket.io)

---

<div align="center">

**AT·OM** - *Sovereign Productivity for the Digital Age*

[Website](https://atom.io) · [Documentation](https://docs.atom.io) · [Support](mailto:support@atom.io)

</div>
