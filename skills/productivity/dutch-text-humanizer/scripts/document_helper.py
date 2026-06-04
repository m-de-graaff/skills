#!/usr/bin/env python3
"""Extract, map, audit, and paragraph-replace document text.

The DOCX paths use only Python's standard library so the helper stays usable in
minimal agent environments. PDF support is opportunistic: it uses whichever
common extraction library is already installed.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

try:
    from lxml import etree as LET  # type: ignore
except ImportError:  # pragma: no cover - validated at runtime for DOCX writes.
    LET = None


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W_NS = NS["w"]
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
WORD_PARTS = [
    "word/document.xml",
    "word/footnotes.xml",
    "word/endnotes.xml",
]

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass


@dataclass
class Paragraph:
    id: str
    part: str
    index: int
    text: str


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def text(self) -> str:
        raw = " ".join(self.parts)
        raw = html.unescape(raw)
        raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
        raw = re.sub(r"\n\s+", "\n", raw)
        return raw.strip()


def qn(local_name: str) -> str:
    return f"{{{W_NS}}}{local_name}"


def require_lxml() -> Any:
    if LET is None:
        raise RuntimeError("DOCX replacement requires lxml to preserve Word XML namespaces.")
    return LET


def iter_docx_parts(path: Path) -> Iterable[tuple[str, ET.Element]]:
    with zipfile.ZipFile(path) as zf:
        for part in WORD_PARTS:
            try:
                yield part, ET.fromstring(zf.read(part))
            except KeyError:
                continue


def paragraph_text(paragraph: ET.Element) -> str:
    chunks: list[str] = []
    for node in paragraph.iter():
        if node.tag == qn("t"):
            chunks.append(node.text or "")
        elif node.tag == qn("tab"):
            chunks.append("\t")
        elif node.tag == qn("br"):
            chunks.append("\n")
    return "".join(chunks)


def paragraph_prefix(part: str) -> str:
    if part == "word/document.xml":
        return "body"
    return Path(part).stem


def docx_paragraphs(path: Path) -> list[Paragraph]:
    paragraphs: list[Paragraph] = []
    counters: dict[str, int] = {}
    for part, root in iter_docx_parts(path):
        prefix = paragraph_prefix(part)
        counters.setdefault(prefix, 0)
        for paragraph in root.findall(".//w:p", NS):
            text = paragraph_text(paragraph)
            para_id = f"{prefix}:p{counters[prefix]:06d}"
            counters[prefix] += 1
            paragraphs.append(Paragraph(para_id, part, counters[prefix] - 1, text))
    return paragraphs


def extract_docx(path: Path) -> list[dict[str, Any]]:
    return [
        {"id": p.id, "part": p.part, "index": p.index, "text": p.text}
        for p in docx_paragraphs(path)
        if p.text.strip()
    ]


def extract_pdf(path: Path) -> str:
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except ImportError:
        pass

    try:
        import PyPDF2  # type: ignore

        reader = PyPDF2.PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except ImportError:
        pass

    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(str(path)) as pdf:
            return "\n\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except ImportError:
        pass

    try:
        import fitz  # type: ignore

        doc = fitz.open(str(path))
        return "\n\n".join(page.get_text("text") for page in doc).strip()
    except ImportError:
        pass

    raise RuntimeError(
        "PDF extraction requires one installed backend: pypdf, PyPDF2, pdfplumber, or PyMuPDF."
    )


def extract_textlike(path: Path) -> str:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        parser = TextHTMLParser()
        parser.feed(raw)
        return parser.text()
    return raw


def extract_any(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        text = extract_pdf(path)
        return [{"id": "pdf:p000000", "part": str(path), "index": 0, "text": text}]
    if suffix in {".txt", ".md", ".markdown", ".html", ".htm"}:
        return [{"id": "text:p000000", "part": str(path), "index": 0, "text": extract_textlike(path)}]
    raise RuntimeError(f"Unsupported input type: {path.suffix}")


def write_extraction(items: list[dict[str, Any]], output_format: str) -> None:
    if output_format == "json":
        json.dump({"paragraphs": items}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return
    for item in items:
        text = item["text"].strip()
        if text:
            print(f"[{item['id']}] {text}")


def set_paragraph_text(paragraph: ET.Element, text: str) -> None:
    etree = require_lxml()

    def write_text_nodes(run: ET.Element, value: str) -> None:
        parts = value.split("\n")
        for index, part in enumerate(parts):
            if index:
                etree.SubElement(run, qn("br"))
            t_node = etree.SubElement(run, qn("t"))
            t_node.text = part
            if part.startswith(" ") or part.endswith(" "):
                t_node.set(XML_SPACE, "preserve")

    runs = paragraph.findall("w:r", NS)
    if not runs:
        run = etree.SubElement(paragraph, qn("r"))
        write_text_nodes(run, text)
        return

    first_run = runs[0]
    for run in runs:
        for child in list(run):
            if child.tag in {qn("t"), qn("tab"), qn("br")}:
                run.remove(child)

    write_text_nodes(first_run, text)


def load_replacements(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("paragraphs")
    if not isinstance(rows, list):
        raise RuntimeError("Replacement JSON must contain a 'paragraphs' array.")

    replacements: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or "id" not in row or "text" not in row:
            raise RuntimeError("Each replacement row must contain 'id' and 'text'.")
        replacements[str(row["id"])] = str(row["text"])
    return replacements


def xml_standalone(raw: bytes) -> bool | None:
    prefix = raw[:200].lower()
    if b"standalone" not in prefix:
        return None
    if b"standalone='yes'" in prefix or b'standalone="yes"' in prefix:
        return True
    if b"standalone='no'" in prefix or b'standalone="no"' in prefix:
        return False
    return None


def parse_word_xml(raw: bytes) -> Any:
    etree = require_lxml()
    parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False, huge_tree=True)
    return etree.fromstring(raw, parser)


def serialize_word_xml(root: Any, original_raw: bytes) -> bytes:
    etree = require_lxml()
    kwargs: dict[str, Any] = {
        "encoding": "UTF-8",
        "xml_declaration": True,
        "pretty_print": False,
    }
    standalone = xml_standalone(original_raw)
    if standalone is not None:
        kwargs["standalone"] = standalone
    return etree.tostring(root, **kwargs)


def replace_docx(source: Path, replacements_path: Path, output: Path) -> int:
    replacements = load_replacements(replacements_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    modified_parts: dict[str, bytes] = {}
    with zipfile.ZipFile(source) as zf:
        replaced = 0
        applied_ids: set[str] = set()
        for part in WORD_PARTS:
            try:
                original_raw = zf.read(part)
            except KeyError:
                continue
            doc_root = parse_word_xml(original_raw)
            prefix = paragraph_prefix(part)
            part_replaced = 0
            for index, paragraph in enumerate(doc_root.findall(".//w:p", NS)):
                para_id = f"{prefix}:p{index:06d}"
                if para_id in replacements:
                    set_paragraph_text(paragraph, replacements[para_id])
                    replaced += 1
                    part_replaced += 1
                    applied_ids.add(para_id)
            if part_replaced:
                modified_parts[part] = serialize_word_xml(doc_root, original_raw)

        missing_ids = sorted(set(replacements) - applied_ids)
        if missing_ids:
            preview = ", ".join(missing_ids[:10])
            suffix = "..." if len(missing_ids) > 10 else ""
            raise RuntimeError(f"Replacement IDs not found in source DOCX: {preview}{suffix}")

        tmp_fd, tmp_name = tempfile.mkstemp(
            prefix=f"{output.stem}.", suffix=".tmp.docx", dir=str(output.parent)
        )
        os.close(tmp_fd)
        tmp_path = Path(tmp_name)
        try:
            with zipfile.ZipFile(tmp_path, "w") as out_zf:
                for info in zf.infolist():
                    data = modified_parts.get(info.filename)
                    if data is None:
                        data = zf.read(info.filename)
                    out_zf.writestr(info, data)
            validate_docx_package(tmp_path, source=source, fail_on_text=False)
            os.replace(tmp_path, output)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
    return replaced


def docx_entry_names(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        return zf.namelist()


def validate_docx_package(path: Path, source: Path | None = None, fail_on_text: bool = True) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels"}

    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            if bad:
                failures.append(f"ZIP CRC failure at {bad}")
            names = zf.namelist()
            missing = sorted(required - set(names))
            if missing:
                failures.append(f"Missing required DOCX parts: {', '.join(missing)}")
            for part in WORD_PARTS:
                if part in names:
                    raw = zf.read(part)
                    try:
                        parse_word_xml(raw)
                    except Exception as exc:  # noqa: BLE001
                        failures.append(f"{part} does not parse as XML: {exc}")
            document_xml = zf.read("word/document.xml")
            if b"<ns0:document" in document_xml[:500] or b"ns0:" in document_xml[:500]:
                failures.append("word/document.xml uses generic ns0 prefixes; Word may treat this as repairable content.")
            if b"<w:document" not in document_xml[:500]:
                warnings.append("word/document.xml does not start with a w:document prefix.")
    except zipfile.BadZipFile as exc:
        failures.append(f"Not a valid ZIP/DOCX package: {exc}")

    if source is not None:
        try:
            source_names = docx_entry_names(source)
            target_names = docx_entry_names(path)
            if set(source_names) != set(target_names):
                failures.append("DOCX package entries differ from source.")
            if source_names != target_names:
                warnings.append("DOCX package entry order differs from source.")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"Could not compare package entries with source: {exc}")

    try:
        import docx  # type: ignore

        docx.Document(str(path))
    except ImportError:
        warnings.append("python-docx is not installed; skipped python-docx open check.")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"python-docx could not open document: {exc}")

    if fail_on_text:
        try:
            items = extract_any(path)
            findings = audit_text("\n\n".join(item["text"] for item in items))
            if findings:
                failures.extend(f"text audit: {finding}" for finding in findings)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"Could not run text audit: {exc}")

    return failures, warnings


def audit_text(text: str) -> list[str]:
    checks: list[tuple[str, str]] = [
        ("em dash", "—"),
        ("en dash", "–"),
        ("curly double quote", r"[“”]"),
        ("curly single quote", r"[‘’]"),
        ("emoji/symbol bullet", r"[\U0001F300-\U0001FAFF]"),
        ("bold inline header", r"\*\*[^*\n]{1,60}:\*\*"),
        ("chatbot residue", r"\b(natuurlijk|zeker|ik hoop dat dit helpt|laat het me weten|laten we|hier is een overzicht)\b"),
        ("inflated Dutch significance", r"\b(cruciaal|essentieel|pivotaal|sleutelrol|onderstreept|toonaangevend|baanbrekend|naadloos|robuust|dynamisch)\b"),
        ("vague authority", r"\b(experts stellen|onderzoek toont aan|diverse bronnen|marktpartijen zien|men verwacht)\b"),
        ("English AI vocabulary", r"\b(delven|delve|showcase|landscape|tapestry|testament|pivotal|crucial|unlocking potential)\b"),
        ("fake contrast", r"\b(niet alleen|meer dan alleen|not only|not just)\b"),
    ]
    findings: list[str] = []
    for label, pattern in checks:
        if label in {"em dash", "en dash"}:
            count = text.count(pattern)
        else:
            count = len(re.findall(pattern, text, flags=re.IGNORECASE))
        if count:
            findings.append(f"{label}: {count}")
    return findings


def command_extract(args: argparse.Namespace) -> None:
    items = extract_any(Path(args.input))
    write_extraction(items, args.format)


def command_map_docx(args: argparse.Namespace) -> None:
    path = Path(args.input)
    items = [
        {"id": p.id, "part": p.part, "index": p.index, "text": p.text}
        for p in docx_paragraphs(path)
    ]
    payload = {"paragraphs": items}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(items)} paragraphs to {out}")


def command_replace_docx(args: argparse.Namespace) -> None:
    count = replace_docx(Path(args.source), Path(args.replacements), Path(args.output))
    print(f"Replaced {count} paragraphs in {args.output}")


def command_audit(args: argparse.Namespace) -> None:
    items = extract_any(Path(args.input))
    text = "\n\n".join(item["text"] for item in items)
    findings = audit_text(text)
    if findings:
        print("Findings:")
        for finding in findings:
            print(f"- {finding}")
        sys.exit(1)
    print("No configured AI-writing tells found.")


def command_audit_docx(args: argparse.Namespace) -> None:
    failures, warnings = validate_docx_package(
        Path(args.input), source=Path(args.source) if args.source else None
    )
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("DOCX package audit passed.")


def command_diff_docx(args: argparse.Namespace) -> None:
    before = {item["id"]: item for item in extract_docx(Path(args.source))}
    after = {item["id"]: item for item in extract_docx(Path(args.target))}
    all_ids = sorted(set(before) | set(after))
    changes: list[dict[str, Any]] = []
    for para_id in all_ids:
        old = before.get(para_id, {}).get("text")
        new = after.get(para_id, {}).get("text")
        if old != new:
            changes.append({"id": para_id, "before": old, "after": new})

    if args.format == "json":
        payload = {"changed_count": len(changes), "changes": changes}
        if args.out:
            Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        return

    print(f"Changed paragraphs: {len(changes)}")
    for change in changes:
        print(f"[{change['id']}]")
        print(f"- {change['before']}")
        print(f"+ {change['after']}")


def command_visualize_docx(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    out_dir = Path(args.output_dir)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    winword = shutil.which("WINWORD")

    try:
        import pdf2image  # noqa: F401

        pdf2image_available = True
    except ImportError:
        pdf2image_available = False

    report = {
        "input": str(input_path),
        "output_dir": str(out_dir),
        "soffice": soffice,
        "winword": winword,
        "pdf2image": pdf2image_available,
        "status": "unavailable",
        "message": "",
    }

    if not soffice:
        report["message"] = "No LibreOffice/soffice executable found; DOCX visual rendering is unavailable."
    elif not pdf2image_available:
        report["message"] = "pdf2image is not installed; PDF-to-PNG rasterization is unavailable."
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_dir = out_dir / "pdf"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            soffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(pdf_dir),
            str(input_path),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
        if proc.returncode != 0:
            report["message"] = f"LibreOffice conversion failed: {proc.stderr.strip() or proc.stdout.strip()}"
        else:
            from pdf2image import convert_from_path  # type: ignore

            pdf_candidates = sorted(pdf_dir.glob("*.pdf"))
            if not pdf_candidates:
                report["message"] = "LibreOffice completed but did not produce a PDF."
            else:
                pages = convert_from_path(str(pdf_candidates[0]), dpi=args.dpi)
                png_dir = out_dir / "png"
                png_dir.mkdir(parents=True, exist_ok=True)
                for index, page in enumerate(pages, start=1):
                    page.save(png_dir / f"page-{index:03d}.png")
                report["status"] = "completed"
                report["message"] = f"Rendered {len(pages)} pages."
                report["png_dir"] = str(png_dir)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {report['status']}")
        print(report["message"])
        if report.get("png_dir"):
            print(f"PNG output: {report['png_dir']}")
    if report["status"] != "completed":
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Extract text from DOCX, PDF, text, Markdown, or HTML.")
    extract_parser.add_argument("input")
    extract_parser.add_argument("--format", choices=["text", "json"], default="text")
    extract_parser.set_defaults(func=command_extract)

    map_parser = subparsers.add_parser("map-docx", help="Write DOCX paragraph IDs and text to JSON.")
    map_parser.add_argument("input")
    map_parser.add_argument("--out", required=True)
    map_parser.set_defaults(func=command_map_docx)

    replace_parser = subparsers.add_parser("replace-docx", help="Clone a DOCX and replace paragraphs by ID.")
    replace_parser.add_argument("source")
    replace_parser.add_argument("replacements")
    replace_parser.add_argument("output")
    replace_parser.set_defaults(func=command_replace_docx)

    audit_parser = subparsers.add_parser("audit", help="Scan extracted text for configured AI-writing tells.")
    audit_parser.add_argument("input")
    audit_parser.set_defaults(func=command_audit)

    audit_docx_parser = subparsers.add_parser(
        "audit-docx", help="Validate DOCX package health and run the text audit."
    )
    audit_docx_parser.add_argument("input")
    audit_docx_parser.add_argument("--source", help="Optional source DOCX for package entry comparison.")
    audit_docx_parser.set_defaults(func=command_audit_docx)

    diff_docx_parser = subparsers.add_parser("diff-docx", help="Compare non-empty DOCX paragraphs by ID.")
    diff_docx_parser.add_argument("source")
    diff_docx_parser.add_argument("target")
    diff_docx_parser.add_argument("--format", choices=["text", "json"], default="text")
    diff_docx_parser.add_argument("--out", help="Write JSON diff to this path.")
    diff_docx_parser.set_defaults(func=command_diff_docx)

    visualize_parser = subparsers.add_parser(
        "visualize-docx", help="Render DOCX to page PNGs when local render backends are available."
    )
    visualize_parser.add_argument("input")
    visualize_parser.add_argument("--output-dir", required=True)
    visualize_parser.add_argument("--dpi", type=int, default=150)
    visualize_parser.add_argument("--timeout", type=int, default=120)
    visualize_parser.add_argument("--format", choices=["text", "json"], default="text")
    visualize_parser.set_defaults(func=command_visualize_docx)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
