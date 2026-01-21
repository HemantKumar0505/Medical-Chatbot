import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "rag", "embeddings")


def get_retriever(top_k=3):
    # unified key logic
    api_key = (
        st.secrets.get("GEMINI_API_KEY")
        or st.secrets.get("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        api_key=api_key
    )

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_DIR,
        collection_name="medical_db"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    return retriever


def retrieve_conditions(query, top_k=3):
    retriever = get_retriever(top_k)
    docs = retriever.invoke(query)

    results = []
    for doc in docs:
        results.append({
            "condition": doc.metadata.get("condition", "unknown"),
            "content": doc.page_content
        })

    return results


if __name__ == "__main__":
    print("Test Query: 'fever with rash'")
    print(retrieve_conditions("fever with rash"))
