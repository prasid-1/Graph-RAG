from src.createGraph import create_graph
from src import fullTextIndexQuery
from src.embeddings import neo4jInit


# add NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD to .env before running

def main():

    # create_graph(docChunkSize=500, docChunkOverlap=24, ProcessInChunks=True, graphChunkSize=10, file_path="documents/BuildingCode.pdf")
    result = fullTextIndexQuery.graph_retriever("What are the codes and standards related to fire safety?")
    print("Graph Retriever Result:")
    print(result)



if __name__ == "__main__":
    main()