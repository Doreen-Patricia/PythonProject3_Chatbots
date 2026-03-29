import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD MODEL
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# CONNECT TO DATABASE
# -----------------------------
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="knowledge_base")

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📚 Enabled Talent Chatbot")

# -----------------------------
# STEP 1: INITIAL GREETING
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 My name is Study Buddies, Enabled Talent Assistant.\n\nI can help you with inclusive hiring, workplace accessibility, and disability employment guidelines.\n\nHow can I assist you today?"
        }
    ]

# -----------------------------
# STEP 2: DISPLAY CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# STEP 3: USER INPUT (IMPORTANT)
# -----------------------------
if prompt := st.chat_input("Ask a question about inclusive hiring..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # -----------------------------
    # STEP 4: QUERY VECTOR DATABASE
    # -----------------------------
    query_embedding = model.encode(prompt).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results["documents"][0]

    # -----------------------------
    # STEP 5: GENERATE RESPONSE
    # -----------------------------
    if docs:
        response = "Here is what I found from the documents:\n\n"

        for doc in docs:
            clean_doc = doc.strip().replace("\n", " ")

            response += "• " + clean_doc[:350] + "...\n\n"
    else:
        response = "Sorry, I could not find relevant information in the documents."

    # Save chatbot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response)