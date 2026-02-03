import json
import uuid
from datetime import datetime
import os


def normalize_document(doc):
    return {
        "doc_id": str(uuid.uuid4()),
        "source_type": doc.get("source_type"),
        "source_domain": doc.get("source_domain"),
        "source_file": doc.get("source_file"),
        "metadata": doc.get("metadata", {}),
        "text": doc.get("content") if "content" in doc else None,
        "structured_data": doc.get("data") if "data" in doc else None,
        "ingested_at": datetime.utcnow().isoformat()
    }


def normalize_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if not file.endswith(".json"):
            continue

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"normalized_{file}")

        with open(input_path, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

        if isinstance(raw_json, list):
            normalized = [normalize_document(doc) for doc in raw_json]
        else:
            normalized = normalize_document(raw_json)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=4)


# -------- USAGE --------
if __name__ == "__main__":
    normalize_folder("C:\\Users\\aquib\\Infosys_project\\json_data", "C:\\Users\\aquib\\Infosys_project\\Normalized_data")
