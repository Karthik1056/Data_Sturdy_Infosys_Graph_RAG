from neo4j import GraphDatabase
from app.config import (
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)

# Create ONE global driver
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def get_session():
    return driver.session()


def close_driver():
    driver.close()
