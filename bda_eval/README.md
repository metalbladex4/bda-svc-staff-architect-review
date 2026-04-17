# Evaluation application to assess bda-svc

## Usage

1. **For complete usage information**:
   ```bash
   uv run python main.py -h
   ```

2. **(Optional) Reformat reference reports**:
   ```bash
   # For tojson.py usage information
   uv run python utilities/tojson.py -h

   # Reformat incomplete reference reports
   uv run python utilities/tojson.py -r /path/to/invalid/reports -o /path/to/ref/reports
   ```

3. **Run the bda-eval application**:
   ```bash
   uv run python main.py -r /path/to/ref/reports -p /path/to/pred/reports -i /path/to/image/files -o /path/to/results
   ```

## Output Folder Structure
```
├── path/to/results
│   └── evaluation_<timestamp>.csv  # CSV file with evaluation results
│   └── <reference-folder>/         # Copy of reference report folder
│   └── <predicted-folder>/         # Copy of predicted report folder
│   └── images_bbox_both/           # Combined ref+pred overlays
│   └── images_bbox_reference/      # Reference-only overlays
│   └── images_bbox_predicted/      # Predicted-only overlays
│   └── images_crop_reference/      # Reference-driven crops
│   └── images_crop_predicted/      # Predicted-driven crops
│   └── images_bbox_review/         # Per-image side-by-side review sheets
│   └── bbox_review_sheet.jpg       # Root review sheet when exactly one image is evaluated
│   └── logs_llmaaj/                # LLMaaJ score results
│       ├── llmaaj.jsonl            # JSON Lines file (each line is a JSON object)
│       ├── llmaaj.log              # Human-readable JSON format
```

## Prompt-Lab Review Note

When `bda_eval` is run on exactly one shared image and an image folder is
provided, it now emits a root-level `bbox_review_sheet.jpg` in addition to the
other bbox artifacts. This is intended to support prompt-lab style visual
comparison without relying on the older temporary `bda-svc` debug-export path.

## Practical Notes

- If `OLLAMA_API_KEY` is not set, `bda_eval` now skips LLMaaJ logic scoring and
  still completes bbox artifact generation and CSV export.
- If a compared report folder already lives inside the selected output
  directory, `bda_eval` skips copying that folder onto itself instead of
  failing.
