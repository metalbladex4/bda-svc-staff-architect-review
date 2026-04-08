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
# ollama model must be installed and running on 127.0.0.1:11434
# ollama model name must match model name in bda-svc config.yaml within container

#Linux command for connection to localhost:11434
docker run --rm --network host -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>


#WSL command for connection to localhost:11434
docker run --rm -e OLLAMA_HOST=http://host.docker.internal:11434 -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>


#Linux command for connection to remote ollama server
docker run --rm -e OLLAMA_HOST=http://<REMOTE_OLLAMA_SERVER_IP>:<PORT_NUM> -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>
```