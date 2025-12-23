from src import queryNeo4j
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from dotenv import load_dotenv
from src.embeddings import neo4jInit

load_dotenv()
graph = Neo4jGraph()

def generate_full_text_query(input: str) -> str:
    words = [el for el in remove_lucene_chars(input).split() if el]
    if not words:
        return ""
    full_text_query = " AND ".join([f"{word}~2" for word in words])
    print(f"Generated Query: {full_text_query}")
    return full_text_query.strip()


# Fulltext index query
def graph_retriever(question: str) -> str:
    """
    Collects the neighborhood of entities mentioned
    in the question
    """
    neo4jInit.main()
    result = ""
    entity_chain, prompt = queryNeo4j.main()
    entities = entity_chain.invoke(question)
    for entity in entities.names:
        lucene_query = generate_full_text_query(entity)
        if not lucene_query:
            continue
        response = graph.query(
             """
                CALL db.index.fulltext.queryNodes('fulltext_entity_id', $query, {limit: 2})
                YIELD node, score

                CALL (node) {
                MATCH (node)-[r]->(neighbor)
                RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output

                UNION ALL

                MATCH (node)<-[r]-(neighbor)
                RETURN neighbor.id + ' - ' + type(r) + ' -> ' + node.id AS output
                }

                RETURN output
                LIMIT 50
                """,
                {"query": lucene_query},
        )
        result += "\n".join([el['output'] for el in response])
    return result

if __name__ == "__main__":
    graph_retriever("What are the codes and standards related to fire safety?")