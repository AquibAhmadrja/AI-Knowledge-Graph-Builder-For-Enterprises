# rag_core.py
from email.mime import text
import faiss
import json
import re
from numpy import indices
import requests
from streamlit import text
from sentence_transformers import SentenceTransformer

# ================= CONFIG =================
# ================= CONFIG =================
FAISS_INDEX_PATH = "../vector_db/faiss_final.index"
METADATA_PATH = "../vector_db/metadata_final.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_URL = "http://localhost:11434/api/generate"

TOP_K = 5
OVERFETCH = 1000
# =========================================


# ---------- KEYWORDS ----------
FACT_KEYWORDS = [
    "hire date", "hiredate", "start date", "startdate",
    "salary", "position", "department",
    "who", "when", "which", "associated", "acquired"
]

RELATION_KEYWORDS = [
    "sent", "emailed", "sent email", "sent to",
    "received", "associated", "connected", "located in", "mentioned"
]

ATTRIBUTE_MAP = {
    "hire date": ["hiredate", "hire date"],
    "start date": ["startdate", "start date"],
    "salary": ["salary", "pay"],
    "position": ["position", "job"],
    "department": ["department"]
}
# -----------------------------------------


# ---------- Helper functions ----------
def is_fact_query(query):
    return any(k in query.lower() for k in FACT_KEYWORDS)


def is_relation_query(query):
    return any(k in query.lower() for k in RELATION_KEYWORDS)


def is_who_relation_query(query):
    q = query.lower()
    return "who" in q and any(k in q for k in ["sent", "emailed", "sent to"])


def extract_email(query):
    match = re.search(r"[\w\.-]+@[\w\.-]+", query.lower())
    return match.group(0) if match else None


def extract_entity(query):
    match = re.search(r"(employee[_\s]?\d+)", query.lower())
    return match.group(1).replace(" ", "_") if match else None


def extract_attribute(query):
    q = query.lower()
    for attr, keys in ATTRIBUTE_MAP.items():
        if any(k in q for k in keys):
            return attr
    return None
# -----------------------------------------


