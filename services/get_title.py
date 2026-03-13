from llm_factory.get_llm import get_gemini_model

def get_chat_title(model, user_query):

    llm = get_gemini_model()

    prompt = f"""
Create a short title (max 7 words) for this query:

{user_query}

Title:
"""

    response = llm.generate_content(prompt)

    return response.text.strip()