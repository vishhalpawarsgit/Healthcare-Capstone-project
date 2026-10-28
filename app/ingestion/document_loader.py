
from pathlib import Path
from typing import Any

from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def load_document(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path.name}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path.name}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension or '(no extension)'}. "
            "Supported formats: PDF, DOCX, TXT."
        )

    if path.stat().st_size == 0:
        raise ValueError(f"{path.name} is empty.")

    try:
        if extension == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
            page_count = len(reader.pages)

        elif extension == ".docx":
            document = Document(str(path))
            text = "\n".join(
                paragraph.text for paragraph in document.paragraphs
            )
            page_count = None

        else:
            text = path.read_text(encoding="utf-8")
            page_count = None

    except Exception as exc:
        raise ValueError(
            f"Could not read {path.name}. The file may be corrupt, "
            "invalid, or encoded incorrectly."
        ) from exc

    text = text.strip()

    if not text:
        raise ValueError(
            f"No extractable text found in {path.name}. "
            "Scanned PDFs may require OCR."
        )

    return {
        "source": path.name,
        "file_type": extension.lstrip("."),
        "text": text,
        "metadata": {
            "file_name": path.name,
            "file_size_bytes": path.stat().st_size,
            "page_count": page_count,
        },
    }
