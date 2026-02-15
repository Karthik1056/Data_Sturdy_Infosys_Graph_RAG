# from app.graph.neo4j_client import get_session


# def write_triples_to_graph(triples):

#     if not triples:
#         return

#     with get_session() as session:

#         for t in triples:

#             if not t["subject"] or not t["object"]:
#                 continue

#             predicate = t["predicate"].upper().replace(" ", "_")

#             query = f"""
#             MERGE (s:Entity {{name:$subject}})
#             MERGE (o:Entity {{name:$object}})
#             MERGE (s)-[:{predicate}]->(o)
#             """

#             session.run(
#                 query,
#                 subject=t["subject"],
#                 object=t["object"]
#             )




from app.graph.neo4j_client import get_session
import re


def sanitize_predicate(predicate: str):

    if not predicate:
        return None

    predicate = predicate.upper()
    predicate = re.sub(r'[^A-Z0-9]', '_', predicate)
    predicate = re.sub(r'_+', '_', predicate)
    predicate = predicate.strip('_')

    return predicate[:30] if predicate else None


def write_triples_to_graph(triples):

    if not triples:
        return

    with get_session() as session:

        for t in triples:

            subject = t.get("subject")
            obj = t.get("object")
            raw_predicate = t.get("predicate")

            if not subject or not obj or not raw_predicate:
                continue

            predicate = sanitize_predicate(raw_predicate)

            # 🚨 Skip garbage predicates
            if not predicate or len(predicate) < 3:
                continue

            query = f"""
            MERGE (s:Entity {{name:$subject}})
            MERGE (o:Entity {{name:$object}})
            MERGE (s)-[:{predicate}]->(o)
            """

            session.run(
                query,
                subject=subject.strip(),
                object=obj.strip()
            )
