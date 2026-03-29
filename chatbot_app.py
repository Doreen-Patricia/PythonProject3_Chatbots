from turtle import st

from document_loader import load_documents
from embed_documents import split_text, collection

# -----------------------------
# BUILD DATABASE (FOR CLOUD)
# -----------------------------
if "db_loaded" not in st.session_state:
    documents = load_documents("knowledge_documents")

    chunks = []
    ids = []

    for i, doc in enumerate(documents):
        for j, chunk in enumerate(split_text(doc)):
            chunks.append(chunk)
            ids.append(f"{i}_{j}")

    if len(chunks) > 0:
        collection.add(
            documents=chunks,
            ids=ids
        )

    st.session_state.db_loaded = True
