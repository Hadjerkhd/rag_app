FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy everything needed
COPY pyproject.toml uv.lock ./

# Verify files are there
RUN ls -la && cat pyproject.toml

# Install
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app
# Copy rest
COPY . /app/

CMD ["fastapi", "run", "--workers", "1", "app/main.py"]
