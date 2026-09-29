# Multi-Stage Production Dockerfile for SIH26143 Maritime Forensic Platform

# ==========================================
# Stage 1: Build React + Leaflet Frontend
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /build

COPY app/frontend/package*.json ./
RUN npm ci

COPY app/frontend/ ./
RUN npm run build

# ==========================================
# Stage 2: Python Backend & Unified Runtime
# ==========================================
FROM python:3.12-slim AS runner

# Install system dependencies (curl for healthchecks, libpq for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, data, experiments, and documentation
COPY src/ ./src/
COPY app/ ./app/
COPY data/ ./data/
COPY experiments/ ./experiments/
COPY reports/ ./reports/
COPY docs/ ./docs/

# Copy compiled frontend assets from Stage 1 into app/frontend/dist
COPY --from=frontend-builder /build/dist ./app/frontend/dist

# Set Python environment variables
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV DEMO_MODE=true

EXPOSE 8000

# Health check to ensure API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Launch production server
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
