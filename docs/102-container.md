# Containers

This is a placeholder for future documentation.

## Container build

```bash
# arm64 architecture image build command
docker buildx build --platform linux/arm64 -f <DOCKERFILE_PATH> -t <IMAGE_NAME> <BUILD_CONTEXT> --load

# x86 architecture image build command
docker build -f <DOCKERFILE_PATH> -t <IMAGE_NAME> <BUILD_CONTEXT>
```

## Container pull

```bash
# arm image uses --platform flag
docker pull --platform linux/arm64 ghcr.io/cmu-bda/bda-svc:latest
```

## Local container testing

```bash
# An OpenAI-compatible model server must be running and accessible.
# The configured model name must match a model loaded on the server.

# Linux - vLLM or Ollama running on localhost
docker run --rm --network host \
    -e OPENAI_BASE_URL=http://localhost:8000/v1 \
    -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> \
    -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> \
    <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>

# WSL - vLLM or Ollama running on localhost
docker run --rm \
    -e OPENAI_BASE_URL=http://host.docker.internal:8000/v1 \
    -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> \
    -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> \
    <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>

# Remote model server
docker run --rm \
    -e OPENAI_BASE_URL=http://<REMOTE_SERVER_IP>:<PORT>/v1 \
    -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> \
    -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> \
    <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>
```