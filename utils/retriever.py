import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

DB_DIR = os.path.join(BASE_DIR, "rag", "embeddings")

def get_retriever(top_k=3):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        api_key=api_key
    )

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )

    # modern retriever setup
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    return retriever


def retrieve_conditions(query, top_k=3):
    retriever = get_retriever(top_k)
    docs = retriever.invoke(query)   # <-- updated API

    results = [
        {
            "condition": doc.metadata.get("condition", "unknown"),
            "content": doc.page_content
        }
        for doc in docs
    ]

    return results


if __name__ == "__main__":
    print("Test Query: 'fever with rash'")
    test = retrieve_conditions("fever with rash")
    print(test)
