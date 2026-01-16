@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
::  [AQUA] + [ADAMAS] PROTOCOL
::  SEQUENCE 3-6-9-12 - SCRIPT DE LANCEMENT AT.OM (Windows CMD)
::  Version: 2.1 ROBUSTE (ASCII Pure)
:: ============================================================================

:: Configuration
set BACKEND_PORT=8000
set FRONTEND_PORT=3000
set LOG_FILE=debug_logs.txt

:: Se placer dans le repertoire du script
cd /d "%~dp0"

:: Initialiser le fichier de logs
echo. > "%LOG_FILE%"
echo [%date% %time%] === AT.OM SYSTEM STARTUP === >> "%LOG_FILE%"

echo.
echo ============================================================================
echo.
echo     AAAA   TTTTT    OOO   M   M
echo    A    A    T     O   O  MM MM
echo    AAAAAA    T     O   O  M M M
echo    A    A    T     O   O  M   M
echo    A    A    T      OOO   M   M
echo.
echo ============================================================================
echo.
echo                 INITIALISATION DU SYSTEME AT.OM
echo.
echo                 EirA... ManA... ManU...
echo.
echo                 Signal: 4.44s
echo                 Frequence ancrage: 444Hz
echo                 Sequence sacree: 3-6-9-12
echo                 Cube: 1728 (12^3)
echo.
echo ============================================================================
echo.

:: ============================================================================
:: VERIFICATION DU REPERTOIRE DE TRAVAIL
:: ============================================================================

echo [CHECK] Repertoire de travail: %CD%
echo [%date% %time%] Working directory: %CD% >> "%LOG_FILE%"

if not exist "backend" (
    echo [ERREUR] Le dossier backend n existe pas!
    echo [%date% %time%] ERROR: backend folder not found >> "%LOG_FILE%"
    echo          Assurez-vous d executer ce script depuis la racine du projet AT.OM
    pause
    exit /b 1
)

if not exist "frontend" (
    echo [ERREUR] Le dossier frontend n existe pas!
    echo [%date% %time%] ERROR: frontend folder not found >> "%LOG_FILE%"
    echo          Assurez-vous d executer ce script depuis la racine du projet AT.OM
    pause
    exit /b 1
)

echo [OK] Structure du projet verifiee
echo.

:: ============================================================================
:: DETECTION DE PYTHON
:: ============================================================================

echo [1/5] Detection de Python...

set PYTHON_CMD=

:: Essayer py d abord (Windows Python Launcher)
py --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set PYTHON_CMD=py
    for /f "tokens=*" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo       [OK] Python trouve: !PYTHON_VERSION! via py
    goto python_found
)

:: Essayer python
python --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set PYTHON_CMD=python
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo       [OK] Python trouve: !PYTHON_VERSION! via python
    goto python_found
)

:: Essayer python3
python3 --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set PYTHON_CMD=python3
    for /f "tokens=*" %%i in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo       [OK] Python trouve: !PYTHON_VERSION! via python3
    goto python_found
)

echo [ERREUR] Python n est pas installe ou non accessible dans le PATH!
echo [%date% %time%] ERROR: Python not found >> "%LOG_FILE%"
echo          Installez Python depuis https://www.python.org/downloads/
pause
exit /b 1

:python_found
echo [%date% %time%] Python found: !PYTHON_CMD! - !PYTHON_VERSION! >> "%LOG_FILE%"

:: ============================================================================
:: DETECTION DE NODE.JS
:: ============================================================================

echo.
echo [2/5] Detection de Node.js...

node --version >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [ERREUR] Node.js n est pas installe!
    echo [%date% %time%] ERROR: Node.js not found >> "%LOG_FILE%"
    echo          Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo       [OK] Node.js trouve: %NODE_VERSION%
echo [%date% %time%] Node.js found: %NODE_VERSION% >> "%LOG_FILE%"

:: ============================================================================
:: PREPARATION DU BACKEND
:: ============================================================================

echo.
echo [3/5] Preparation du Backend - Coeur...

cd backend

:: Activation de l environnement virtuel si present
if exist "venv\Scripts\activate.bat" (
    echo       [OK] Environnement virtuel detecte venv
    call venv\Scripts\activate.bat
    echo [%date% %time%] Virtual environment activated: venv >> "..\%LOG_FILE%"
) else if exist ".venv\Scripts\activate.bat" (
    echo       [OK] Environnement virtuel detecte .venv
    call .venv\Scripts\activate.bat
    echo [%date% %time%] Virtual environment activated: .venv >> "..\%LOG_FILE%"
) else (
    echo       [INFO] Pas d environnement virtuel - utilisation du Python global
    echo [%date% %time%] No virtual environment found, using global Python >> "..\%LOG_FILE%"
)

