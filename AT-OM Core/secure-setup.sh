#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# AT-OM Core - Script de Sécurisation
# 🛡️ Exécutez ce script pour sécuriser votre projet
# ═══════════════════════════════════════════════════════════════════════════════

echo "🛡️ AT-OM Security Setup"
echo "═══════════════════════════════════════════════════════════════"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Retirer .env du tracking Git (si déjà suivi)
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "📁 Étape 1: Retrait des fichiers sensibles du tracking Git..."

if [ -f ".env" ]; then
    git rm -r --cached .env 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ .env retiré du tracking Git${NC}"
    else
        echo -e "${YELLOW}ℹ️ .env n'était pas suivi par Git${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️ Fichier .env non trouvé (normal si pas encore créé)${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Retirer supa.txt du tracking Git
# ═══════════════════════════════════════════════════════════════════════════════
if [ -f "supa.txt" ]; then
    git rm -r --cached supa.txt 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ supa.txt retiré du tracking Git${NC}"
    else
        echo -e "${YELLOW}ℹ️ supa.txt n'était pas suivi par Git${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Transférez le contenu de supa.txt vers .env${NC}"
    echo "   Puis supprimez supa.txt pour plus de sécurité"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Vérifier que .gitignore existe
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "📁 Étape 2: Vérification du .gitignore..."

if [ -f ".gitignore" ]; then
    # Vérifier si .env est dans .gitignore
    if grep -q "^\.env$" .gitignore; then
        echo -e "${GREEN}✅ .gitignore contient .env${NC}"
    else
        echo ".env" >> .gitignore
        echo -e "${GREEN}✅ .env ajouté à .gitignore${NC}"
    fi
    
    # Vérifier si supa.txt est dans .gitignore
    if grep -q "supa.txt" .gitignore; then
        echo -e "${GREEN}✅ .gitignore contient supa.txt${NC}"
    else
        echo "supa.txt" >> .gitignore
        echo -e "${GREEN}✅ supa.txt ajouté à .gitignore${NC}"
    fi
else
    echo -e "${RED}❌ .gitignore non trouvé! Copiez le fichier fourni.${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Vérifier que .claudeignore existe
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "📁 Étape 3: Vérification du .claudeignore..."

if [ -f ".claudeignore" ]; then
    echo -e "${GREEN}✅ .claudeignore existe${NC}"
else
    echo -e "${YELLOW}ℹ️ .claudeignore non trouvé - copiez le fichier fourni${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Vérifier que .env.example existe
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "📁 Étape 4: Vérification du .env.example..."

if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example existe${NC}"
else
    echo -e "${YELLOW}ℹ️ .env.example non trouvé - copiez le fichier fourni${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Résumé
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🛡️ SÉCURISATION TERMINÉE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Prochaines étapes:"
echo "  1. Vérifiez que tous les fichiers sont en place"
echo "  2. Si supa.txt existe, transférez son contenu vers .env"
echo "  3. Commitez les changements:"
echo ""
echo "     git add .gitignore .claudeignore .env.example"
echo "     git commit -m 'security: add secret protection files'"
echo "     git push"
echo ""
echo -e "${GREEN}✅ Périmètre sécurisé!${NC}"
