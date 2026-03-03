FROM python:3.11-slim

WORKDIR /app

# Install curl for HEALTHCHECK
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ src/
COPY scripts/ scripts/

# Create empty model/artifact dirs; they are populated via volume mounts
# in docker-compose.yml (./models and ./artifacts).  This means the image
# builds successfully in CI even when those gitignored directories are absent.
RUN mkdir -p models artifacts

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.api.app:create_app", \
     "--factory", "--host", "0.0.0.0", "--port", "8000"]
