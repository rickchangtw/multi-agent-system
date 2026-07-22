# Multi-Agent Community Management System - Production Dockerfile
# 多 Agent 系統生產環境 Dockerfile
#
# Build: docker build -t multi-agent-server:latest .
# Run: docker-compose up -d
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    pyyaml \
    requests \
    psycopg2-binary \
    redis \
    flask \
    gunicorn

# Create application user
RUN useradd -m appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code
COPY agents/ /app/agents/
COPY protocols/ /app/protocols/
COPY events/ /app/events/
COPY state/ /app/state/
COPY ai/ /app/ai/
COPY wiki/ /app/wiki/
COPY database/ /app/database/
COPY nginx.conf /app/nginx.conf

# Create backup directory
RUN mkdir -p /app/backup /app/data

# Expose application port
EXPOSE 3021

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:3021/api/health')" || exit 1

# Run application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:3021", "--workers", "4", "--timeout", "120", "server:main"]
