import pandas as pd
import json

excel = pd.ExcelFile("Data\\semistructured_data\\issues_snapshot_sample.xlsx")
json_data = []

for sheet in excel.sheet_names:
    df = excel.parse(sheet)
    df = df.dropna(how="all")

    for _, row in df.iterrows():
        json_data.append({
            "source_type": "semi_structured",
            "source_file": "issues_snapshot_sample.xlsx",
            "sheet_name": sheet,
            "data": row.to_dict()
        })

with open("issues_snapshot_sample.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)
