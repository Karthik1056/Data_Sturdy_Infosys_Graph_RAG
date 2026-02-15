from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

with driver.session() as session:
    result = session.run("RETURN 'Neo4j Connected!' AS message")
    
    for record in result:
        print(record["message"])
