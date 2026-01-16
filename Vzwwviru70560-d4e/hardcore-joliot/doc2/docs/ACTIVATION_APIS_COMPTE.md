# 🔌 CHE·NU — Activation des APIs dans le Compte

## ✅ OUI! Les APIs peuvent s'activer dans l'application

CHE·NU permet aux utilisateurs de configurer leurs propres clés API directement depuis leur compte. Voici comment le système fonctionne:

---

## 🏗️ Architecture du Système

```
┌─────────────────────────────────────────────────────────────────┐
│                        COMPTE UTILISATEUR                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  🔗 Connexions   │  │  🔑 Clés API    │  │  ⚙️ Préférences │ │
│  │   Externes      │  │    LLM/Services │  │    IA/Nova      │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    GESTIONNAIRE INTÉGRATIONS                ││
│  │  • Stockage chiffré des clés                               ││
│  │  • Vérification automatique                                ││
│  │  • Suivi d'utilisation                                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📍 Emplacements dans l'Application

### 1. **Connexions Externes (OAuth)**
**Chemin:** `Settings → Connexions`

Permet de connecter des services externes via OAuth:
- Google Drive, Dropbox, OneDrive
- Gmail, Outlook
- Slack, Discord, Teams
- Notion, Trello, Asana
- GitHub, GitLab

**Composant:** `ConnectionsManager.tsx`

### 2. **Clés API LLM/Services** ⭐ NOUVEAU
**Chemin:** `Settings → Clés API`

Permet de configurer ses propres clés API:

| Provider | Catégorie | Description |
|----------|-----------|-------------|
| Anthropic | LLM | Claude 3.5 Sonnet, Opus, Haiku |
| OpenAI | LLM | GPT-4, GPT-4o, DALL-E, Whisper |
| Google AI | LLM | Gemini Pro, Ultra |
| Mistral AI | LLM | Mistral Large, Medium |
| Groq | LLM | Llama 3, Mixtral (ultra-rapide) |
| Cohere | LLM | Command, Embed, Rerank |
| ElevenLabs | Voice | Text-to-Speech |
| Deepgram | Voice | Speech-to-Text |
| Stability AI | Image | Stable Diffusion |
| Replicate | Image | Modèles open-source |

**Composant:** `APIKeysSettings.tsx`

### 3. **Préférences IA/Nova**
**Chemin:** `Settings → IA & Nova`

Configure les préférences d'utilisation:
- Modèle par défaut
- Température (créativité)
- Mémoire contextuelle
- Personnalité de Nova

**Composant:** `AISettings.tsx`

---

## 🔐 Sécurité des Clés API

```
┌─────────────────────────────────────────────┐
│            CYCLE DE VIE D'UNE CLÉ           │
├─────────────────────────────────────────────┤
│  1. Saisie par l'utilisateur                │
│           │                                 │
│           ▼                                 │
│  2. Validation du format (prefix)           │
│           │                                 │
│           ▼                                 │
│  3. Chiffrement (AES-256)                   │
│           │                                 │
│           ▼                                 │
│  4. Stockage sécurisé (DB/Vault)            │
│           │                                 │
│           ▼                                 │
│  5. Vérification API (appel test)           │
│           │                                 │
│           ▼                                 │
│  6. Statut: Active / Invalid / Expired      │
└─────────────────────────────────────────────┘
```

### Mesures de Sécurité:
- ✅ Clés jamais affichées en clair (masquées: `sk-ant-****...****`)
- ✅ Chiffrement avant stockage
- ✅ Possibilité de supprimer à tout moment
- ✅ Pas de transmission vers services tiers
- ✅ Audit d'utilisation

---

## 🛠️ API Backend

### Routes disponibles (`/api/v1/api-keys/`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Liste toutes les clés configurées |
| `GET` | `/providers` | Liste providers supportés |
| `POST` | `/` | Ajoute une nouvelle clé |
| `GET` | `/{provider}` | Détails d'une clé |
| `PUT` | `/{provider}` | Modifie une clé |
| `DELETE` | `/{provider}` | Supprime une clé |
| `POST` | `/{provider}/verify` | Vérifie validité |
| `GET` | `/{provider}/usage` | Stats d'utilisation |

---

## 💡 Comportement de l'Application

### Quand l'utilisateur a sa propre clé:
```
Utilisateur → Requête IA → Utilise SA clé API → Provider → Réponse
```
- Pas de frais CHE·NU pour les tokens
- Facturation directe par le provider

### Quand l'utilisateur n'a PAS de clé:
```
Utilisateur → Requête IA → Utilise clé CHE·NU → Provider → Réponse
```
- Tokens comptabilisés sur son budget CHE·NU
- Selon son niveau d'abonnement

---

## 📱 Interface Utilisateur

### Page Clés API

```
┌─────────────────────────────────────────────────────────────┐
│  🔑 Clés API                                                │
│  Configurez vos propres clés API pour utiliser les services │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ Config. │  │ Dispo.  │  │ Actives │                     │
│  │    3    │  │   12    │  │    2    │                     │
│  └─────────┘  └─────────┘  └─────────┘                     │
│                                                             │
│  [Toutes] [🧠 LLM/IA] [🎤 Voix] [🖼️ Images] [⚙️ Autres]   │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🎭 Anthropic (Claude)                       [✅ Actif]  ││
│  │ Claude 3.5 Sonnet, Opus, Haiku                         ││
│  │ sk-ant-****...****                                     ││
│  │ [🔄 Vérifier] [✏️ Modifier] [🗑️]                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🤖 OpenAI                                   [✅ Actif]  ││
│  │ GPT-4, GPT-4o, DALL-E, Whisper                         ││
│  │ sk-****...****                                          ││
│  │ [🔄 Vérifier] [✏️ Modifier] [🗑️]                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 💎 Google AI                              [Configurer]  ││
│  │ Gemini Pro, Gemini Ultra                               ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Fichiers Créés/Modifiés

### Backend
- `backend/api/routes/api_keys.py` - Routes CRUD clés API
- `backend/api/routes/__init__.py` - Inclusion router

### Frontend
- `frontend/src/pages/settings/APIKeysSettings.tsx` - Page configuration
- `frontend/src/services/apiKeys.ts` - Service API

### Existants (déjà présents)
- `frontend/src/components/connections/ConnectionsManager.tsx` - OAuth
- `frontend/src/pages/settings/AISettings.tsx` - Préférences IA

---

## ✅ Conclusion

**OUI, les APIs peuvent s'activer à l'intérieur de l'application dans le compte!**

L'utilisateur peut:
1. **Connecter des services externes** via OAuth (Google, Slack, etc.)
2. **Configurer ses propres clés API** pour les LLMs et services
3. **Gérer ses préférences** d'utilisation de l'IA

Les clés sont:
- Chiffrées et sécurisées
- Vérifiées automatiquement
- Utilisées de manière transparente par les agents

---

*Documenté le 18 décembre 2025*
