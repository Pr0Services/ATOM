# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  [AQUA] + [ADAMAS] PROTOCOL                                                  ║
# ║  SEQUENCE 3-6-9-12 — SCRIPT DE LANCEMENT AT·OM (PowerShell)                  ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  "Créateur nous sommes, créateur nous serons,                                ║
# ║   et que la lumière nous permette de créer consciemment."                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

$ErrorActionPreference = "Stop"

# Couleurs
function Write-Cyan { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Gold { param($msg) Write-Host $msg -ForegroundColor Yellow }
function Write-Green { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Purple { param($msg) Write-Host $msg -ForegroundColor Magenta }

Write-Host ""
Write-Cyan "════════════════════════════════════════════════════════════"
Write-Gold "     ✧ INITIALISATION DU SYSTÈME AT·OM ✧"
Write-Cyan "════════════════════════════════════════════════════════════"
Write-Host ""
Write-Purple "     EirA... ManA... ManU..."
Write-Host ""
Write-Host "     Signal: " -NoNewline; Write-Green "4.44s"
Write-Host "     Fréquence d'ancrage: " -NoNewline; Write-Green "444Hz"
Write-Host "     Séquence sacrée: " -NoNewline; Write-Green "3-6-9-12"
Write-Host "     Cube: " -NoNewline; Write-Green "1728 (12³)"
Write-Host ""

# Vérification du répertoire
if (-not (Test-Path "backend") -or -not (Test-Path "atom/app")) {
    Write-Host "Erreur: Ce script doit etre execute depuis la racine du projet CHE-NU" -ForegroundColor Red
    exit 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. LANCEMENT DU CŒUR (BACKEND)
# ═══════════════════════════════════════════════════════════════════════════════

Write-Cyan "[1/3] Activation du Cœur (Backend)..."

Push-Location backend

# Activation de l'environnement virtuel si présent
$venvActivate = $null
if (Test-Path "venv\Scripts\Activate.ps1") {
    $venvActivate = "venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    $venvActivate = ".venv\Scripts\Activate.ps1"
}

if ($venvActivate) {
    & $venvActivate
    Write-Host "     " -NoNewline; Write-Green "✓"; Write-Host " Environnement virtuel activé"
} else {
    Write-Host "     " -NoNewline; Write-Gold "⚠"; Write-Host " Pas d'environnement virtuel détecté"
}

# Lancement du serveur FastAPI en arrière-plan
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    if ($using:venvActivate) { & $using:venvActivate }
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}
Write-Host "     " -NoNewline; Write-Green "✓"; Write-Host " Backend démarré (Job ID: $($backendJob.Id))"

Pop-Location

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PAUSE DE SYNCHRONISATION (Signal 4.44s)
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Cyan "[2/3] Synchronisation du Signal..."
Write-Host "     Attente de " -NoNewline; Write-Green "4.44s"; Write-Host " pour alignement..."

Start-Sleep -Seconds 4.44

Write-Host "     " -NoNewline; Write-Green "✓"; Write-Host " Signal synchronisé"

# ═══════════════════════════════════════════════════════════════════════════════
# 3. LANCEMENT DES INTERFACES (FRONTEND)
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Cyan "[3/3] Activation des Interfaces (AT-OM Frontend)..."

Push-Location atom/app

# Vérification des dépendances
if (-not (Test-Path "node_modules")) {
    Write-Host "     " -NoNewline; Write-Gold "⚠"; Write-Host " Installation des dépendances npm..."
    npm install
}

Write-Host ""
Write-Cyan "════════════════════════════════════════════════════════════"
Write-Gold "     ✧ AT·OM SYSTÈME ACTIVÉ ✧"
Write-Cyan "════════════════════════════════════════════════════════════"
Write-Host ""
Write-Host "     Backend:  " -NoNewline; Write-Green "http://localhost:8000"
Write-Host "     API Docs: " -NoNewline; Write-Green "http://localhost:8000/docs"
Write-Host "     Frontend: " -NoNewline; Write-Green "http://localhost:5173"
Write-Host ""
Write-Purple "     MU·A·RA·TA — Le chemin du retour"
Write-Host ""

# Gestion de l'arrêt propre
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
    Write-Gold "✧ Arrêt du système AT·OM..."
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
    Write-Green "✓ Backend arrêté"
    Write-Purple "💔 Signal 4.44s interrompu"
}

try {
    # Lancement du serveur de développement frontend
    npm run dev
} finally {
    # Cleanup au cas où
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
    Pop-Location
}
