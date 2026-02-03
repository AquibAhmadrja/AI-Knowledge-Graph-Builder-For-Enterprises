import os
import json

# -------- CONFIG --------
CHUNKS_DIR = "C:\\Users\\aquib\\Infosys_project\\chunks_text"
OUTPUT_FILE = "C:\\Users\\aquib\\Infosys_project\\kg_text\\all_chunks.json"
# -----------------------


def main():
    all_chunks = []
    skipped_files = 0

    for file_name in os.listdir(CHUNKS_DIR):
        if not file_name.endswith("_chunks.json"):
            continue

        file_path = os.path.join(CHUNKS_DIR, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            if isinstance(chunks, list):
                all_chunks.extend(chunks)
            else:
                skipped_files += 1

        except Exception as e:
            print(f"⚠️ Skipping {file_name}: {e}")
            skipped_files += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Combined chunks saved to: {OUTPUT_FILE}")
    print(f"📊 Total chunks: {len(all_chunks)}")
    print(f"⚠️ Skipped files: {skipped_files}")


if __name__ == "__main__":
    main()
