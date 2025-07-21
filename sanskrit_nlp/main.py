from neo4j import GraphDatabase

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_node(self, label, properties):
        with self._driver.session() as session:
            session.write_transaction(self._create_node, label, properties)

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} $props)"
        tx.run(query, props=properties)

    def add_relationship(self, from_node_label, from_node_props, to_node_label, to_node_props, rel_type):
        with self._driver.session() as session:
            session.write_transaction(self._create_relationship, from_node_label, from_node_props, to_node_label, to_node_props, rel_type)

    @staticmethod
    def _create_relationship(tx, from_node_label, from_node_props, to_node_label, to_node_props, rel_type):
        query = f"""
        MATCH (a:{from_node_label}), (b:{to_node_label})
        WHERE a.name = $from_name AND b.name = $to_name
        CREATE (a)-[r:{rel_type}]->(b)
        """
        tx.run(query, from_name=from_node_props['name'], to_name=to_node_props['name'])


if __name__ == '__main__':
    # This is a placeholder for where the NLP pipeline and graph database will be integrated.
    # For now, it just demonstrates the basic functionality of the KnowledgeGraph class.
    print("Knowledge Graph module is ready. Integration with NLP pipeline is the next step.")
