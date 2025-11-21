import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from prompts import SOLVE_SYS, GEN_SYS

PERSIST_DIR = "vectorstore"

def get_retriever():
    emb = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    vs = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
    return vs.as_retriever(search_kwargs={"k": 5})

def get_llm(temperature=0.2):
    return ChatOpenAI(
        model=os.getenv("CHAT_MODEL", "openrouter/auto"),
        temperature=temperature
        # OPENAI_API_KEY & OPENAI_API_BASE diambil dari ENV (OpenRouter)
    )

def format_context(docs):
    parts = []
    for d in docs:
        src = d.metadata.get("source")
        pg = d.metadata.get("page")
        parts.append(f"[{src} p.{pg}] {d.page_content}")
    return "\n\n---\n\n".join(parts)

def solve_question(query, retriever, llm):
    docs = retriever.invoke(query)        # <- ganti ke invoke
    context = format_context(docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SOLVE_SYS),
        ("user", f"[SOAL]: {query}\n\n[KONTEKS]:\n{context}")
    ])
    return llm.invoke(prompt.format_messages()).content, docs

def generate_item(topic_query, retriever, llm):
    docs = retriever.invoke(topic_query)  # <- ganti ke invoke
    context = format_context(docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", GEN_SYS),
        ("user", f"Topik: {topic_query}\n\n[KONTEKS]:\n{context}")
    ])
    return llm.invoke(prompt.format_messages()).content, docs

