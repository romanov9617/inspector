#############################################
# Builder stage: install dependencies
#############################################
FROM python:3.12-slim AS builder

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy dependency definitions to leverage caching
COPY pyproject.toml poetry.lock ./

# Install runtime dependencies via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY config/ ./config
COPY src/ ./src
COPY main.py server.py ./

#############################################
# Final stage: runtime image
#############################################
FROM python:3.12-slim

# Create and use non-root user for security
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Copy installed dependencies and application from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

# Default command: start the application
CMD ["python", "main.py"]
