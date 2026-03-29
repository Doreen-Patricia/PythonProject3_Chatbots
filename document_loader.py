from pypdf import PdfReader
from docx import Document
import os
import requests
from bs4 import BeautifulSoup


# -----------------------------
# LOAD TEXT FROM WEB URL ✅
# -----------------------------
def load_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract only paragraph text (cleaner)
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text.strip()

    except Exception as e:
        print(f"Error loading {url}: {e}")
        return ""


# -----------------------------
# ADD YOUR WEB LINKS HERE ✅
# -----------------------------
web_links = [
    "https://www.canada.ca/en/employment-social-development/programs/accessible-canada.html",
    "https://www.canada.ca/en/services/jobs/workplace/disability-inclusion.html",
    "https://www.inclusioncanada.ca/our-work/employment",
    "https://theinclusiveworkplace.ca/en/articles/inclusive-hiring-works",
    "https://laws-lois.justice.gc.ca/eng/acts/h-6/",
    "https://www.canada.ca/en/services/jobs/workplace/human-rights.html",
    "https://laws-lois.justice.gc.ca/eng/",
    "https://www.supportedemployment.ca/",
    "https://accessible.canada.ca/"

]


# -----------------------------
# LOAD DOCUMENTS (FILES + WEB) ✅
# -----------------------------
def load_documents(folder_path):
    documents = []

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        # -----------------------------
        # TEXT FILES
        # -----------------------------
        if file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    documents.append(text)

        # -----------------------------
        # PDF FILES
        # -----------------------------
        elif file.endswith(".pdf"):
            try:
                reader = PdfReader(file_path)
                text = ""

                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

                if text.strip():
                    documents.append(text)

            except Exception as e:
                print(f"Error reading PDF {file}: {e}")

        # -----------------------------
        # DOCX FILES
        # -----------------------------
        elif file.endswith(".docx"):
            try:
                doc = Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])

                if text.strip():
                    documents.append(text)

            except Exception as e:
                print(f"Error reading DOCX {file}: {e}")

    # -----------------------------
    # LOAD WEB DATA ✅
    # -----------------------------
    for url in web_links:
        print(f"Loading web data from: {url}")
        web_text = load_webpage(url)

        if web_text:
            documents.append(web_text)

    return documents