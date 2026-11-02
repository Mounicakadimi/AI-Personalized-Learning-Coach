
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_json(prompt):
    """
    Sends a prompt to Gemini and returns a JSON response.
    """
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        return json.loads(response.text)

    except json.JSONDecodeError:
        raise ValueError("Gemini returned an invalid JSON response.")

    except Exception as error:
        raise RuntimeError(f"Gemini API error: {error}")
