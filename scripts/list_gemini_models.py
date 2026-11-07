"""List the Gemini models your API key can use (helps choose GEMINI_SQL_MODEL)."""
import os

from dotenv import load_dotenv
from google import genai

if __name__ == "__main__":
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    for model in client.models.list():
        print(model.name)
