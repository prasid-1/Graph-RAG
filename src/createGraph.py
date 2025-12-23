
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()


def create_graph(docChunkSize: int= 250, docChunkOverlap: int = 24, ProcessInChunks: bool = False, graphChunkSize: int = 10, file_path: str = "documents/BuildingCode.pdf"):
    graph = Neo4jGraph()

    # Load PDF and split into chunks
    loader = PyPDFLoader(file_path=file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=docChunkSize, chunk_overlap=docChunkOverlap)
    documents = text_splitter.split_documents(documents=docs)
    print(f"Number of documents: {len(documents)}")
    docSize = len(documents)

    # Initialize OllamaFunctions LLM
    llm = OllamaFunctions(model="llama3.1:8b", temperature=0, format="json")

    llm_transformer = LLMGraphTransformer(llm=llm)

    # Process documents in chunks if specified
    if ProcessInChunks:
        for i in range(0, docSize, graphChunkSize):
            chunk = documents[i:min(i + graphChunkSize, docSize)]
            print(f"Processing chunk {i // graphChunkSize + 1}: documents {i} to {min(i + graphChunkSize, docSize) - 1}")

            try:
                graph_documents = llm_transformer.convert_to_graph_documents(chunk)

                graph.add_graph_documents(
                    graph_documents,
                    baseEntityLabel=True,
                    include_source=True
                )
            except Exception as e:
                print(f"Error processing chunk {i // graphChunkSize + 1}: {e}")
    
    # Process all documents at once if not in chunks
    if not ProcessInChunks:
        try:
            graph_documents = llm_transformer.convert_to_graph_documents(documents)

            graph.add_graph_documents(
                graph_documents,
                baseEntityLabel=True,
                include_source=True
            )
        except Exception as e:
            print(f"Error processing documents: {e}")


if __name__ == "__main__":
    create_graph()