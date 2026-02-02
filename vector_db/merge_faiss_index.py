import faiss

# -------- CONFIG --------
MAIN_INDEX_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\faiss.index"
KG_INDEX_PATH = "C:\\Users\\aquib\\Infosys_project\\kg_text\\faiss.index"

FINAL_INDEX_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\faiss_final.index"

CHUNK_SIZE = 50000   # adjust if needed
# -----------------------


def add_in_chunks(src_index, dst_index, label):
    total = src_index.ntotal
    print(f"➕ Adding {label} vectors in chunks ({total})")

    for start in range(0, total, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, total)
        vectors = src_index.reconstruct_n(start, end - start)
        dst_index.add(vectors)
        print(f"   ✔ {label}: added {end}/{total}")


def main():
    print("📦 Loading main FAISS index...")
    index_main = faiss.read_index(MAIN_INDEX_PATH)

    print("📦 Loading KG FAISS index...")
    index_kg = faiss.read_index(KG_INDEX_PATH)

    assert index_main.d == index_kg.d, "Embedding dimension mismatch"

    dim = index_main.d
    index_final = faiss.IndexFlatL2(dim)

    add_in_chunks(index_main, index_final, "MAIN")
    add_in_chunks(index_kg, index_final, "KG")

    print(f"📊 Total vectors after merge: {index_final.ntotal}")

    faiss.write_index(index_final, FINAL_INDEX_PATH)
    print("✅ Final FAISS index saved")


if __name__ == "__main__":
    main()
