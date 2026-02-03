# import json
# import pdfplumber

# def pdf_to_json(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"

#     return {
#         "source_type": "unstructured",
#         "source_file": pdf_path,
#         "content": text.strip()
#     }

# pdf_json = pdf_to_json("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\2024_Annual_Report-Microsoft.pdf")

# with open("annual_report_2024.json", "w", encoding="utf-8") as f:
#     json.dump(pdf_json, f, indent=4)


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

pdf_json = ingest_pdf("C:\\Users\\aquib\\Infosys_project\\Data\\Unstructured_Data\\US federal Reserve Policy.pdf")
with open("US federal Reserve Policy.json", "w", encoding="utf-8") as f:
    json.dump(pdf_json, f, indent=4)