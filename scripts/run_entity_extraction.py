import os
import json
from entity_extraction import extract_entities_from_text


def enrich_document(doc):
    """
    Add entities to one normalized document
    """
    entities = extract_entities_from_text(doc.get("text"))
    doc["entities"] = entities
    return doc


def process_normalized_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if not file.endswith(".json"):
            continue

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"entity_{file}")

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle list OR single JSON
        if isinstance(data, list):
            enriched = [enrich_document(doc) for doc in data]
        else:
            enriched = enrich_document(data)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=4)

        print(f"Processed: {file}")


if __name__ == "__main__":
    process_normalized_folder(
        "C:\\Users\\aquib\\Infosys_project\\Normalized_data",
        "C:\\Users\\aquib\\Infosys_project\\Entity_Enriched_Data"
    )
