import os
import streamlit as st
from document_loader import load_documents
from embed_documents import split_text
from chromadb import Client

# Ensure DB folder exists
if not os.path.exists("./db"):
    os.makedirs("./db")

# Initialize Chroma client
client = Client(persist_directory="./db", settings={})

# Define collection
collection_name = "knowledge_collection"
if collection_name in [c.name for c in client.list_collections()]:
    collection = client.get_collection(name=collection_name)
else:
    collection = client.create_collection(name=collection_name)

# -----------------------------
# BUILD DATABASE
# -----------------------------
if "db_loaded" not in st.session_state:

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