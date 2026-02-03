import json
import os
import re

# ---------- CONFIG ----------
TRIPLES_PATH = "all_structured_semistructured_triples.json" 
OUTPUT_PATH = "semistructured_triples.txt"
# ----------------------------


def clean_entity(entity: str) -> str:
    """
    Remove trailing metadata like:
    Ronald Fain/HR/Corp -> Ronald Fain
    Meredith Homco/HOU/ECT@ECT -> Meredith Homco
    """
    # split on / or @ and keep first part
    entity = re.split(r"[/@]", entity)[0]
    return entity.strip()


def normalize_relation(relation: str) -> str:
    """
    Convert relations to readable English
    """
    relation = relation.lower().replace("_", " ")

    relation_map = {
        "associated with": "is associated with",
        "works for": "works for",
        "located in": "is located in",
        "member of": "is a member of"
    }

    return relation_map.get(relation, relation)


def load_triples(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "triples" in data:
        return data["triples"]
    else:
        raise ValueError("Unsupported triples.json format")


def triples_to_sentences(triples):
    sentences = set()

    for t in triples:
        head = clean_entity(t.get("head", ""))
        tail = clean_entity(t.get("tail", ""))
        relation = t.get("relation", "")

        if not head or not tail or not relation:
            continue

        rel_text = normalize_relation(relation)
        sentence = f"{head} {rel_text} {tail}."

        sentences.add(sentence)

    return sorted(sentences)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    triples = load_triples(TRIPLES_PATH)
    sentences = triples_to_sentences(triples)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for s in sentences:
            f.write(s + "\n")

    print(f"✅ KG sentences written to: {OUTPUT_PATH}")
    print(f"📊 Total KG sentences: {len(sentences)}")


if __name__ == "__main__":
    main()