# ---------- RAG ENGINE ----------
class RAGEngine:
    def __init__(self):
        self.index = faiss.read_index(FAISS_INDEX_PATH)

        # Smart loading - handles both JSON array and JSONL formats
        self.metadata = []
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            
            # Try loading as JSON array first
            if content.startswith('['):
                try:
                    self.metadata = json.loads(content)
                    print(f"✓ Loaded metadata as JSON array: {len(self.metadata)} items")
                except json.JSONDecodeError:
                    print("✗ Failed to load as JSON array, trying JSONL...")
                    self._load_jsonl(content)
            else:
                # Try JSONL format
                self._load_jsonl(content)

        if not self.metadata:
            raise ValueError("Failed to load metadata from file")

        self.embed_model = SentenceTransformer(EMBEDDING_MODEL)

        # Verify consistency
        if self.index.ntotal != len(self.metadata):
            print(f"⚠ Warning: FAISS index has {self.index.ntotal} vectors but metadata has {len(self.metadata)} items")

    def _load_jsonl(self, content):
        """Load JSONL format (one JSON object per line)"""
        for line in content.split('\n'):
            line = line.strip()
            if line:
                try:
                    self.metadata.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠ Skipping invalid JSON line: {line[:50]}... Error: {e}")
        print(f"✓ Loaded metadata as JSONL: {len(self.metadata)} items")

    def retrieve_chunks(self, query):
        emb = self.embed_model.encode([query], convert_to_numpy=True).astype("float32")
        _, indices = self.index.search(emb, OVERFETCH)

        chunks = []

        fact_mode = is_fact_query(query) or is_relation_query(query)

        for idx in indices[0]:
            if idx == -1 or idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]
            text = meta.get("text", "")
            if not text:
                continue

            # 🔹 FACT / KG MODE → allow short text
            if fact_mode:
                chunks.append(meta)

            # 🔹 PDF / DESCRIPTIVE MODE → require longer text
            else:
                if len(text) >= 80:   # you can tune this (60–120)
                    chunks.append(meta)

            if len(chunks) >= TOP_K:
                break

        return chunks


    # ---------- ATTRIBUTE FACT ----------
    def extract_fact_answer(self, chunks, query):
        entity = extract_entity(query)
        attribute = extract_attribute(query)
        if not entity or not attribute:
            return None

        for c in chunks:
            text = c["text"].lower()
            if entity.lower() in text:
                for key in ATTRIBUTE_MAP[attribute]:
                    if key.replace(" ", "") in text or key in text:
                        return c["text"]
        return None

    # ---------- RELATION FACT ----------
    def extract_relation_answer(self, chunks, query):
        email = extract_email(query)
        if not email:
            return None

        for c in chunks:
            text = c["text"].lower()
            if email in text and ("sent" in text or "sent_to" in text or "emailed" in text):
                return c["text"]
        return None

    def extract_sender_from_kg(self, chunks, query):
        receiver = extract_email(query)
        if not receiver:
            return None

        for c in chunks:
            text = c["text"].lower()
            # Expected: ingrid.immer@williams.com sent to chris.germany@enron.com
            if receiver in text and "sent" in text:
                sender = text.split(" sent")[0].strip()
                return sender
        return None
    
    def is_context_relevant(self, query, chunks):
        query_keywords = set(query.lower().split())
        match_count = 0

        for c in chunks:
            text = c["text"].lower()
            if any(word in text for word in query_keywords):
                match_count += 1

        # Require at least 1 meaningful overlap
        return match_count > 0


    # ---------- GENERATION ----------
    def generate_with_ollama(self, prompt):
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    # ---------- MAIN ANSWER ----------
    def answer(self, query):

        chunks = self.retrieve_chunks(query)

        if not chunks or not self.is_context_relevant(query, chunks):
            return {
                "answer": "The information is not available in the provided documents.",
                "sources": [],
                "confidence": 0.0
            }

        used_sources = set()

        for c in chunks:
            if c.get("source_file"):
                used_sources.add(c["source_file"])
            else:
                # fallback for KG triples
                used_sources.add("Knowledge Graph")
        used_sources = list(used_sources)

        # 1️⃣ WHO-SENT (KG deterministic)
        if is_who_relation_query(query):
            sender = self.extract_sender_from_kg(chunks, query)
            if sender:
                return {
                    "answer": sender,
                    "sources": used_sources,
                    "confidence": 0.95
                }
        # 2️⃣ Attribute-based facts
        if is_fact_query(query):
            fact = self.extract_fact_answer(chunks, query)
            if fact:
                return {
                    "answer": fact,
                    "sources": used_sources,
                    "confidence": 0.95
                }
        # 3️⃣ Relation facts
        if is_relation_query(query):
            relation_fact = self.extract_relation_answer(chunks, query)
            if relation_fact:
                return {
                    "answer": relation_fact,
                    "sources": used_sources,
                    "confidence": 0.90
                }
        # 4️⃣ Descriptive / summarization using LLM
        context = "\n".join(f"- {c['text']}" for c in chunks)
        prompt = f"""You are an analytical assistant.

Task:
- Answer the question using the provided context
- You may summarize and combine related points but for the information which is no present in the context, do NOT invent facts and clearly just say that the information is not present. and the source is not available
- Do NOT invent facts
- If the answer is not present, say so clearly
- Write a clear, human-like explanation (4–6 sentences)

Context:
{context}

Question:
{query}

Answer:"""
        
        answer_text = self.generate_with_ollama(prompt)

        # detect PDF usage
        if any(c.get("source_domain") == "pdf" or c.get("source_type") == "unstructured" for c in chunks):
            used_sources.add("PDF Documents")

        return {
            "answer": answer_text,
            "sources": list(used_sources),
            "confidence": 0.90
        }