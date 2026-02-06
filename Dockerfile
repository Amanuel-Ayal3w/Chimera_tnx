# Project Chimera development/test image
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install system deps and uv package manager
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Sync dependencies before copying the full source to leverage Docker layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --locked

COPY . .
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "pytest"]
