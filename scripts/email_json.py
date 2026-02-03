# import csv
# import json
# import sys

# # Windows-safe increase of CSV field size limit
# max_int = sys.maxsize
# while True:
#     try:
#         csv.field_size_limit(max_int)
#         break
#     except OverflowError:
#         max_int = int(max_int / 10)

# def enron_csv_to_json(csv_file):
#     documents = []

#     with open(csv_file, newline="", encoding="utf-8", errors="ignore") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             documents.append({
#                 "source_type": "unstructured",
#                 "source_domain": "email",
#                 "source_file": csv_file,
#                 "metadata": {
#                     "message_id": row.get("message_id"),
#                     "date": row.get("date"),
#                     "sender": row.get("from"),
#                     "receiver": row.get("to"),
#                     "subject": row.get("subject")
#                 },
#                 "content": row.get("body", "").strip()
#             })

#     return documents


# # usage
# emails_json = enron_csv_to_json("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\emails.csv")

# with open("emails.json", "w", encoding="utf-8") as f:
#     json.dump(emails_json, f, indent=4)


# import csv

# with open("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\emails.csv", newline="", encoding="utf-8", errors="ignore") as f:
#     reader = csv.reader(f)
#     headers = next(reader)
#     print(headers)




# import pandas as pd
# import json

# df = pd.read_csv("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\emails.csv")

# json_data = []
# for _, row in df.iterrows():
#     json_data.append({
#                 "source_type": "unstructured",
#                 "source_domain": "email",
#                 "source_file": "emails.csv",
#                 "metadata": {
#                     "message_id": row.get("message_id"),
#                     "date": row.get("date"),
#                     "sender": row.get("from"),
#                     "receiver": row.get("to"),
#                     "subject": row.get("subject")
#                 },
#                 "content": row.get("body", "").strip()
#             })

# with open("emails.json", "w", encoding="utf-8") as f:
#     json.dump(json_data, f, indent=4)


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
emails_json = ingest_enron_emails("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\emails.csv")
with open("emails.json", "w", encoding="utf-8") as f:
    json.dump(emails_json, f, indent=4)