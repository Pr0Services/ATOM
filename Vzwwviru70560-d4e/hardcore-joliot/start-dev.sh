#!/bin/bash
# CHE·NU V75 - Development Startup Script

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            CHE·NU V75 - DEVELOPMENT MODE                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Set environment for dev mode (mocks enabled)
export USE_MOCK_REDIS=true
export USE_SQLITE=true

# Start Backend
echo ""
echo "🚀 Starting Backend (FastAPI on port 8000)..."
cd "$(dirname "$0")/backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "   Waiting for backend..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "   ✅ Backend ready!"
        break
    fi
    sleep 1
done

# Start Frontend
echo ""
echo "🎨 Starting Frontend (Vite on port 5173)..."
cd "$(dirname "$0")/frontend"
npx vite --port 5173 --host &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

sleep 3

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 CHE·NU V75 READY!                      ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Backend:  http://127.0.0.1:8000                             ║"
echo "║  API Docs: http://127.0.0.1:8000/docs                        ║"
echo "║  Frontend: http://127.0.0.1:5173                             ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Press Ctrl+C to stop all services                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Wait for interrupt
wait
