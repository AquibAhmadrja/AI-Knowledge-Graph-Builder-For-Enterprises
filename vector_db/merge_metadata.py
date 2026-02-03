# -------- CONFIG --------
MAIN_METADATA = "C:\\Users\\aquib\\Infosys_project\\vector_db\\metadata_with_text.json"
KG_METADATA = "C:\\Users\\aquib\\Infosys_project\\kg_text\\metadata_semi_with_text.json"

FINAL_METADATA = "C:\\Users\\aquib\\Infosys_project\\vector_db\\metadata_final.json"
# -----------------------


def main():
    with open(FINAL_METADATA, "w", encoding="utf-8") as out:
        # 🔹 First: main metadata
        with open(MAIN_METADATA, "r", encoding="utf-8") as f:
            for line in f:
                out.write(line)

        # 🔹 Second: KG metadata
        with open(KG_METADATA, "r", encoding="utf-8") as f:
            for line in f:
                out.write(line)

    print("✅ Metadata merge completed")
    print(f"📁 Final metadata saved to: {FINAL_METADATA}")


if __name__ == "__main__":
    main()


