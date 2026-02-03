import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# -------- CONFIG --------
INPUT_FILE = "C:\\Users\\aquib\\Infosys_project\\kg_text\\semi_chunks.json"
OUTPUT_DIR = "C:\\Users\\aquib\\Infosys_project\\kg_text"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32
# ------------------------


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Load final chunks
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = []
    metadata = []

    for chunk in chunks:
        text = chunk.get("text", "").strip()
        if not text:
            continue

        texts.append(text)
        metadata.append({
            "chunk_id": chunk.get("chunk_id"),
            "source": chunk.get("source"),
            "doc_id": chunk.get("doc_id"),
            "source_file": chunk.get("source_file")
        })

    print(f"📄 Total chunks to embed: {len(texts)}")

    # 2. Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    # 3. Generate embeddings
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # 4. Save embeddings & metadata
    np.save(os.path.join(OUTPUT_DIR, "embeddings.npy"), embeddings)

    with open(os.path.join(OUTPUT_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("✅ Embeddings generated successfully")
    print(f"📐 Embedding shape: {embeddings.shape}")
    print(f"📁 Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
