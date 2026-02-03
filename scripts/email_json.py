

import csv
import json
import sys

# Windows-safe CSV field size fix
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

def ingest_enron_emails(csv_file):
    documents = []

    with open(csv_file, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        for row in reader:
            documents.append({
                "source_type": "unstructured",
                "source_domain": "email",
                "source_file": csv_file,
                "metadata": {
                    "file_id": row.get("file")   # only metadata available
                },
                "content": (row.get("message") or "").strip()
            })

    return documents
emails_json = ingest_enron_emails("Data\\Unstructured_Data\\emails.csv")
with open("emails.json", "w", encoding="utf-8") as f:
    json.dump(emails_json, f, indent=4)