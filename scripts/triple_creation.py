import json


def create_triples(relations):
    """
    Convert relation objects into KG triples
    """
    triples = []

    for rel in relations:
        subject = rel.get("subject")
        predicate = rel.get("predicate")
        obj = rel.get("object")

        # basic validation
        if not subject or not predicate or not obj:
            continue

        triples.append({
            "head": subject,
            "relation": predicate,
            "tail": obj,
            "doc_id": rel.get("doc_id")
        })

    return triples


def deduplicate_triples(triples):
    """
    Remove duplicate triples
    """
    seen = set()
    unique_triples = []

    for t in triples:
        key = (t["head"], t["relation"], t["tail"])
        if key not in seen:
            seen.add(key)
            unique_triples.append(t)

    return unique_triples



if __name__ == "__main__":

    with open("C:\\Users\\aquib\\Infosys_project\\relationship_extraction_all123.json", "r", encoding="utf-8") as f:
        relations = json.load(f)

    triples = create_triples(relations)
    triples = deduplicate_triples(triples)

    with open("triples_all.json", "w", encoding="utf-8") as f:
        json.dump(triples, f, indent=4)

    print(f"Created {len(triples)} unique triples")