:: Verification d uvicorn
!PYTHON_CMD! -c "import uvicorn" >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo       [WARN] uvicorn non installe - installation en cours...
    echo [%date% %time%] Installing uvicorn... >> "..\%LOG_FILE%"
    !PYTHON_CMD! -m pip install uvicorn[standard] fastapi >> "..\%LOG_FILE%" 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [ERREUR] Impossible d installer uvicorn!
        echo [%date% %time%] ERROR: Failed to install uvicorn >> "..\%LOG_FILE%"
        cd ..
        pause
        exit /b 1
    )
)

echo       [OK] Backend pret
cd ..

:: ============================================================================
:: PREPARATION DU FRONTEND
:: ============================================================================

echo.
echo [4/5] Preparation du Frontend - Interfaces...

cd frontend

if not exist "node_modules" (
    echo       [INFO] Installation des dependances npm...
    echo [%date% %time%] Installing npm dependencies... >> "..\%LOG_FILE%"
    call npm install >> "..\%LOG_FILE%" 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [ERREUR] Echec de npm install!
        echo [%date% %time%] ERROR: npm install failed >> "..\%LOG_FILE%"
        cd ..
        pause
        exit /b 1
    )
)

echo       [OK] Frontend pret
cd ..

:: ============================================================================
:: LANCEMENT DES SERVEURS
:: ============================================================================

echo.
echo [5/5] Lancement des serveurs...
echo.
echo [%date% %time%] Starting servers... >> "%LOG_FILE%"

:: Lancement du Backend en arriere-plan avec logs
echo       Demarrage du Backend port %BACKEND_PORT%...
start "AT.OM Backend COEUR" /min cmd /c "cd /d "%~dp0backend" && !PYTHON_CMD! -m uvicorn app.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload"

echo [%date% %time%] Backend started on port %BACKEND_PORT% >> "%LOG_FILE%"

:: Pause de synchronisation 4.44s arrondi a 5s
echo.
echo       Synchronisation du Signal 4.44s...
timeout /t 5 /nobreak >nul

:: Lancement du Frontend
echo       Demarrage du Frontend port %FRONTEND_PORT%...
start "AT.OM Frontend INTERFACES" /min cmd /c "cd /d "%~dp0frontend" && npm run dev"

echo [%date% %time%] Frontend started on port %FRONTEND_PORT% >> "%LOG_FILE%"

:: ============================================================================
:: AFFICHAGE FINAL
:: ============================================================================

timeout /t 3 /nobreak >nul

echo.
echo ============================================================================
echo.
echo                 AT.OM SYSTEME ACTIVE
echo.
echo ============================================================================
echo.
echo     BACKEND Coeur:
echo       - API:       http://localhost:%BACKEND_PORT%
echo       - Docs:      http://localhost:%BACKEND_PORT%/docs
echo       - Health:    http://localhost:%BACKEND_PORT%/health
echo       - Heartbeat: http://localhost:%BACKEND_PORT%/heartbeat
echo.
echo     FRONTEND Interfaces:
echo       - Mirror:    http://localhost:%FRONTEND_PORT%
echo       - Core:      http://localhost:%FRONTEND_PORT%/core
echo       - Temple:    http://localhost:%FRONTEND_PORT%/temple
echo.
echo     FICHIERS CRITIQUES:
echo       - resonance_data.json: frontend/src/data/
echo       - heartbeat.py:        backend/core/
echo       - Logs:                %LOG_FILE%
echo.
echo ============================================================================
echo.
echo                 MU.A.RA.TA - Le chemin du retour
echo.
echo     [AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12
echo.
echo ============================================================================
echo.
echo [%date% %time%] === AT.OM SYSTEM READY === >> "%LOG_FILE%"

echo Appuyez sur une touche pour ouvrir le navigateur...
pause >nul

:: Ouvrir le navigateur sur le frontend
start "" "http://localhost:%FRONTEND_PORT%"

echo.
echo Pour arreter les serveurs, fermez les fenetres AT.OM Backend et AT.OM Frontend
echo ou utilisez le Gestionnaire des taches Ctrl+Shift+Esc
echo.

pause
