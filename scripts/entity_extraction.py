import spacy

nlp = spacy.load("en_core_web_sm")


def extract_entities_from_text(text):
    """
    Extract named entities from text using spaCy
    """
    entities = []

    if not text:
        return entities

    doc = nlp(text)

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })

    return entities
