
import json
import pdfplumber

def ingest_pdf(pdf_file):
    """
    Ingests an unstructured PDF and returns a JSON-like dict.
    """

    full_text = []
    page_count = 0

    with pdfplumber.open(pdf_file) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    document = {
        "source_type": "unstructured",
        "source_domain": "pdf",
        "source_file": pdf_file,
        "metadata": {
            "page_count": page_count
        },
        "content": "\n".join(full_text)
    }

    return document

pdf_json = ingest_pdf("Data\\Unstructured_Data\\US federal Reserve Policy.pdf")
with open("US federal Reserve Policy.json", "w", encoding="utf-8") as f:
    json.dump(pdf_json, f, indent=4)