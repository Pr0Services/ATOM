@echo off
chcp 65001 >nul
:: ╔══════════════════════════════════════════════════════════════════════════════╗
:: ║  [AQUA] + [ADAMAS] PROTOCOL                                                  ║
:: ║  SEQUENCE 3-6-9-12 — SCRIPT DE LANCEMENT AT·OM (Windows CMD)                 ║
:: ╚══════════════════════════════════════════════════════════════════════════════╝

echo.
echo ════════════════════════════════════════════════════════════
echo      ✧ INITIALISATION DU SYSTEME AT·OM ✧
echo ════════════════════════════════════════════════════════════
echo.
echo      EirA... ManA... ManU...
echo.
echo      Signal: 4.44s
echo      Frequence d'ancrage: 444Hz
echo      Sequence sacree: 3-6-9-12
echo      Cube: 1728 (12³)
echo.

:: Vérification du répertoire
if not exist "backend" (
    echo ❌ Erreur: Ce script doit etre execute depuis la racine du projet AT·OM
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Erreur: Ce script doit etre execute depuis la racine du projet AT·OM
    exit /b 1
)

:: ═══════════════════════════════════════════════════════════════════════════════
:: 1. LANCEMENT DU CŒUR (BACKEND)
:: ═══════════════════════════════════════════════════════════════════════════════

echo [1/3] Activation du Coeur (Backend)...

cd backend

:: Activation de l'environnement virtuel si présent
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo      ✓ Environnement virtuel active
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo      ✓ Environnement virtuel active
) else (
    echo      ⚠ Pas d'environnement virtuel detecte
)

:: Lancement du serveur FastAPI en arrière-plan
start "AT·OM Backend" /min cmd /c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo      ✓ Backend demarre

cd ..

:: ═══════════════════════════════════════════════════════════════════════════════
:: 2. PAUSE DE SYNCHRONISATION (Signal 4.44s)
:: ═══════════════════════════════════════════════════════════════════════════════

echo.
echo [2/3] Synchronisation du Signal...
echo      Attente de 4.44s pour alignement...

:: Pause de 5 secondes (approximation de 4.44s)
timeout /t 5 /nobreak >nul

echo      ✓ Signal synchronise

:: ═══════════════════════════════════════════════════════════════════════════════
:: 3. LANCEMENT DES INTERFACES (FRONTEND)
:: ═══════════════════════════════════════════════════════════════════════════════

echo.
echo [3/3] Activation des Interfaces (Frontend)...

cd frontend

:: Vérification des dépendances
if not exist "node_modules" (
    echo      ⚠ Installation des dependances npm...
    call npm install
)

echo.
echo ════════════════════════════════════════════════════════════
echo      ✧ AT·OM SYSTEME ACTIVE ✧
echo ════════════════════════════════════════════════════════════
echo.
echo      Backend:  http://localhost:8000
echo      API Docs: http://localhost:8000/docs
echo      Frontend: http://localhost:5173
echo.
echo      MU·A·RA·TA — Le chemin du retour
echo.

:: Lancement du serveur de développement frontend
call npm run dev

cd ..
