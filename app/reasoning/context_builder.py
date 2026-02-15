def build_context(triples):

    if not triples:
        return "No graph knowledge found."

    lines = []

    for t in triples:
        lines.append(
            f"{t['company']} {t['relation']} {t['object']}"
        )

    return "\n".join(lines)
