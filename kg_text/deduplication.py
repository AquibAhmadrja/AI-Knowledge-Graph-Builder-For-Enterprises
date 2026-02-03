import json
import hashlib

INPUT_FILE = "final_chunks.json"
OUTPUT_FILE = "final_chunks_dedup.json"

def hash_text(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    seen = set()
    dedup_chunks = []

    for chunk in chunks:
        text = chunk.get("text", "").strip()
        if not text:
            continue

        h = hash_text(text)
        if h in seen:
            continue

        seen.add(h)
        dedup_chunks.append(chunk)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dedup_chunks, f, indent=2, ensure_ascii=False)

    print("Original chunks:", len(chunks))
    print("After deduplication:", len(dedup_chunks))

if __name__ == "__main__":
    main()
