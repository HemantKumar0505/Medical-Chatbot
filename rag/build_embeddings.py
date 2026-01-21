import json
import os
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # medical_chatbot/
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
DATA_FILE = os.path.join(os.path.dirname(__file__), "dataset", "diseases.json")
DB_DIR = os.path.join(os.path.dirname(__file__), "embeddings")


def load_dataset():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Dataset file not found at: {DATA_FILE}")
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def build_text(entry):
    return (
        f"Condition: {entry['condition']}\n"
        f"Symptoms: {', '.join(entry['symptoms'])}\n"
        f"Causes: {', '.join(entry['causes'])}\n"
        f"Risk Factors: {', '.join(entry['risk_factors'])}\n"
        f"Emergency Signs: {', '.join(entry['emergency_signs'])}\n"
        f"When to See Doctor: {', '.join(entry['when_to_see_doctor'])}\n"
        f"Self Care: {', '.join(entry['self_care'])}\n"
        f"Source: {entry['source']}"
    )


def embed_dataset():
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env"
        )

    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    data = load_dataset()
    texts = [build_text(entry) for entry in data]
    metadatas = [{"condition": entry["condition"]} for entry in data]

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        api_key=api_key
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=DB_DIR
    )

    vectorstore.persist()
    print("Embedding build completed successfully!")


if __name__ == "__main__":
    embed_dataset()
