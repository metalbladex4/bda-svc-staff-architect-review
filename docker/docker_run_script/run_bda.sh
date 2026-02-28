#!/bin/bash

# run_bda.sh - Dynamic Mission Runner for BDA Service

# Set the default image if no flag is provided
IMAGE_NAME="bda-svc:latest"

# Usage information
usage() {
  echo "Error: Missing required arguments."
  echo "Usage: $0 -i <input_dir> -o <output_dir> [-m <model_tag>]"
  echo "  -i: Local directory containing images (Required)"
  echo "  -o: Local directory for results (Required)"
  echo "  -m: Docker image tag/model name (Optional, default: bda-svc:latest)"
  exit 1
}

# Parse command-line options
while getopts "i:o:m:h" opt; do
  case $opt in
    i) INPUT_DIR=$(realpath "$OPTARG") ;;
    o) OUTPUT_DIR=$(realpath "$OPTARG") ;;
    m) IMAGE_NAME="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done

# --- STRICT VALIDATION ---
if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    usage
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist."
    exit 1
fi
# -------------------------

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "----------------------------------------------------"
echo "BDA Service: Mission Start"
echo "Target Model:   $IMAGE_NAME"
echo "Input Path:     $INPUT_DIR"
echo "Output Path:    $OUTPUT_DIR"
echo "----------------------------------------------------"

# Run the container
# We keep the internal mappings to /inputs and /bda_output
# as defined in the optimized Dockerfile structure.
docker run --rm --gpus all -it \
  -v "$INPUT_DIR":/inputs \
  -v "$OUTPUT_DIR":/bda_output \
  "$IMAGE_NAME" -i /inputs -o /bda_output

echo "----------------------------------------------------"
echo "Mission Complete."