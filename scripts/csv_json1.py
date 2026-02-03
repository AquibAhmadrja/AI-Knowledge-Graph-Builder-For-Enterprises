import pandas as pd
import json

df = pd.read_csv("C:\\Users\\aquib\\Infosys_project\\Data\\structured_data_large\\time_off.csv")

json_data = []
for _, row in df.iterrows():
    json_data.append({
        "source_type": "structured",
        "source_file": "time_off.csv",
        "data": row.to_dict()
    })

with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)



