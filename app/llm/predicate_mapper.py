PREDICATE_MAP = {

    "USES": "USES_TECH",
    "LEVERAGES": "USES_TECH",
    "UTILIZES": "USES_TECH",

    "PARTNERED_WITH": "PARTNERS_WITH",
    "COLLABORATES_WITH": "PARTNERS_WITH",

    "COMPETES": "COMPETES_WITH"
}


def normalize_predicate(pred):

    pred = pred.upper().replace(" ", "_")

    return PREDICATE_MAP.get(pred, pred)
