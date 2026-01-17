# =============================================================================
# AT·OM API - DOCKERFILE
# Canon AT·OM - Le Moteur (The Engine)
# Optimized for 350 WebSocket Connections (L'Essaim)
# =============================================================================

FROM python:3.11-slim

# Labels
LABEL maintainer="AT·OM System"
LABEL description="AT·OM API Server - Sovereign Identity Platform"
LABEL version="1.0.0"

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

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' atomuser && \
    chown -R atomuser:atomuser /app

USER atomuser

# Expose port
EXPOSE 8000

# Health check (Canon AT·OM endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with uvicorn - 4 workers for API load
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
