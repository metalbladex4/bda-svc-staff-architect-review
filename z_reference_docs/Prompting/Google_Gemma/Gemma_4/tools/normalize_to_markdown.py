#!/usr/bin/env python3
"""Create markdown mirrors for Gemma 4 source documents.

The mirrors are optimized for prompt-development use: easier search, easier
diffing, and cleaner extraction than raw HTML or notebook JSON, while staying
close to the original source structure.
"""

from __future__ import annotations

import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
NORMALIZED_DIR = BASE_DIR / "normalized_md"
SKIP_PARTS = {"normalized_md", "tools", "__pycache__"}
SOURCE_SUFFIXES = {".html", ".ipynb"}


def collapse_blank_lines(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    blank_run = 0
    for line in lines:
        if line.strip():
            blank_run = 0
            cleaned.append(line)
        else:
            blank_run += 1
            if blank_run <= 1:
                cleaned.append("")
    return "\n".join(cleaned).strip() + "\n"


def clean_markdown_lines(text: str) -> str:
    filtered: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "#":
            continue
        if stripped.startswith("[[["):
            continue
        filtered.append(line)
    return collapse_blank_lines("\n".join(filtered))


def collapse_inline_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def first_match(text: str, *patterns: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return unescape(match.group(1)).strip()
    return None


def choose_html_fragment(path: Path, text: str) -> tuple[str, str]:
    parts = set(path.parts)
    start = 0
    end = len(text)
    note = "Kept the main content region and removed page chrome where possible."

    if {"official_docs", "prompting_behavior"} & parts and "devsite-article-body" in text:
        start = text.find('<h1 class="devsite-page-title"')
        if start == -1:
            start = text.find('<div class="devsite-article-body')
        footer_start = text.find("<footer", start)
        if footer_start != -1:
            end = footer_start
        note = "Trimmed Google DevSite navigation and preserved the main article region."
    elif "model_cards" in parts and ("huggingface.co" in text or "Hugging Face" in text):
        start = text.find('<h1 class="flex flex-wrap items-center')
        if start == -1:
            start = text.find("<main class=")
        footer_start = text.find("<footer", start)
        if footer_start != -1:
            end = footer_start
        note = "Trimmed Hugging Face site chrome and preserved the model page main region."
    elif "context" in parts:
        for marker in ("<article", "<main", '<div class="article'):
            start = text.find(marker)
            if start != -1:
                break
        footer_start = text.find("<footer", start if start != -1 else 0)
        if footer_start != -1:
            end = footer_start
        note = "Trimmed blog-site navigation and preserved the article region."
    else:
        for marker in ("<main", "<article", "<body"):
            start = text.find(marker)
            if start != -1:
                break
        footer_start = text.find("<footer", start if start != -1 else 0)
        if footer_start != -1:
            end = footer_start

    if start == -1:
        start = 0

    return text[start:end], note


class MarkdownHTMLParser(HTMLParser):
    BLOCK_TAGS = {
        "article",
        "aside",
        "blockquote",
        "div",
        "header",
        "main",
        "p",
        "section",
    }
    IGNORE_CONTAINER_TAGS = {
        "button",
        "canvas",
        "form",
        "iframe",
        "noscript",
        "picture",
        "script",
        "select",
        "style",
        "svg",
        "textarea",
    }
    IGNORE_VOID_TAGS = {
        "img",
        "input",
        "label",
        "option",
        "path",
        "source",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.ignore_depth = 0
        self.in_pre = False
        self.inline_code = 0
        self.list_stack: list[str] = []
        self.anchor_stack: list[dict[str, str]] = []

    def emit(self, text: str) -> None:
        self.out.append(text)

    def newline(self, count: int = 1) -> None:
        self.emit("\n" * count)

    def emit_text(self, text: str) -> None:
        if not text:
            return
        if not self.out:
            self.emit(text)
            return

        prev = self.out[-1]
        if prev.endswith((" ", "\n", "(", "[", "`", "#")):
            self.emit(text)
            return
        if text[0] in ".,;:!?)]}/":
            self.emit(text)
            return
        self.emit(" " + text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.IGNORE_VOID_TAGS:
            return
        if tag in self.IGNORE_CONTAINER_TAGS:
            self.ignore_depth += 1
            return
        if self.ignore_depth:
            return

        attrs_dict = dict(attrs)

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.newline(2)
            self.emit("#" * int(tag[1]) + " ")
        elif tag in self.BLOCK_TAGS:
            self.newline(2)
        elif tag == "br":
            self.newline()
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
            self.newline()
        elif tag == "li":
            self.newline()
            indent = "  " * max(len(self.list_stack) - 1, 0)
            bullet = "- " if not self.list_stack or self.list_stack[-1] == "ul" else "1. "
            self.emit(indent + bullet)
        elif tag == "pre":
            self.in_pre = True
            self.newline(2)
            self.emit("```text\n")
        elif tag == "code" and not self.in_pre:
            self.inline_code += 1
            self.emit("`")
        elif tag == "a":
            self.anchor_stack.append({"href": attrs_dict.get("href") or "", "text": ""})
        elif tag == "table":
            self.newline(2)
        elif tag == "tr":
            self.newline()
        elif tag in {"th", "td"}:
            if not self.out or self.out[-1].endswith("\n"):
                self.emit("| ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.IGNORE_VOID_TAGS:
            return
        if tag in self.IGNORE_CONTAINER_TAGS:
            if self.ignore_depth:
                self.ignore_depth -= 1
            return
        if self.ignore_depth:
            return

        if tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self.newline(2)
        elif tag == "pre":
            if self.out and not self.out[-1].endswith("\n"):
                self.emit("\n")
            self.emit("```\n")
            self.in_pre = False
        elif tag == "code" and not self.in_pre:
            if self.inline_code:
                self.inline_code -= 1
            self.emit("`")
        elif tag == "a" and self.anchor_stack:
            link = self.anchor_stack.pop()
            text = collapse_inline_whitespace(link["text"])
            href = link["href"].strip()
            rendered = text
            if href:
                rendered = f"[{text}]({href})" if text else href
            if self.anchor_stack:
                self.anchor_stack[-1]["text"] += rendered
            else:
                self.emit_text(rendered)
        elif tag in {"th", "td"}:
            self.emit(" | ")
        elif tag in self.BLOCK_TAGS or tag in {"table", "tr"}:
            self.newline()

    def handle_data(self, data: str) -> None:
        if self.ignore_depth or not data:
            return

        text = data if self.in_pre else collapse_inline_whitespace(data)
        if not text:
            return

        if self.anchor_stack:
            self.anchor_stack[-1]["text"] += text
        else:
            if self.in_pre:
                self.emit(text)
            else:
                self.emit_text(text)

    def get_markdown(self) -> str:
        return "".join(self.out)


def render_header(
    *,
    title: str,
    raw_relative_path: Path,
    source_url: str | None,
    note: str,
) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Raw source: `{raw_relative_path.as_posix()}`",
    ]
    if source_url:
        lines.append(f"- Source URL: {source_url}")
    lines.append(f"- Normalization note: {note}")
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def normalize_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    fragment, note = choose_html_fragment(path, text)

    title = first_match(
        text,
        r"<title>(.*?)</title>",
        r'<meta property="og:title" content="(.*?)"',
        r'<h1[^>]*>(.*?)</h1>',
    ) or path.stem.replace("_", " ")
    source_url = first_match(
        text,
        r'<link rel="canonical" href="(.*?)"',
        r'<meta property="og:url" content="(.*?)"',
    )

    parser = MarkdownHTMLParser()
    parser.feed(fragment)
    body = clean_markdown_lines(parser.get_markdown())

    return render_header(
        title=title,
        raw_relative_path=path.relative_to(BASE_DIR),
        source_url=source_url,
        note=note,
    ) + body


def first_notebook_title(cells: list[dict]) -> str | None:
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        for line in cell.get("source", []):
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            title = stripped.lstrip("#").strip()
            if not title:
                continue
            if "copyright" in title.lower():
                continue
            if stripped.startswith("# ") or stripped.startswith("## "):
                return title
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        for line in cell.get("source", []):
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            title = stripped.lstrip("#").strip()
            if title and "copyright" not in title.lower():
                return title
    return None


def notebook_source_url(cells: list[dict]) -> str | None:
    text = "\n".join("".join(cell.get("source", [])) for cell in cells[:4])
    urls = re.findall(r"https?://[^\s)>\"]+", text)
    preferred = (
        "ai.google.dev",
        "github.com/google-gemma/cookbook",
        "colab.research.google.com",
        "kaggle.com",
        "console.cloud.google.com",
    )
    for domain in preferred:
        for url in urls:
            if domain in url:
                return url
    return urls[0] if urls else None


def render_notebook_output(output: dict) -> str | None:
    output_type = output.get("output_type")
    if output_type == "stream":
        text = output.get("text", "")
        if isinstance(text, list):
            text = "".join(text)
        return text.strip("\n")
    if output_type in {"display_data", "execute_result"}:
        data = output.get("data", {})
        text = data.get("text/plain")
        if isinstance(text, list):
            text = "".join(text)
        if isinstance(text, str):
            return text.strip("\n")
    if output_type == "error":
        traceback = output.get("traceback", [])
        if traceback:
            return "\n".join(traceback)
        return "\n".join(part for part in [output.get("ename", ""), output.get("evalue", "")] if part)
    return None


def normalize_notebook(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    title = first_notebook_title(cells) or path.stem.replace("_", " ")
    source_url = notebook_source_url(cells)

    language = (
        notebook.get("metadata", {})
        .get("kernelspec", {})
        .get("language", "python")
    )

    chunks: list[str] = [
        render_header(
            title=title,
            raw_relative_path=path.relative_to(BASE_DIR),
            source_url=source_url,
            note="Notebook cells were preserved in order. Markdown and code were kept as-is where possible; only notebook JSON wrappers were removed.",
        )
    ]

    code_index = 0
    other_index = 0
    for cell in cells:
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))
        if not source.strip() and cell_type != "code":
            continue

        if cell_type == "markdown":
            chunks.append(source.strip() + "\n")
        elif cell_type == "code":
            code_index += 1
            chunks.append(f"## Code Cell {code_index}\n\n```{language}\n{source.rstrip()}\n```\n")
            outputs = [render_notebook_output(output) for output in cell.get("outputs", [])]
            outputs = [output for output in outputs if output]
            if outputs:
                chunks.append("**Outputs**\n\n```text\n" + "\n\n".join(outputs).rstrip() + "\n```\n")
        else:
            other_index += 1
            chunks.append(f"## {cell_type.title()} Cell {other_index}\n\n{source.strip()}\n")

    return clean_markdown_lines("\n".join(chunks))


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for path in BASE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(BASE_DIR).parts):
            continue
        if path.suffix.lower() in SOURCE_SUFFIXES:
            files.append(path)
    return sorted(files)


def write_normalized_file(source_path: Path) -> Path:
    rel_path = source_path.relative_to(BASE_DIR)
    dest_path = NORMALIZED_DIR / rel_path.with_suffix(".md")
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if source_path.suffix.lower() == ".html":
        normalized = normalize_html(source_path)
    elif source_path.suffix.lower() == ".ipynb":
        normalized = normalize_notebook(source_path)
    else:
        raise ValueError(f"Unsupported source type: {source_path}")

    dest_path.write_text(normalized, encoding="utf-8")
    return dest_path


def main() -> None:
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    written = [write_normalized_file(path) for path in iter_source_files()]
    print(f"Wrote {len(written)} normalized markdown files into {NORMALIZED_DIR}")


if __name__ == "__main__":
    main()
