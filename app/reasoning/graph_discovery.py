from app.graph.neo4j_client import get_session


def graph_discovery_search(intent_data, limit=60):

    focus = intent_data.get("focus_area", "")

    cypher = """
    MATCH (c:Entity)-[r]->(o:Entity)
    WHERE
        toLower(o.name) CONTAINS toLower($focus)
        OR
        toLower(type(r)) CONTAINS toLower($focus)

    RETURN
        c.name AS company,
        type(r) AS relation,
        o.name AS object
    LIMIT $limit
    """

    with get_session() as session:

        result = session.run(
            cypher,
            focus=focus,
            limit=limit
        )

        return [dict(r) for r in result]
