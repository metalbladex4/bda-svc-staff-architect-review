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

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
