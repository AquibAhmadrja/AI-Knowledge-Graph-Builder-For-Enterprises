import json
import re
from itertools import combinations



def extract_email_relations(doc):
    relations = []
    text = doc.get("text", "")

    if not text:
        return relations

    sender = re.search(r"From:\s*(.*)", text, re.IGNORECASE)
    receiver = re.search(r"To:\s*(.*)", text, re.IGNORECASE)

    if sender and receiver:
        relations.append({
            "subject": sender.group(1).strip(),
            "predicate": "SENT_TO",
            "object": receiver.group(1).strip(),
            "doc_id": doc["doc_id"]
        })

    return relations


# ---------------- ENTITY CO-OCCURRENCE RULES ----------------

def extract_entity_relations(doc):
    relations = []
    entities = doc.get("entities", [])

    for e1, e2 in combinations(entities, 2):

        # PERSON -> ORG
        if e1["label"] == "PERSON" and e2["label"] == "ORG":
            relations.append({
                "subject": e1["text"],
                "predicate": "ASSOCIATED_WITH",
                "object": e2["text"],
                "doc_id": doc["doc_id"]
            })

        # ORG -> GPE
        if e1["label"] == "ORG" and e2["label"] == "GPE":
            relations.append({
                "subject": e1["text"],
                "predicate": "LOCATED_IN",
                "object": e2["text"],
                "doc_id": doc["doc_id"]
            })

        # generic mention
        relations.append({
            "subject": e1["text"],
            "predicate": "MENTIONS",
            "object": e2["text"],
            "doc_id": doc["doc_id"]
        })

    return relations



def extract_relations(all_docs):
    all_relations = []

    for doc in all_docs:
        if doc.get("source_domain") == "email":
            all_relations.extend(extract_email_relations(doc))

        if "entities" in doc:
            all_relations.extend(extract_entity_relations(doc))

    return all_relations



if __name__ == "__main__":

    with open("all_entity_docs.json", "r", encoding="utf-8") as f:
        all_docs = json.load(f)

    relations = extract_relations(all_docs)

    with open("relations.json", "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4)

    print(f"Extracted {len(relations)} relations")
