BAD_OBJECTS = {
    "company",
    "entity",
    "organization",
    "",
    None
}


def is_valid_triple(t):

    if not t.get("subject") or not t.get("object"):
        return False

    obj = t["object"].lower()

    if obj in BAD_OBJECTS:
        return False

    if len(obj) < 3:
        return False

    return True


def filter_triples(triples):
    return [t for t in triples if is_valid_triple(t)]
