# GraphRAG (Graph Retrieval-Augmented Generation)

✅ **Purpose:** GraphRAG builds a small end-to-end example that converts documents into a Neo4j knowledge graph and allows retrieval using graph-aware queries. It demonstrates how to:

- Chunk and embed documents
- Create graph nodes/relationships in Neo4j
- Query the graph for relevant information

---

## 🔧 Quick Start

Prerequisites:

- Python 3.10+
- A running Neo4j instance (local or cloud)
- Optional: virtualenv or conda for isolated environment

1. Clone the repo

```bash
git clone <repo-url>
cd GraphRAG_langchain
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add Neo4j credentials to a `.env` file in the project root:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-password>
```

4. Run the example

```bash
python main.py
```

This will call the graph retriever in `src/fullTextIndexQuery.py` and print results to the console.

---

## 📁 Project Structure

- `main.py` — sample script that executes a graph retrieval
- `src/` — main source code
  - `createGraph.py` — functions to build graph from documents
  - `fullTextIndexQuery.py` — graph retriever and query helpers
  - `queryNeo4j.py` — lower-level Neo4j queries
  - `embeddings/neo4jInit.py` — Neo4j driver and initialization helpers
- `documents/` — add PDF or text documents here to be processed

---

## ⚙️ Usage Tips

- To create the graph from a document, call `create_graph()` from `src/createGraph.py` with appropriate chunk sizes. Example (inside `main.py`):

```py
# create_graph(docChunkSize=500, docChunkOverlap=24, ProcessInChunks=True, graphChunkSize=10, file_path="documents/BuildingCode.pdf")
```

- To query the graph, use `fullTextIndexQuery.graph_retriever(<query_string>)` as shown in `main.py`.

---

## 🚨 Troubleshooting

- Connection errors: verify `.env` values and that Neo4j is running and accessible.
- Missing dependencies: re-run `pip install -r requirements.txt`.
- Empty results: ensure documents were processed into the graph by running `create_graph()` first.

---

## Contributing

Contributions are welcome. Please open issues or pull requests describing the change.

---

## License

Add your license here (e.g., MIT) or remove this section if you prefer a different license.

---

If you want, I can also add examples, screenshots, or expand the Troubleshooting and Development sections — tell me what to include. ✨
