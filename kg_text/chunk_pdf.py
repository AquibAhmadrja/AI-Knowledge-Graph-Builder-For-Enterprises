import os
import json
from pathlib import Path

# ---------- CONFIG ----------
INPUT_DIR = "C:\\Users\\aquib\\Infosys_project\\Normalized_data"   
OUTPUT_DIR = "C:\\Users\\aquib\\Infosys_project\\chunks_text"

CHUNK_SIZE = 400
OVERLAP = 50
# ---------------------------


def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        if chunk_words:
            chunks.append(" ".join(chunk_words))

        start = end - overlap

    return chunks


def extract_text_safe(data, file_name):
    """
    Safely extract text from various normalized JSON formats.
    """
    if isinstance(data, dict):
        text = data.get("text")
        if isinstance(text, str) and text.strip():
            return text.strip()

    print(f"⚠️ Skipping {file_name}: no valid 'text' field")
    return None


def process_json_file(file_path):
    file_name = os.path.basename(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read {file_name}: {e}")
        return []

    text = extract_text_safe(data, file_name)
    if not text:
        return []

    chunks = chunk_text(text)

    doc_id = data.get("doc_id", Path(file_name).stem)
    source_file = data.get("source_file", file_name)

    chunk_records = []
    for i, chunk in enumerate(chunks):
        record = {
            "chunk_id": f"{doc_id}_chunk_{i}",
            "doc_id": doc_id,
            "text": chunk,
            "source_type": data.get("source_type", "unstructured"),
            "source_domain": data.get("source_domain", "pdf"),
            "source_file": source_file
        }
        chunk_records.append(record)

    return chunk_records


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_chunks = 0

    for file_name in os.listdir(INPUT_DIR):
        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(INPUT_DIR, file_name)
        chunks = process_json_file(file_path)

        if not chunks:
            continue

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{Path(file_name).stem}_chunks.json"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        total_chunks += len(chunks)
        print(f"✅ {file_name}: {len(chunks)} chunks created")

    print(f"\n📊 Total chunks created: {total_chunks}")


if __name__ == "__main__":
    main()


