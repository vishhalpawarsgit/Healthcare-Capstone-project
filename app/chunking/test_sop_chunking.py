
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root / "app" / "ingestion"))

from document_loader import load_document
from text_chunker import chunk_text


pdf_path = project_root / "data" / "raw_data" / "Admission Process- SOP.pdf"

# Extract text from the real hospital SOP.
document = load_document(pdf_path)
text = document["text"]

# Split the extracted text into overlapping chunks.
chunks = chunk_text(
    text,
    chunk_size=1000,
    chunk_overlap=150,
)

print("Real SOP chunking test")
print("----------------------")
print("Source:", document["source"])
print("Extracted characters:", len(text))
print("Total chunks:", len(chunks))

for chunk in chunks[:3]:
    print(f"\nChunk {chunk['chunk_index']}")
    print(chunk["text"][:250])

assert text.strip()
assert chunks
assert all(chunk["text"].strip() for chunk in chunks)
assert all(len(chunk["text"]) <= 1000 for chunk in chunks)

print("\n✅ Real SOP chunking test passed!")
