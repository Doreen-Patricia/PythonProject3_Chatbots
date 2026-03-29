import chromadb
from sentence_transformers import SentenceTransformer
from document_loader import load_documents

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="knowledge_base")

# --------------------------------
# ADD split_text FUNCTION HERE
# --------------------------------
def split_text(text, chunk_size=800, overlap=150):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks

# -----------------------------
# LOAD DOCUMENTS
# -----------------------------
documents = load_documents("knowledge_documents")

# -----------------------------
# DEBUG PREVIEW (ADD HERE)
# -----------------------------
print("\nLoaded documents:")

for i, doc in enumerate(documents):
    print(f"\nDocument {i+1} preview:")
    print(doc[:200])

# --------------------------------
# REPLACE OLD EMBEDDING CODE
# ADD CHUNKING CODE HERE
# --------------------------------
chunks = []
ids = []
embeddings = []

for i, doc in enumerate(documents):
    split_chunks = split_text(doc)

    for j, chunk in enumerate(split_chunks):
        chunks.append(chunk)
        ids.append(f"{i}_{j}")
        embeddings.append(model.encode(chunk).tolist())

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)

print("Documents successfully embedded.")