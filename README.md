# Overview

Automated Battle Damage Assessment system powered by machine learning.

![Diagram](https://github.com/user-attachments/assets/5dbd6987-7653-4948-8f8a-f326d3ac6df3)

## Development Setup

1. [**Install uv**](https://docs.astral.sh/uv/getting-started/installation/)

2. [**Install Ollama and ensure the local server is running**](https://ollama.com/download)

   If Ollama is not already running on your machine, start it with:
   ```bash
   ollama serve
   ```

   Then pull the models configured in `src/bda_svc/pipeline/config.yaml`, for example:
   ```bash
   ollama pull qwen3-vl:8b-instruct-q8_0
   ```

3. **Clone the repository and install dependencies**

   ```bash
   git clone <repository-url>
   cd bda-svc
   uv sync
   ```

4. **Install pre-commit hooks**

   ```bash
   uv run pre-commit install
   ```

## Usage

1. **For complete usage information**:

   ```bash
   uv run bda-svc -h
   ```

2. **Run the BDA service with the default input folder, an environment variable, or a command-line path**:

   ```bash
   uv run bda-svc

   # or

   BDA_INPUT="/path/to/images" uv run bda-svc

   # or

   uv run bda-svc -i /path/to/image.ext

   # or

   uv run bda-svc -i /path/to/folder
   ```

## Project Structure

```
├── .github/                   # CI/CD workflows
├── bda_eval/                  # Evaluation workspace
├── docker/                    # Container assets and helper scripts
├── src/
│   └── bda_svc/
│       ├── __init__.py
│       ├── app.py             # Main application entrypoint
│       ├── cli.py             # Command-line argument parsing
│       ├── constants.py       # Shared constants
│       ├── export.py          # JSON export utilities
│       ├── inputs.py          # Input path validation/discovery
│       └── pipeline/
│           ├── __init__.py
│           ├── config.yaml    # Model + prompt configuration
│           ├── doctrine.yaml  # Doctrinal definitions
│           ├── interfaces.py  # Abstract interfaces + Ollama backend
│           ├── model.py       # BDAPipeline
│           └── utilities.py   # Pipeline helper functions
├── tests/                     # Test suite
├── pyproject.toml
├── uv.lock
└── README.md
```

## Container Build with Docker

```bash
# arm64 architecture image build command

docker buildx build --platform linux/arm64 -f <DOCKERFILE_PATH> -t <IMAGE_NAME> <BUILD_CONTEXT> --load


# x86 architecture image build command

docker build -f <DOCKERFILE_PATH> -t <IMAGE_NAME> <BUILD_CONTEXT>
```

## Container Pull

```bash
# arm image uses --platform flag

docker pull --platform linux/arm64 ghcr.io/cmu-bda/bda-svc:latest

```

## Local Container Testing

```bash
# ollama model must be installed and running on 127.0.0.1:11434
# ollama model name must match model name in bda-svc config.yaml within container

#Linux command for connection to localhost:11434

docker run --rm --network host -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>


#WSL command for connection to localhost:11434

docker run --rm -e OLLAMA_HOST=http://host.docker.internal:11434 -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>


#Linux command for connection to remote ollama server:11434

docker run --rm -e OLLAMA_HOST=http://<REMOTE_OLLAMA_SERVER_IP>:11434 -v <HOST_INPUT_DIR>:<CONTAINER_INPUT_DIR> -v <HOST_OUTPUT_DIR>:<CONTAINER_OUTPUT_DIR> <IMAGE_NAME> -i <CONTAINER_INPUT_DIR> -o <CONTAINER_OUTPUT_DIR>

```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
