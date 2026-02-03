import faiss
import json
import re
import requests
from sentence_transformers import SentenceTransformer

# ================= CONFIG =================
FAISS_INDEX_PATH = "../vector_db/faiss_final.index"
METADATA_PATH = "../vector_db/metadata_final.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

OLLAMA_MODEL = "llama3"      # mistral / phi3 also fine
OLLAMA_URL = "http://localhost:11434/api/generate"

TOP_K = 5
OVERFETCH = 5000
# =========================================


# ---------- FACT CONFIG ----------
FACT_KEYWORDS = [
    "hire date", "hiredate", "start date", "startdate",
    "salary", "position", "department",
    "who", "when", "which", "associated", "acquired"
]

ATTRIBUTE_MAP = {
    "hire date": ["hiredate", "hire date"],
    "start date": ["startdate", "start date"],
    "salary": ["salary", "pay"],
    "position": ["position", "job"],
    "department": ["department"]
}
# --------------------------------


# ---------- Load FAISS ----------
def load_faiss():
    print("📦 Loading FAISS index...")
    index = faiss.read_index(FAISS_INDEX_PATH)

    print("📄 Loading metadata...")
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert index.ntotal == len(metadata), "❌ FAISS–metadata mismatch"
    return index, metadata


# ---------- Query Helpers ----------
def is_fact_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in FACT_KEYWORDS)


def extract_entity(query: str):
    match = re.search(r"(employee[_\s]?\d+)", query.lower())
    if match:
        return match.group(1).replace(" ", "_")
    return None


def extract_attribute(query: str):
    q = query.lower()
    for attr, keys in ATTRIBUTE_MAP.items():
        if any(k in q for k in keys):
            return attr
    return None


# ---------- Retrieve ----------
def retrieve_chunks(query, index, metadata, embed_model):
    query_emb = embed_model.encode([query], convert_to_numpy=True).astype("float32")
    _, indices = index.search(query_emb, OVERFETCH)

    chunks = []
    for idx in indices[0]:
        if idx == -1:
            continue
        meta = metadata[idx]
        if meta.get("text"):
            chunks.append(meta)
        if len(chunks) >= TOP_K:
            break

    return chunks


# ---------- Extractive Fact QA ----------
def extract_fact_answer(chunks, query):
    entity = extract_entity(query)
    attribute = extract_attribute(query)

    if not entity or not attribute:
        return None

    entity = entity.lower()
    keys = ATTRIBUTE_MAP[attribute]

    for c in chunks:
        text = c["text"].lower()
        if entity in text and any(k in text for k in keys):
            return c["text"]

    return None


def build_prompt(chunks, question):
    context = "\n".join(f"- {c['text']}" for c in chunks)

    return f"""
You are an analytical assistant.

Task:
- Answer the question using the provided context
- You may summarize and combine related points
- Do NOT invent facts
- It is acceptable if the information is partial
- Write a clear, human-like explanation (5–7 sentences)

Context:
{context}

Question:
{question}

Answer:
"""


# ---------- Ollama Call ----------
def generate_answer_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"].strip()


# ---------- MAIN ----------
def main():
    index, metadata = load_faiss()
    embed_model = SentenceTransformer(EMBEDDING_MODEL)

    print("\n🤖 RAG System Ready (type 'exit' to quit)\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() == "exit":
            break

        chunks = retrieve_chunks(query, index, metadata, embed_model)
        print(f"\n📄 Retrieved {len(chunks)} chunks")

        # 🔥 FACT MODE (NO LLM REASONING)
        if is_fact_query(query):
            answer = extract_fact_answer(chunks, query)
            print("\n🧠 Answer:\n")
            print(answer if answer else "The information is not available in the provided documents.")
            print("\n" + "=" * 80)
            continue

        # 🔥 GENERATIVE MODE
        prompt = build_prompt(chunks, query)
        answer = generate_answer_ollama(prompt)

        print("\n🧠 Answer:\n")
        print(answer)
        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
