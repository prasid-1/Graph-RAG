from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Neo4jVector
from neo4j import GraphDatabase
import os

def main():
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large:335m",
    )

    vector_index = Neo4jVector.from_existing_graph(
        embeddings,
        search_type="hybrid",
        node_label="Document",
        text_node_properties=["text"],
        embedding_node_property="embedding"
    )
    vector_retriever = vector_index.as_retriever()
    driver = GraphDatabase.driver(
        uri = os.environ["NEO4J_URI"],
        auth = (os.environ["NEO4J_USERNAME"],
                os.environ["NEO4J_PASSWORD"]))

    def create_fulltext_index(tx):
        query = '''
        CREATE FULLTEXT INDEX `fulltext_entity_id` 
        IF NOT EXISTS
        FOR (n:__Entity__) 
        ON EACH [n.id];
        '''
        tx.run(query)

    # Function to execute the query
    def create_index():
        with driver.session() as session:
            session.execute_write(create_fulltext_index)
            print("Fulltext index created successfully.")

    # Call the function to create the index
    try:
        create_index()
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the driver connection
    driver.close()

if __name__ == "__main__":
    main()