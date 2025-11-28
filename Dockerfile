FROM python:3.13-slim as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# Use bytocode compilation for faster program startup. Works for large environments
#ENV UV_COMPILE_BYTECODE=1

ENV UV_PROJECT_ENV=/app/.venv

# Use system Python instead of downloading a new one
ENV UV_PYTHON_PREFERENCE=only-system

# Copy from cache instread of symlinking them
ENV UV_LINK_MODE=copy 

# Install executables into this directory, so the tools immediatelly accessible without modifying the PATH(CLI packages). 
ENV UV_TOOL_BIN_DIR=/usr/local/bin

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

RUN chown -R nonroot:nonroot /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

