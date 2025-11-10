# Stage 1 — builder environment
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

# Set working directory
WORKDIR /app

# Copy project files for dependency resolution
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv
RUN uv sync --frozen --no-dev

# Copy application code and model
COPY . .

# Stage 2 — runtime environment
FROM python:3.13-slim

WORKDIR /app

# Copy uv-managed virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy application code and model
COPY --from=builder /app/predict.py /app/model.bin /app/

# Ensure uv-managed venv is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
