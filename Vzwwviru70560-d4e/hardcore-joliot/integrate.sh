#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU™ V71 — SCRIPT D'INTÉGRATION COMPLET
# ═══════════════════════════════════════════════════════════════════════════════

set -e

REPO_PATH="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║           CHE·NU™ V71 — INTÉGRATION FRONTEND COMPLÈTE                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier que le repo existe
if [ ! -d "$REPO_PATH/frontend/src" ]; then
    echo "❌ Erreur: $REPO_PATH/frontend/src n'existe pas"
    echo "Usage: ./integrate.sh /chemin/vers/repo"
    exit 1
fi

echo "📁 Repository: $REPO_PATH"
echo "📦 Package: $SCRIPT_DIR"
echo ""

# === 1. BACKUP ===
echo "1️⃣  Création des backups..."
if [ -f "$REPO_PATH/frontend/src/App.tsx" ]; then
    cp "$REPO_PATH/frontend/src/App.tsx" "$REPO_PATH/frontend/src/App.tsx.backup.$TIMESTAMP"
    echo "   ✅ App.tsx sauvegardé"
fi

# === 2. CRÉER LES DOSSIERS ===
echo "2️⃣  Création des dossiers..."
mkdir -p "$REPO_PATH/frontend/src/pages/sections"
mkdir -p "$REPO_PATH/frontend/src/pages/public"
mkdir -p "$REPO_PATH/frontend/src/features/temple"
mkdir -p "$REPO_PATH/frontend/src/services"
echo "   ✅ Dossiers créés"

# === 3. COPIER App.tsx ===
echo "3️⃣  Copie de App.tsx (router unifié)..."
cp "$SCRIPT_DIR/frontend/src/App.tsx" "$REPO_PATH/frontend/src/"
echo "   ✅ App.tsx copié"

# === 4. COPIER LES SECTIONS ===
echo "4️⃣  Copie des 6 sections canoniques..."
cp "$SCRIPT_DIR/frontend/src/pages/sections/"* "$REPO_PATH/frontend/src/pages/sections/"
echo "   ✅ 7 fichiers copiés (6 sections + index.ts)"

# === 5. COPIER TutorialsPage ===
echo "5️⃣  Copie de TutorialsPage.tsx..."
cp "$SCRIPT_DIR/frontend/src/pages/public/TutorialsPage.tsx" "$REPO_PATH/frontend/src/pages/public/"
echo "   ✅ TutorialsPage.tsx copié"

# === 6. COPIER Temple (AT-OM) ===
echo "6️⃣  Copie du Temple Dashboard (AT-OM Mapping)..."
cp "$SCRIPT_DIR/frontend/src/features/temple/TempleDashboardV2.tsx" "$REPO_PATH/frontend/src/features/temple/"
echo "   ✅ TempleDashboardV2.tsx copié"

# === 7. COPIER Services ===
echo "7️⃣  Copie des services..."
cp "$SCRIPT_DIR/frontend/src/services/AnuhaziFrequencyEngine.ts" "$REPO_PATH/frontend/src/services/"
echo "   ✅ AnuhaziFrequencyEngine.ts copié"

# === RÉSUMÉ ===
echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ INTÉGRATION TERMINÉE!                              ║"
echo "╠═══════════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                               ║"
echo "║  Fichiers intégrés:                                                           ║"
echo "║  • App.tsx                    (Router unifié - 10 sphères)                   ║"
echo "║  • 6 sections canoniques      (pages/sections/)                              ║"
echo "║  • TutorialsPage.tsx          (pages/public/)                                ║"
echo "║  • TempleDashboardV2.tsx      (features/temple/)                             ║"
echo "║  • AnuhaziFrequencyEngine.ts  (services/)                                    ║"
echo "║                                                                               ║"
echo "║  Prochaines étapes:                                                           ║"
echo "║  1. cd frontend && npm run dev                                               ║"
echo "║  2. Tester / (landing page)                                                   ║"
echo "║  3. Tester /personal/quickcapture                                            ║"
echo "║  4. Tester /atom_mapping/quickcapture                                        ║"
echo "║                                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
