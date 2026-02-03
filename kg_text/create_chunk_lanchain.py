import os
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------- CONFIG --------
PDF_CHUNKS_DIR = "chunks_text"
KG_SENTENCES_FILE = "semistructured_triples.txt"
OUTPUT_DIR = "chunks_text"
OUTPUT_FILE = "final_chunks.json"

KG_CHUNK_SIZE = 200
KG_OVERLAP = 20
# -----------------------


# 🔹 LangChain splitter for KG sentences (optional but standard)
kg_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=KG_CHUNK_SIZE,
    chunk_overlap=KG_OVERLAP,
    separators=["\n\n", "\n", " ", ""]
)


def load_pdf_chunks():
    """
    Load already-chunked PDF JSON files.
    No re-chunking is done here.
    """
    all_pdf_chunks = []

    for file_name in os.listdir(PDF_CHUNKS_DIR):
        if not file_name.endswith("_chunks.json"):
            continue

        file_path = os.path.join(PDF_CHUNKS_DIR, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            for chunk in chunks:
                record = {
                    "chunk_id": f"pdf_{chunk.get('chunk_id')}",
                    "text": chunk.get("text", ""),
                    "source": "PDF",
                    "doc_id": chunk.get("doc_id"),
                    "source_file": chunk.get("source_file")
                }
                all_pdf_chunks.append(record)

        except Exception as e:
            print(f"⚠️ Skipping {file_name}: {e}")

    return all_pdf_chunks


def load_kg_chunks():
    """
    Load KG sentences and chunk them using LangChain.
    """
    kg_chunks = []

    if not os.path.exists(KG_SENTENCES_FILE):
        return kg_chunks

    with open(KG_SENTENCES_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 🔹 LangChain chunking applied here
    split_sentences = kg_text_splitter.split_text(raw_text)

    for idx, sentence in enumerate(split_sentences):
        sentence = sentence.strip()
        if not sentence:
            continue

        record = {
            "chunk_id": f"kg_{idx}",
            "text": sentence,
            "source": "KG"
        }
        kg_chunks.append(record)

    return kg_chunks


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_chunks = load_pdf_chunks()
    kg_chunks = load_kg_chunks()

    final_chunks = pdf_chunks + kg_chunks

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=2, ensure_ascii=False)

    print("✅ Final chunks created")
    print(f"📄 PDF chunks: {len(pdf_chunks)}")
    print(f"🧠 KG chunks: {len(kg_chunks)}")
    print(f"📊 Total chunks: {len(final_chunks)}")
    print(f"📁 Saved to: {output_path}")


if __name__ == "__main__":
    main()
