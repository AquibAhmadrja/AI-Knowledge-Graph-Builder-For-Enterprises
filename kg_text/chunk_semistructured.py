import json
import uuid
import re
from collections import defaultdict
from pathlib import Path

# ---------- CONFIG ----------
INPUT_TEXT_FILE = "semistructured_triples.txt"
OUTPUT_JSON_FILE = "semi_chunks.json"

SOURCE_TYPE = "TXT"
MAX_SENTENCES_PER_CHUNK = 5
DEFAULT_ENTITY_PREFIX = "Employee"
# ----------------------------

LINE_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<entity>[A-Za-z_0-9\-]+|\d+)
    \s+has\s+
    (?P<predicate>[A-Za-z_]+)
    \s+
    (?P<value>.+?)
    \.\s*$
    """,
    re.IGNORECASE | re.VERBOSE
)

def normalize_entity(entity: str):
    if entity.isdigit():
        return f"{DEFAULT_ENTITY_PREFIX}_{entity}"
    return entity

def parse_line(line: str):
    match = LINE_PATTERN.match(line)
    if not match:
        return None, None, None

    entity = normalize_entity(match.group("entity"))
    predicate = match.group("predicate")
    value = match.group("value")

    normalized_sentence = f"{entity} has {predicate} {value}."
    return entity, predicate, normalized_sentence

def entity_predicate_aware_chunking(input_file, output_file):
    doc_id = str(uuid.uuid4())
    grouped = defaultdict(list)

    total_lines = 0
    parsed_lines = 0

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue

            entity, predicate, normalized_sentence = parse_line(line)
            if not entity:
                continue

            parsed_lines += 1
            grouped[(entity, predicate)].append(normalized_sentence)

    if parsed_lines == 0:
        raise RuntimeError(
            "❌ Parsed 0 lines. Check input format. "
            "Example expected: 'Employee_101 has salary 90000.'"
        )

    chunks = []
    chunk_counter = 0

    for (entity, predicate), sentences in grouped.items():
        for i in range(0, len(sentences), MAX_SENTENCES_PER_CHUNK):
            sub = sentences[i:i + MAX_SENTENCES_PER_CHUNK]

            chunks.append({
                "chunk_id": f"{Path(input_file).stem}_{doc_id}_chunk_{chunk_counter}",
                "text": " ".join(sub),
                "source": SOURCE_TYPE,
                "doc_id": doc_id,
                "source_file": str(Path(input_file).resolve())
            })
            chunk_counter += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Parsed {parsed_lines}/{total_lines} lines")
    print(f"✅ Stored {len(chunks)} normalized semantic chunks")
    print(f"📄 doc_id = {doc_id}")


if __name__ == "__main__":
    entity_predicate_aware_chunking(INPUT_TEXT_FILE, OUTPUT_JSON_FILE)
