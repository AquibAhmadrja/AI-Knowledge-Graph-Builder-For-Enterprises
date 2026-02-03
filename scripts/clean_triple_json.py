import re

INPUT_FILE = r"triples_all.json"
OUTPUT_FILE = r"triples_all_clean.json"

# Regex to remove illegal control characters
CONTROL_CHAR_RE = re.compile(
    r'[\x00-\x08\x0B\x0C\x0E-\x1F]'
)

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    raw = f.read()

cleaned = CONTROL_CHAR_RE.sub("", raw)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Cleaned JSON written to:", OUTPUT_FILE)

