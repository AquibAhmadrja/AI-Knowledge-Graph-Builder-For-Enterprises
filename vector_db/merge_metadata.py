# -------- CONFIG --------
MAIN_METADATA = "vector_db\\metadata_with_text.json"
KG_METADATA = "kg_text\\metadata_semi_with_text.json"

FINAL_METADATA = "vector_db\\metadata_final.json"
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


