
import json
import csv
import os
import re

INPUT_JSON = r"all_structured_semistructured_triples.json"
OUTPUT_CSV = r"neo4j_triples_semistructured.csv"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)


def clean_text(value):
    """
    Make text safe for Neo4j CSV:
    - Remove newlines
    - Normalize quotes
    - Remove non-printable chars
    """
    if value is None:
        return ""

    text = str(value)

    # remove newlines and tabs
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # remove non-printable characters
    text = re.sub(r"[^\x20-\x7E]", "", text)

    # normalize double quotes
    text = text.replace('"', "'")

    return text.strip()


def stream_json_array(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        buffer = ""

        for line in f:
            line = line.strip()

            if not line or line.startswith("["):
                continue

            if line.endswith("]"):
                break

            buffer += line

            if buffer.endswith("},"):
                try:
                    yield json.loads(buffer[:-1])
                except Exception:
                    pass
                buffer = ""

            elif buffer.endswith("}"):
                try:
                    yield json.loads(buffer)
                except Exception:
                    pass
                buffer = ""


with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(
        csvfile,
        quoting=csv.QUOTE_ALL,   # 🔥 force safe quoting
        escapechar="\\"
    )

    writer.writerow(["head", "relation", "tail", "doc_id"])

    written = 0
    skipped = 0

    for triple in stream_json_array(INPUT_JSON):

        if not isinstance(triple, dict):
            skipped += 1
            continue

        head = clean_text(triple.get("head"))
        relation = clean_text(triple.get("relation"))
        tail = clean_text(triple.get("tail"))
        doc_id = clean_text(triple.get("doc_id"))

        if not head or not relation or not tail:
            skipped += 1
            continue

        writer.writerow([head, relation, tail, doc_id])
        written += 1

        if written % 200000 == 0:
            print(f"🟢 Written {written} triples...")

print("\n✅ SAFE CSV generation completed")
print(f"🟢 Triples written: {written}")
print(f"⚠ Skipped records: {skipped}")
print(f"📄 Output CSV: {OUTPUT_CSV}")
