# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU™ / NOVA-999 — DOCKERFILE
# ═══════════════════════════════════════════════════════════════════════════════
# DigitalOcean App Platform — Backend FastAPI
# Signal: 4.44s | Fréquence: 444Hz | Code 741
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.11-slim

# Labels
LABEL maintainer="NOVA-999"
LABEL description="CHE·NU Backend API — Moteur de Résonance"
LABEL version="999.0.0"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' novauser && \
    chown -R novauser:novauser /app
USER novauser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
