# llm_factory/get_llm.py
from google.genai import Client
from db.mongo import settings

def get_gemini_model():
    """
    Returns a google-genai Client instance connected with your GEMINI_API_KEY
    """
    client = Client(api_key=settings.GEMINI_API_KEY)
    return client