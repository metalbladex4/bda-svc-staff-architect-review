# bda-svc

`bda-svc` is an automated Battle Damage Assessment (BDA) service for imagery. It uses local Ollama vision-language models to detect targets, assess visible physical damage, and produce structured JSON reports.

![Diagram](https://github.com/user-attachments/assets/5dbd6987-7653-4948-8f8a-f326d3ac6df3)

## Quick Start

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

2. [Install Ollama](https://ollama.com/download) and ensure the local server is running:

   ```bash
   ollama serve
   ```

3. Pull the model configured in [`src/bda_svc/pipeline/config.yaml`](src/bda_svc/pipeline/config.yaml), for example:

   ```bash
   ollama pull qwen3-vl:8b-instruct
   ```

4. Clone the repository and install dependencies:

   ```bash
   git clone <repository-url>
   cd bda-svc
   uv sync
   ```

5. Run the service:

   ```bash
   uv run bda-svc
   ```

## Usage

Show command-line help:

```bash
uv run bda-svc -h
```

Run using the default input folder:

```bash
uv run bda-svc
```

Run on a single image:

```bash
uv run bda-svc -i /path/to/image.ext
```

Run on a folder of images:

```bash
uv run bda-svc -i /path/to/folder
```

If no input path is provided, `bda-svc` defaults to `./bda_input`.

## Output

Reports are written to `bda_output/` as JSON files.

Each report includes:

- `metadata`
- `physical_damage`
- `summary`

At a high level, `physical_damage` contains one entry per assessed target, including:

- `target_type`
- `damage_category`
- `confidence_level`
- `brief_supporting_logic`
- `bounding_box`

## Container

A container image can be built from `docker/Dockerfile` for running `bda-svc` in a containerized environment.

## Documentation

Detailed setup, configuration, and container usage instructions will live in a future `docs/` directory.

For now, see:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`src/bda_svc/pipeline/config.yaml`](src/bda_svc/pipeline/config.yaml)
- [`src/bda_svc/pipeline/doctrine.yaml`](src/bda_svc/pipeline/doctrine.yaml)

## License

This project is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for details.