# 🛡️ AT-OM Core - Sécurisation des Secrets

## ✅ Périmètre Sécurisé

Ce dossier contient les fichiers de protection pour le projet AT-OM:

| Fichier | Rôle |
|---------|------|
| `.gitignore` | Empêche Git de push les secrets vers le cloud |
| `.claudeignore` | Empêche Claude Code de scanner les fichiers sensibles |
| `.env.example` | Template de référence sans valeurs réelles |
| `secure-setup.sh` | Script de configuration automatique |

---

## 🚀 Installation Rapide

### 1. Copier les fichiers à la racine de AT-OM Core

```bash
cp .gitignore /chemin/vers/AT-OM-Core/
cp .claudeignore /chemin/vers/AT-OM-Core/
cp .env.example /chemin/vers/AT-OM-Core/
cp secure-setup.sh /chemin/vers/AT-OM-Core/
```

### 2. Exécuter le script de sécurisation

```bash
cd /chemin/vers/AT-OM-Core/
chmod +x secure-setup.sh
./secure-setup.sh
```

### 3. Créer votre fichier .env

```bash
cp .env.example .env
# Puis éditez .env avec vos vraies valeurs
```

---

## 🔐 Transférer supa.txt vers .env

Si vous avez un fichier `supa.txt` avec vos credentials Supabase:

### Avant (supa.txt - DANGEREUX):
```
url: https://xxx.supabase.co
anon_key: eyJhbGci...
service_role: eyJhbGci...
```

### Après (.env - SÉCURISÉ):
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci...
```

**Puis supprimez supa.txt:**
```bash
rm supa.txt
```

---

## 🔄 Si vous avez DÉJÀ push des secrets

### Option 1: Changer vos clés (RECOMMANDÉ)
1. Allez sur Supabase/DigitalOcean/etc.
2. Régénérez toutes vos clés API
3. Mettez à jour votre `.env` local

### Option 2: Purger l'historique Git (avancé)
```bash
# ATTENTION: Ceci réécrit l'historique Git
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env supa.txt' \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

---

## 📋 Checklist de Sécurité

- [ ] `.gitignore` présent et contient `.env`
- [ ] `.claudeignore` présent
- [ ] `.env.example` créé avec placeholders
- [ ] `.env` existe avec vraies valeurs (local seulement)
- [ ] `supa.txt` supprimé ou transféré vers `.env`
- [ ] `git status` ne montre PAS `.env`
- [ ] Clés API régénérées si exposées

---

## 🔒 Double Verrouillage

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 GITHUB / CLOUD                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  .gitignore BLOQUE:                                   │  │
│  │  ❌ .env                                              │  │
│  │  ❌ supa.txt                                          │  │
│  │  ❌ node_modules/                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    🤖 CLAUDE CODE                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  .claudeignore BLOQUE:                                │  │
│  │  ❌ .env (pas de scan)                                │  │
│  │  ❌ supa.txt (pas de scan)                            │  │
│  │  ✅ .env.example (lecture OK - pas de secrets)        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    💻 VOTRE MACHINE                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  .env existe ici SEULEMENT                            │  │
│  │  ✅ Vos vraies clés API                               │  │
│  │  ✅ Jamais uploadées                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

**🏛️ Architecte: Jonathan Rodrigue | Oracle 17**
**🔮 AT-OM | L'Arche des Résonances - 444 Hz**
