import json
import os


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_relations(main_relations_file, email_relations_file,email_entity_relations, output_file):
    main_relations = load_json(main_relations_file)
    email_relations = load_json(email_relations_file)
    email_entity_relations = load_json(email_entity_relations)

    if not isinstance(main_relations, list):
        main_relations = [main_relations]

    if not isinstance(email_relations, list):
        email_relations = [email_relations]

    if not isinstance(email_entity_relations, list):
        email_entity_relations = [email_entity_relations]

    merged = main_relations + email_relations + email_entity_relations

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4)

    print(f"Final relations written to: {output_file}")
    print(f"Total relations: {len(merged)}")


if __name__ == "__main__":

    merge_relations(
        "C:\\Users\\aquib\\Infosys_project\\relations.json",
        "C:\\Users\\aquib\\Infosys_project\\email_relations.json",
        "C:\\Users\\aquib\\Infosys_project\\email_entity_relations.json",
        "C:\\Users\\aquib\\Infosys_project\\relationship_extraction_all123.json"
    )
