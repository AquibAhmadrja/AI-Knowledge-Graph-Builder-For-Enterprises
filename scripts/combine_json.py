import os
import json

def combine_entity_files(input_folder, output_file):
    combined = []

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # must be a file AND must end with .json
        if not (os.path.isfile(file_path) and filename.endswith(".json")):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    combined.extend(data)
                else:
                    combined.append(data)

            print(f"Loaded: {filename}")

        except Exception as e:
            print(f" Skipped {filename} → {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)

    print(f"\nCombined {len(combined)} documents into {output_file}")


# ---------------- USAGE ----------------
combine_entity_files(
    r"Entity_Enriched_Data",
    r"all_entity_docs_1.json"
)
