import json

# -------- CONFIG --------
FINAL_CHUNKS_FILE = "C:\\Users\\aquib\\Infosys_project\\kg_text\\semi_chunks.json"
OLD_METADATA_FILE = "C:\\Users\\aquib\\Infosys_project\\kg_text\\metadata_semi.json"
NEW_METADATA_FILE = "C:\\Users\\aquib\\Infosys_project\\kg_text\\metadata_semi_with_text.json"
# ------------------------


def main():
    with open(FINAL_CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    with open(OLD_METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert len(chunks) == len(metadata), "Mismatch between chunks and metadata!"

    new_metadata = []

    for chunk, meta in zip(chunks, metadata):
        meta["text"] = chunk.get("text", "")
        new_metadata.append(meta)

    with open(NEW_METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(new_metadata, f, indent=2, ensure_ascii=False)

    print("✅ Metadata fixed")
    print(f"📄 Entries: {len(new_metadata)}")


if __name__ == "__main__":
    main()
