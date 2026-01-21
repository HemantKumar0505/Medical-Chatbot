import os
from dotenv import load_dotenv
from google.genai import Client

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client = Client(api_key=api_key)


def generate_medical_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Depending on the model, either works:
        if hasattr(response, "output_text"):
            return response.output_text
        return response.text

    except Exception as e:
        return f"[ERROR] {e}"


if __name__ == "__main__":
    print(generate_medical_response("Explain fever in 3 lines."))
