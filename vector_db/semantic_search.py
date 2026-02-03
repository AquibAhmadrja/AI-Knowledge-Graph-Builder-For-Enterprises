# print("Starting semantic search module...")
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
FAISS_INDEX_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\faiss_final.index"
METADATA_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\metadata_final.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
OVERFETCH = 200     
# ---------------------------------------


def load_faiss_index():
    print("📦 Loading FAISS index...")
    index = faiss.read_index(FAISS_INDEX_PATH)
    print(f"✅ FAISS index loaded | Total vectors: {index.ntotal}")
    return index


def load_metadata():
    print("📄 Loading metadata...")
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    print(f"✅ Metadata loaded | Entries: {len(metadata)}")
    return metadata


def decide_source(query: str):
    """
    Simple heuristic to decide preferred source.
    """
    q = query.lower()

    descriptive_keywords = [
        "what happened", "describe", "explain", "summary", "overview", "report"
    ]
    factual_keywords = [
        "who", "when", "which", "associated", "acquired"
    ]

    if any(k in q for k in descriptive_keywords):
        return "PDF"
    if any(k in q for k in factual_keywords):
        return "KG"

    # Default fallback
    return "PDF"


def semantic_search(
    query,
    index,
    metadata,
    model,
    top_k=5,
    preferred_source=None
):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    OVERFETCH = 5000  
    distances, indices = index.search(query_embedding, OVERFETCH)

    filtered_results = []
    mixed_results = []

    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        meta = metadata[idx]
        result = {
            "rank": None,
            "distance": float(distances[0][rank]),
            "source": meta.get("source"),
            "doc_id": meta.get("doc_id"),
            "source_file": meta.get("source_file"),
            "chunk_id": meta.get("chunk_id"),
            "text": meta.get("text")
        }

        # Collect mixed results (fallback)
        if len(mixed_results) < top_k:
            mixed_results.append(result)

        # Collect preferred-source results
        if preferred_source:
            if str(meta.get("source", "")).lower() == preferred_source.lower():
                filtered_results.append(result)

        if len(filtered_results) >= top_k:
            break

    # 🔁 Decide what to return
    final_results = filtered_results if filtered_results else mixed_results

    # Assign ranks
    for i, r in enumerate(final_results):
        r["rank"] = i + 1

    return final_results



def main():
    # Load index & metadata
    index = load_faiss_index()
    metadata = load_metadata()

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")

    print("\n🔎 Semantic Search Ready")
    print("Type a query (or 'exit' to quit)\n")

    while True:
        query = input("Query: ").strip()
        if query.lower() == "exit":
            break

        preferred_source = decide_source(query)
        print(f"\n🔧 Preferred source: {preferred_source}")

        results = semantic_search(
            query,
            index,
            metadata,
            model,
            TOP_K,
            preferred_source=preferred_source
        )

        print("\n📄 Top Results:\n")
        if not results:
            print("❌ No results found.")
            continue

        for r in results:
            print(f"Rank {r['rank']} | Distance: {r['distance']:.4f}")
            print(f"Source: {r['source']} | File: {r['source_file']}")
            print(f"Chunk ID: {r['chunk_id']}")
            print(f"Text Preview:\n{r['text'][:500]}...")
            print("-" * 80)


if __name__ == "__main__":
    main()
