import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
PERSIST_DIR = "vectorstore"

def build_store():
    docs = []
    for fname in os.listdir(DATA_DIR):
        if fname.lower().endswith(".pdf"):
            path = os.path.join(DATA_DIR, fname)
            loader = PyPDFLoader(path)
            pages = loader.load()
            for i, d in enumerate(pages):
                d.metadata["source"] = fname
                d.metadata["page"] = d.metadata.get("page", i + 1)
                # Opsional: tebak subject/topic dari nama file/folder
            docs.extend(pages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    vs = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=PERSIST_DIR)
    vs.persist()
    print(f"Indexed {len(chunks)} chunks ke Chroma ({PERSIST_DIR})")

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PERSIST_DIR, exist_ok=True)
    build_store()
