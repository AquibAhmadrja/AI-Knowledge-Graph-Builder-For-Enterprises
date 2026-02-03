import json
from collections import Counter

with open("C:\\Users\\aquib\\Infosys_project\\all_entity_docs.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

domains = Counter(doc.get("source_domain") for doc in docs)
print(domains)

