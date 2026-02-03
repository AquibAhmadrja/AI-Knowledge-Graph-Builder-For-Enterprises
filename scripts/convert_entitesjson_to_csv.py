import json
import csv

INPUT_JSON = r"C:\Users\aquib\Infosys_project\all_entity_docs_1.json"
OUTPUT_CSV = r"C:\Users\aquib\Infosys_project\entities.csv"

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    docs = json.load(f)

rows = []
seen = set()

for doc in docs:
    doc_id = doc["doc_id"]

    for e in doc.get("entities", []):
        name = e["text"].strip()
        etype = e["label"]

        key = (name.lower(), etype)
        if key in seen:
            continue

        seen.add(key)
        rows.append({
            "name": name,
            "type": etype,
            "doc_id": doc_id
        })

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "type", "doc_id"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Entities exported: {len(rows)}")
