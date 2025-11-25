FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Pre-install dependencies (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/app/.venv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project

# Copy source
COPY . /app/

# Install the project itself (uses cached venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/app/.venv \
    uv sync --frozen

CMD ["fastapi", "run", "--workers", "1", "app/main.py"]
