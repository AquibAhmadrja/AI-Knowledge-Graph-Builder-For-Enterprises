import pandas as pd
import json

df = pd.read_csv("C:\\Users\\aquib\\Infosys_project\\Data\\semistructured_data\\Wholesale customers data.csv")   

json_data = []
for _, row in df.iterrows():
    cleaned = {k: v for k, v in row.items() if pd.notna(v)}

    json_data.append({
        "source_type": "semi_structured",
        "source_file": "Wholesale customers data.csv",
        "data": cleaned
    })

with open("Wholesale customers data.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)
