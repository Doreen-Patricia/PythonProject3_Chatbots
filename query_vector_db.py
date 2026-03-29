import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(name="knowledge_base")

while True:
    query = input("\nAsk a question (or type 'exit'): ")

    if query.lower() == "exit":
        break

    # Convert question to embedding
    query_embedding = model.encode(query).tolist()

    # Search database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_docs = results["documents"][0]

    print("\nAnswer based on uploaded files:\n")

    for doc in retrieved_docs:
        print(doc)
        print()