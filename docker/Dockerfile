# 1. Start with the slim base
FROM python:3.12-slim-trixie

# 2. Get uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set workdir
WORKDIR /app

# 4. Copy ONLY dependency files first
COPY pyproject.toml uv.lock ./

# 5. Install dependencies
ENV UV_NO_DEV=1
ENV UV_COMPILE_BYTECODE=1
RUN uv sync --frozen --no-install-project

# 6. Copy the project and models (doing last so we don't break the cache from steps above)
COPY . .

# 7. Final sync to install the project itself
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "bda-svc"]
CMD ["-i", "-h", "o"]