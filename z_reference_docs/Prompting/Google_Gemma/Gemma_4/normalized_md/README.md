# Gemma 4 Normalized Markdown Layer

This directory mirrors the raw Gemma 4 source bundle in Markdown form so the
documents are easier to search, diff, quote, and reuse during prompt
development.

Design intent:

- Keep the original source files in place for archival fidelity.
- Mirror each `.html` and `.ipynb` file into a `.md` file with the same relative
  path under `normalized_md/`.
- Preserve source ordering and content structure as closely as possible while
  removing site chrome and notebook JSON wrappers.

Normalization rules:

- Google DevSite and Hugging Face HTML snapshots are trimmed to their main
  content regions before conversion.
- Notebook Markdown and code cells are preserved in order.
- Simple textual notebook outputs are retained when available.
- Each normalized file starts with source-path metadata and, when available, the
  source URL.

The normalizer is stored at:

- `tools/normalize_to_markdown.py`

Run it from the Gemma 4 folder root with:

```bash
python3 tools/normalize_to_markdown.py
```
