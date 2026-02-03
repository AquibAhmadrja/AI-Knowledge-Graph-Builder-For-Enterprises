import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
import os

from typer import prompt

# ---------------- CONFIG ----------------
FAISS_INDEX_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\faiss_final.index"
METADATA_PATH = "C:\\Users\\aquib\\Infosys_project\\vector_db\\metadata_final.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
OVERFETCH = 5000

# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"
# ---------------------------------------


def load_faiss():
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


def decide_source(query: str):
    q = query.lower()

    if any(k in q for k in ["describe", "explain", "summary", "report", "how"]):
        return "PDF"
    if any(k in q for k in ["who", "when", "which", "associated", "acquired"]):
        return "KG"

    return None  # allow mixed


def retrieve_chunks(query, index, metadata, model):
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")

    distances, indices = index.search(query_embedding, OVERFETCH)

    preferred_source = decide_source(query)
    filtered = []
    mixed = []

    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        meta = metadata[idx]
        record = {
            "source": meta.get("source"),
            "text": meta.get("text")
        }

        if record["text"]:
            mixed.append(record)

        if preferred_source:
            if str(meta.get("source", "")).lower() == preferred_source.lower():
                filtered.append(record)

        if len(filtered) >= TOP_K and preferred_source:
            break
        if len(mixed) >= TOP_K and not preferred_source:
            break

    return filtered if filtered else mixed


def build_prompt(context_chunks, question):
    context_text = "\n".join(
        [f"- {chunk['text']}" for chunk in context_chunks]
    )

    return f"""
You are a professional assistant.

Instructions:
- Use ONLY the provided context
- Answer clearly and concisely
- Prefer the most relevant fact
- Write in natural human language
- If the answer is missing, say it is not available

Context:
{context_text}

Question:
{question}

Answer:
"""


def generate_answer(prompt):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a factual, context-grounded assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]


def main():
    index, metadata = load_faiss()
    model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")

    print("\n🤖 RAG System Ready (type 'exit' to quit)\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() == "exit":
            break

        chunks = retrieve_chunks(query, index, metadata, model)
        print(f"\n📄 Retrieved {len(chunks)} chunks\n")

        prompt = build_prompt(chunks, query)

        # 🔥 THIS WAS MISSING
        answer = generate_answer(prompt)

        print("🧠 Answer:\n")
        print(answer)

        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
