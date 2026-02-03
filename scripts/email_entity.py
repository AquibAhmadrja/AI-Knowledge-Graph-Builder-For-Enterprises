import json
import spacy
import time
import os
from itertools import islice

# ================= CONFIG =================
INPUT_JSON = "C:\\Users\\aquib\\Infosys_project\\Normalized_data\\normalized_emails.json"
OUTPUT_JSON = "C:\\Users\\aquib\\Infosys_project\\Entity_Enriched_Data\\entity_emails_spacy.json"
PROGRESS_FILE = "C:\\Users\\aquib\\Infosys_project\\Entity_Enriched_Data\\email_progress.json"

TOTAL_EMAIL_LIMIT = 10000     
BATCH_SIZE = 100              
MAX_TEXT_LENGTH = 5000 
# =========================================


# ---------- LOAD SPACY (FAST MODE) ----------
nlp = spacy.load(
    "en_core_web_sm",
    disable=["tagger", "parser", "lemmatizer"]
)


# ---------- LOAD / SAVE PROGRESS ----------
def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 0
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("last_processed_index", 0)


def save_progress(index):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_processed_index": index}, f)


# ---------- BATCH GENERATOR ----------
def batch_iterable(iterable, batch_size):
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch


# ---------- ENTITY EXTRACTION ----------
def extract_entities_spacy_batch(email_docs, start_index):
    results = []
    processed = 0
    start_time = time.time()

    # 🔥 LIMIT TOTAL EMAILS TO 10K
    slice_docs = email_docs[start_index:start_index + TOTAL_EMAIL_LIMIT]

    total_to_process = len(slice_docs)

    for batch_no, batch in enumerate(batch_iterable(slice_docs, BATCH_SIZE), start=1):

        texts = [
            doc["text"][:MAX_TEXT_LENGTH]
            for doc in batch
            if doc.get("text")
        ]

        spacy_docs = nlp.pipe(texts, batch_size=BATCH_SIZE)

        for email_doc, spacy_doc in zip(batch, spacy_docs):
            email_doc["entities"] = [
                {"text": ent.text, "label": ent.label_}
                for ent in spacy_doc.ents
            ]
            results.append(email_doc)

        processed += len(batch)

        elapsed = time.time() - start_time
        percent = (processed / total_to_process) * 100

        print(
            f"🟢 Batch {batch_no} | "
            f"{processed}/{total_to_process} emails "
            f"({percent:.2f}%) | "
            f"Elapsed: {elapsed:.1f}s"
        )

    return results, start_index + processed


# ---------- RUN ----------
if __name__ == "__main__":

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        all_email_docs = json.load(f)

    start_index = load_progress()

    print(f"\n🚀 Starting spaCy NER for emails")
    print(f"📌 Starting index: {start_index}")
    print(f"📦 Batch size: {BATCH_SIZE}")
    print(f"🔢 Max emails this run: {TOTAL_EMAIL_LIMIT}")
    print(f"✂ Text length limit: {MAX_TEXT_LENGTH}\n")

    enriched_emails, new_index = extract_entities_spacy_batch(
        all_email_docs,
        start_index
    )

    # Append results safely
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(enriched_emails)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)

    save_progress(new_index)

    print("\n✅ spaCy entity extraction completed")
    print(f"📄 Output file: {OUTPUT_JSON}")
    print(f"📌 Emails processed till index: {new_index}")
