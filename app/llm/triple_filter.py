BAD_OBJECT_PATTERNS = [
    "no specific",
    "not mentioned",
    "various",
    "many",
    "several"
]

BAD_SINGLE_WORDS = {
    "entity",
    "company",
    "sector",
    "initiative",
    "deal"
}

VALID_TYPES = {
    "Company",
    "Technology",
    "Platform",
    "Sector",
    "Strategy",
    "Partnership",
    "Acquisition",
    "Capability"
}

import re


def is_bad_object(obj: str) -> bool:

    if not obj:
        return True

    obj_lower = obj.lower().strip()

    if len(obj_lower) < 4:
        return True

    if len(obj_lower.split()) > 8:
        return True

    if obj_lower in BAD_SINGLE_WORDS:
        return True

    for pattern in BAD_OBJECT_PATTERNS:
        if pattern in obj_lower:
            return True

    if re.fullmatch(r"\d+[%]?", obj_lower):
        return True

    return False


# ⭐⭐⭐ THIS is what your pipeline is trying to import
def filter_triples(triples):

    if not triples:
        return []

    filtered = []

    for t in triples:

        subject = t.get("subject")
        predicate = t.get("predicate")
        obj = t.get("object")
        confidence = t.get("confidence", 1)
        obj_type = t.get("object_type")

        # Confidence gate
        if confidence < 0.6:
            continue

        if not subject or not predicate or not obj:
            continue

        if is_bad_object(obj):
            continue

        # Optional but VERY powerful
        if obj_type and obj_type not in VALID_TYPES:
            continue

        filtered.append(t)

    return filtered
