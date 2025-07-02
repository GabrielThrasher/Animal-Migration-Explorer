import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("API_key")

client = genai.Client(
    api_key=API_key,
)


def answer_query(user_query):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=user_query
        ),
        contents="",)

    return response.text
