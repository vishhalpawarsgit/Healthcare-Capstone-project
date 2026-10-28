
import tempfile
import unittest
from pathlib import Path

from docx import Document

from app.ingestion.document_loader import load_document


class TestDocumentLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_txt(self):
        path = self.folder / "sample.txt"
        path.write_text(
            "Fictional hospital admission procedure.",
            encoding="utf-8",
        )

        result = load_document(path)

        self.assertEqual(result["file_type"], "txt")
        self.assertIn("admission procedure", result["text"])
        self.assertEqual(result["source"], "sample.txt")

    def test_load_docx(self):
        path = self.folder / "sample.docx"
        document = Document()
        document.add_paragraph("Fictional patient safety procedure.")
        document.save(path)

        result = load_document(path)

        self.assertEqual(result["file_type"], "docx")
        self.assertIn("patient safety", result["text"])

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_document(self.folder / "missing.txt")

    def test_unsupported_extension(self):
        path = self.folder / "sample.csv"
        path.write_text("example", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Unsupported file type"):
            load_document(path)

    def test_empty_file(self):
        path = self.folder / "empty.txt"
        path.write_bytes(b"")

        with self.assertRaisesRegex(ValueError, "is empty"):
            load_document(path)

    def test_whitespace_only_file(self):
        path = self.folder / "blank.txt"
        path.write_text("   \n  ", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "No extractable text"):
            load_document(path)

    def test_corrupt_docx(self):
        path = self.folder / "corrupt.docx"
        path.write_bytes(b"not a valid Word document")

        with self.assertRaisesRegex(ValueError, "Could not read"):
            load_document(path)

    def test_corrupt_pdf(self):
        path = self.folder / "corrupt.pdf"
        path.write_bytes(b"not a valid PDF")

        with self.assertRaisesRegex(ValueError, "Could not read"):
            load_document(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
