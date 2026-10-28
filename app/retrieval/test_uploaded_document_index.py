
import io
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

from app.retrieval.uploaded_document_index import (
    MAX_FILE_SIZE_BYTES,
    UploadedDocumentIndex,
)


def create_test_image(image_format="PNG", include_text=True):
    image = Image.new("RGB", (900, 180), "white")

    if include_text:
        draw = ImageDraw.Draw(image)
        draw.text(
            (25, 40),
            "Fictional Hospital Visitor Policy: Visitors check in at reception.",
            fill="black",
        )

    buffer = io.BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()


class TestUploadedDocumentImages(unittest.TestCase):
    def setUp(self):
        # Avoid downloading/loading the real embedding model in unit tests.
        self.embedding_patcher = patch(
            "app.retrieval.uploaded_document_index.EmbeddingModel"
        )
        MockEmbeddingModel = self.embedding_patcher.start()
        self.addCleanup(self.embedding_patcher.stop)

        self.embedding = MockEmbeddingModel.return_value
        self.embedding.dimensions = 3
        self.embedding.encode_texts.side_effect = (
            lambda texts: __import__("numpy").tile(
                __import__("numpy").array([[1.0, 0.0, 0.0]], dtype="float32"),
                (len(texts), 1),
            )
        )

        self.index = UploadedDocumentIndex(
            embedding_model=self.embedding
        )

    def test_index_png_with_ocr_text(self):
        content = create_test_image("PNG")

        with patch(
            "app.retrieval.uploaded_document_index.pytesseract.image_to_string",
            return_value="Visitors must check in at reception.",
        ):
            chunks = self.index.add_uploaded_file("visitor.png", content)

        self.assertGreater(chunks, 0)
        self.assertEqual(self.index.records[0]["metadata"]["source"], "visitor.png")
        self.assertEqual(self.index.records[0]["metadata"]["file_type"], "png")
        self.assertIn("reception", self.index.records[0]["text"])

    def test_index_jpeg_with_ocr_text(self):
        content = create_test_image("JPEG")

        with patch(
            "app.retrieval.uploaded_document_index.pytesseract.image_to_string",
            return_value="Visitors check in at reception.",
        ):
            chunks = self.index.add_uploaded_file("visitor.jpg", content)

        self.assertGreater(chunks, 0)
        self.assertEqual(self.index.records[0]["metadata"]["file_type"], "jpg")

    def test_reject_invalid_image_bytes(self):
        with self.assertRaisesRegex(ValueError, "Could not read image"):
            self.index.add_uploaded_file("broken.png", b"not an image")

    def test_reject_image_without_ocr_text(self):
        content = create_test_image("PNG", include_text=False)

        with patch(
            "app.retrieval.uploaded_document_index.pytesseract.image_to_string",
            return_value="   ",
        ):
            with self.assertRaisesRegex(ValueError, "No text could be extracted"):
                self.index.add_uploaded_file("blank.png", content)

    def test_reject_unsupported_extension(self):
        with self.assertRaisesRegex(ValueError, "Supported formats"):
            self.index.add_uploaded_file("document.csv", b"some content")

    def test_reject_oversized_upload(self):
        content = b"x" * (MAX_FILE_SIZE_BYTES + 1)

        with self.assertRaisesRegex(
            ValueError,
            "exceeds the 50 MiB file-size limit",
        ):
            self.index.add_uploaded_file("oversized.txt", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
