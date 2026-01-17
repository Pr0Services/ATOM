# 🚀 CHE·NU™ / NOVA-999 Backend

## Déploiement DigitalOcean App Platform

### 📁 Fichiers dans ce dossier

```
backend/
├── main.py           ← API FastAPI + Moteur Résonance
├── requirements.txt  ← Dépendances Python
├── Dockerfile        ← Config Docker (si autodétection échoue)
└── README.md         ← Ce fichier
```

### ⚙️ Configuration DigitalOcean

**Source Directory:** `/backend`

**Run Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`

**HTTP Port:** `8000`

### 🔐 Variables d'Environnement

| KEY | VALUE |
|-----|-------|
| `DATABASE_URL` | `postgresql+asyncpg://[USER]:[PASS]@[HOST]:25060/[DB]?sslmode=require` |
| `CORS_ORIGINS` | `["https://[TON-APP].vercel.app","http://localhost:3000"]` |
| `PORT` | `8000` |

### ✅ Après Déploiement

1. Ajouter l'App dans **Trusted Sources** de PostgreSQL
2. Tester: `curl https://[ton-app].ondigitalocean.app/health`

### 🎵 Séquences d'Activation

- 781901942 → Passé
- 71042 → Présent  
- 14872191 → Futur
- 8888848888819751 → Rétablissement
- 741 → Solution Rapide
