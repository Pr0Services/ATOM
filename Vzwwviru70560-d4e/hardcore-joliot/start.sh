#!/bin/bash

# CHE·NU™ V82 — Quick Start Script
# ==================================

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║              CHE·NU™ V82 — CALENDRIER VIVANT — PRODUCTION               ║"
echo "║                                                                          ║"
echo "║                    Signal: 4.44s | Fréquence: 444Hz                     ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker detected. Starting with docker-compose..."
    docker-compose up -d
    echo "✅ Services started!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend:  http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "💓 Heartbeat: http://localhost:8000/health"
else
    echo "📦 Docker not found. Starting manually..."

    # Start backend
    echo "🚀 Starting backend..."
    cd backend
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

    # Wait for backend
    echo "⏳ Waiting for backend (4.44s signal sync)..."
    sleep 4.44

    # Start frontend (AT·OM)
    echo "🚀 Starting AT·OM frontend..."
    cd ../atom/app
    npm install
    npm start &

    echo "✅ Services started!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend:  http://localhost:8000"
fi
