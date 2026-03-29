import streamlit as st
from document_loader import load_documents
from embed_documents import split_text
from chromadb import Client  # if using ChromaDB
from chromadb.config import Settings

# -----------------------------
# SETUP VECTOR DATABASE
# -----------------------------
# Initialize Chroma client (or your DB of choice)
client = Client(Settings(
    chroma_db_impl="duckdb+parquet",  # local storage
    persist_directory="./db"           # where your DB will be saved
))

# Define a collection for your documents
collection_name = "knowledge_collection"

# Check if the collection exists, else create
if collection_name in [c.name for c in client.list_collections()]:
    collection = client.get_collection(name=collection_name)
else:
    collection = client.create_collection(name=collection_name)

# -----------------------------
# BUILD DATABASE (FOR CLOUD) ✅
# -----------------------------
if "db_loaded" not in st.session_state:

    # Check if collection already has data
    existing_data = collection.count()

    if existing_data == 0:
        st.write("🔄 Loading and embedding documents...")

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

        st.write("✅ Documents loaded successfully!")

    else:
        st.write("✅ Database already initialized")

    st.session_state.db_loaded = True