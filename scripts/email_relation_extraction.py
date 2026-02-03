import re
import json


def extract_email_headers(text):
    if not text:
        return {}

    patterns = {
        "sender": r"From:\s*(.*)",
        "receiver": r"To:\s*(.*)",
        "cc": r"Cc:\s*(.*)",
        "subject": r"Subject:\s*(.*)",
        "date": r"Date:\s*(.*)"
    }

    headers = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            headers[key] = match.group(1).strip()

    return headers


def extract_email_relations(docs):
    relations = []

    for doc in docs:
        headers = extract_email_headers(doc.get("text"))

        sender = headers.get("sender")
        receiver = headers.get("receiver")

        if sender and receiver:
            relations.append({
                "subject": sender,
                "predicate": "SENT_TO",
                "object": receiver,
                "doc_id": doc["doc_id"]
            })

    return relations


# ---------------- USAGE ----------------
if __name__ == "__main__":

    with open("Normalized_data\\normalized_emails.json", "r", encoding="utf-8") as f:
        normalized_email_docs = json.load(f)

    email_relations = extract_email_relations(normalized_email_docs)

    with open("email_relations.json", "w", encoding="utf-8") as f:
        json.dump(email_relations, f, indent=4)
