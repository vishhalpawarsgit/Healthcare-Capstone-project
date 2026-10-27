
from pathlib import Path
from typing import Any

from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def load_document(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        page_count = len(reader.pages)

    elif extension == ".docx":
        document = Document(str(path))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        page_count = None

    else:
        text = path.read_text(encoding="utf-8")
        page_count = None

    return {
        "source": path.name,
        "file_type": extension.lstrip("."),
        "text": text.strip(),
        "metadata": {
            "file_name": path.name,
            "file_size_bytes": path.stat().st_size,
            "page_count": page_count,
        },
    }
