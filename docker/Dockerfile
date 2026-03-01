# Base python images
FROM python:3.12-slim-trixie


# Copy uv from repo
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working dir
WORKDIR /app

# Copy over only model
COPY ./models/HuggingFaceTB--SmolVLM-256M-Instruct/ /app/models/

# Install dependencies
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1
COPY pyproject.toml uv.lock ./
COPY README.md ./

# 3. Copy over only src dir
COPY src/ ./src/

# Install project
RUN uv sync --frozen --no-dev


# 4. Set PATH to venv
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["bda-svc"]

CMD ["-i", "-h", "o"]