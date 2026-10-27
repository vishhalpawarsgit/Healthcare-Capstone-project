
from pathlib import Path

from document_loader import load_document


project_root = Path(__file__).resolve().parents[2]
data_folder = project_root / "data" / "raw_data"

pdf_files = sorted(data_folder.glob("*.pdf"))

if not pdf_files:
    raise RuntimeError(f"No PDF files found in {data_folder}")

print(f"Found {len(pdf_files)} PDF files\n")

failed = []

for pdf_path in pdf_files:
    try:
        result = load_document(pdf_path)

        print(f"✅ File: {result['source']}")
        print(f"   Pages: {result['metadata']['page_count']}")
        print(f"   Extracted characters: {len(result['text'])}")

        if not result["text"].strip():
            print("   ⚠️ No text extracted")
            failed.append(pdf_path.name)

    except Exception as exc:
        print(f"❌ File: {pdf_path.name}")
        print(f"   Error: {exc}")
        failed.append(pdf_path.name)

print("\n-------------------------")
print(f"Total PDFs: {len(pdf_files)}")
print(f"Failed or empty: {len(failed)}")

if failed:
    print("Files needing investigation:")
    for name in failed:
        print(f"- {name}")
else:
    print("✅ All PDF loader checks passed!")
