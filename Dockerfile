# ===========================================
# AT·OM Sync Engine + Agent System
# Production Dockerfile
# ===========================================
# Optimized Node.js container for:
# - Hedera-Supabase bridge
# - 400+ Agent orchestration system
# - Sacred frequency calculations
# Runs on DigitalOcean App Platform
# ===========================================

# Stage 1: Build
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY services/hedera/package*.json ./services/hedera/
COPY services/database/package*.json ./services/database/

# Install ALL dependencies (including dev for build)
RUN npm ci --only=production

# Copy source code
COPY . .

# ===========================================
# Stage 2: Production
# ===========================================
FROM node:20-alpine AS production

# Add labels for identification
LABEL org.opencontainers.image.title="AT·OM Sync Engine + Agents"
LABEL org.opencontainers.image.description="Hedera-Supabase sync with 400+ agent orchestration"
LABEL org.opencontainers.image.version="2.0.0"

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ONLY production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built application from builder stage
COPY --from=builder /app/services ./services
COPY --from=builder /app/agents ./agents

# Copy .env.template as reference (actual .env should be mounted or use env vars)
COPY .env.template ./.env.template

# Set ownership to non-root user
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose the API port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Set environment variables for production
ENV NODE_ENV=production
ENV PORT=3000

# Sacred frequency constants
ENV ATOM_M=44.4
ENV ATOM_P=161.8
ENV ATOM_I=369
ENV ATOM_PO=1728

# Memory settings for agent workload (400+ concurrent agents)
ENV NODE_OPTIONS="--max-old-space-size=512"

# Start the sync engine with health server
CMD ["node", "services/hedera/sync-engine.js", "--server"]
