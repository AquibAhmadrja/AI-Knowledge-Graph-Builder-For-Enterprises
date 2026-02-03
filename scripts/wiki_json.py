import json

def ingest_text_file(text_file):
    """
    Ingests an unstructured text file (wiki, articles, notes)
    and returns a JSON-like dict.
    """
    with open(text_file, encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    document = {
        "source_type": "unstructured",
        "source_domain": "wiki_text",
        "source_file": text_file,
        "metadata": {},
        "content": content
    }

    return document


wiki_json = ingest_text_file(
    "C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\wikidata_index.txt"
)

with open("wiki_text.json", "w", encoding="utf-8") as f:
    json.dump(wiki_json, f, indent=4)
