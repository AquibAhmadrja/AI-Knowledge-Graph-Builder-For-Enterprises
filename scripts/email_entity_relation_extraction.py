import json
from itertools import combinations

INPUT_JSON = "C:\\Users\\aquib\\Infosys_project\\Entity_Enriched_Data\\entity_emails_spacy.json"
OUTPUT_JSON = "C:\\Users\\aquib\\Infosys_project\\email_entity_relations.json"


def extract_entity_relations_from_email(doc):
    """
    Extract semantic relations from spaCy entities in email body
    """
    relations = []
    entities = doc.get("entities", [])
    doc_id = doc.get("doc_id")

    # normalize entity texts (avoid duplicates)
    unique_entities = {}
    for e in entities:
        key = (e["text"].strip(), e["label"])
        unique_entities[key] = e["label"]

    entity_list = [
        {"text": text, "label": label}
        for (text, label) in unique_entities
    ]

    for e1, e2 in combinations(entity_list, 2):

        # PERSON <-> PERSON
        if e1["label"] == "PERSON" and e2["label"] == "PERSON":
            relations.append({
                "subject": e1["text"],
                "predicate": "MENTIONS",
                "object": e2["text"],
                "doc_id": doc_id
            })

        # PERSON -> ORG
        if e1["label"] == "PERSON" and e2["label"] == "ORG":
            relations.append({
                "subject": e1["text"],
                "predicate": "ASSOCIATED_WITH",
                "object": e2["text"],
                "doc_id": doc_id
            })

        # ORG -> GPE
        if e1["label"] == "ORG" and e2["label"] == "GPE":
            relations.append({
                "subject": e1["text"],
                "predicate": "LOCATED_IN",
                "object": e2["text"],
                "doc_id": doc_id
            })

    return relations


def extract_all_email_entity_relations(docs):
    all_relations = []

    for idx, doc in enumerate(docs, start=1):
        rels = extract_entity_relations_from_email(doc)
        all_relations.extend(rels)

        if idx % 500 == 0:
            print(f"🟢 Processed {idx} email docs")

    return all_relations


if __name__ == "__main__":

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        email_docs = json.load(f)

    print(f"🚀 Extracting entity-based relations from {len(email_docs)} emails")

    relations = extract_all_email_entity_relations(email_docs)

    # ensure output directory exists
    import os
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4)

    print(f"\n✅ Extracted {len(relations)} email entity relations")
    print(f"📄 Output: {OUTPUT_JSON}")
