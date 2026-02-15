# # from app.graph.neo4j_client import get_session


# # def get_company_context(companies, limit=80):

# #     cypher = """
# #     MATCH (c:Entity)-[r]->(o:Entity)
# #     WHERE c.name IN $companies

# #     RETURN
# #         c.name AS company,
# #         type(r) AS relation,
# #         o.name AS object
# #     LIMIT $limit
# #     """

# #     with get_session() as session:

# #         result = session.run(
# #             cypher,
# #             companies=companies,
# #             limit=limit
# #         )

# #         return [dict(r) for r in result]


from app.graph.neo4j_client import get_session
def retrieve_graph_context():

    query = """
        MATCH (a)-[r]->(b)
    WHERE size(a.name) > 2 AND size(b.name) > 2
    RETURN a.name AS subject,
        type(r) AS predicate,
        b.name AS object
    """

    context_lines = []

    with get_session() as session:

        result = session.run(query)

        for record in result:

            context_lines.append(
                f"{record['subject']} {record['predicate']} {record['object']}"
            )

    return "\n".join(context_lines) if context_lines else ""



# from app.graph.neo4j_client import get_session


# def retrieve_graph_context():

#     query = """
#     MATCH (a:Entity)-[r]->(b:Entity)

#     WHERE
#         a.name IS NOT NULL
#         AND b.name IS NOT NULL
#         AND size(a.name) > 2
#         AND size(b.name) > 2

#     RETURN
#         a.name AS subject,
#         type(r) AS predicate,
#         b.name AS object
#     """

#     with get_session() as session:

#         result = session.run(query)

#         triples = [dict(record) for record in result]

#     return triples
