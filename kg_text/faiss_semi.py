import os
import json
import faiss
import numpy as np
import shutil

# -------- CONFIG --------
EMBEDDINGS_PATH = "C:\\Users\\aquib\\Infosys_project\\kg_text\\embeddings.npy"
METADATA_PATH = "C:\\Users\\aquib\\Infosys_project\\kg_text\\metadata.json"

OUTPUT_DIR = "C:\\Users\\aquib\\Infosys_project\\kg_text"
FAISS_INDEX_FILE = "faiss.index"
# ------------------------


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("📦 Loading embeddings...")
    embeddings = np.load(EMBEDDINGS_PATH, mmap_mode="r")
    embeddings = embeddings.astype("float32")

    num_vectors, dim = embeddings.shape
    print(f"📐 Embeddings shape: {num_vectors} x {dim}")

    print("⚙️ Creating FAISS IndexFlatL2...")
    index = faiss.IndexFlatL2(dim)

    print("➕ Adding embeddings to index (this may take time)...")
    index.add(embeddings)

    print("💾 Saving FAISS index...")
    faiss.write_index(
        index,
        os.path.join(OUTPUT_DIR, FAISS_INDEX_FILE)
    )

    # Copy metadata (do NOT regenerate)
    shutil.copy(
        METADATA_PATH,
        os.path.join(OUTPUT_DIR, "metadata.json")
    )

    print("✅ FAISS index created successfully")
    print(f"📁 Saved to: {OUTPUT_DIR}")
    print(f"🔢 Total vectors indexed: {index.ntotal}")


if __name__ == "__main__":
    main()
