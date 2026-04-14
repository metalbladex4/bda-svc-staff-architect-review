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
│   └── evaluation.csv        # CSV file with evaluation results
│   └── reports_reference/    # Copy of reference report folder
│   └── reports_predicted/    # Copy of predicted report folder
│   └── images/bbox/both/     # Contains images with ref/pred bounding boxes
│   └── logs_llmaaj/          # LLMaaJ score results
│       ├── llmaaj.jsonl      # JSON Lines file (each line is a JSON object)
│       ├── llmaaj.log        # Human-readable JSON format
```