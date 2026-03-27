# Base python images
FROM nvcr.io/nvidia/l4t-jetpack:r36.4.0


# Set working dir
WORKDIR /app

# Update Linux OS dependencies & install uv
RUN apt-get update && apt-get install -y curl ca-certificates \
 && curl -LsSf https://astral.sh/uv/install.sh | sh


ENV PATH="/root/.local/bin:${PATH}"


# Copy over only model
COPY ./models/ /app/models/


# Set uv environment variables
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1


# Copy over .toml/uv.lock/README.md and src dir
COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY src/ ./src/


# Install project using uv pyproject.toml
RUN uv sync --frozen --no-dev


# Set PATH to venv
ENV PATH="/app/.venv/bin:$PATH"


ENTRYPOINT ["bda-svc"]

CMD ["-i", "-h", "o"]