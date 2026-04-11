FROM python:3.12-slim

WORKDIR /app

# ---- Env ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1
ENV PATH="/root/.local/bin:${PATH}"

# ---- System deps (minimal) ----
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- Install uv ----
RUN curl -Ls https://astral.sh/uv/install.sh | sh

# ---- Copy uv files ----
COPY pyproject.toml uv.lock README.md ./

# ---- Copy /src directory ----
COPY src/ ./src/

# ---- Install ----
RUN uv sync --frozen --no-dev

# ---- Set PATH to venv -----
ENV PATH="/app/.venv/bin:$PATH"

#------ Run ----
ENTRYPOINT ["bda-svc"]