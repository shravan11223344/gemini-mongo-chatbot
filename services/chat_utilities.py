from llm_factory.get_llm import get_gemini_model

def get_answer(model_name, chat_history):
    model = get_gemini_model()

    # Build conversation string
    conversation = ""
    for msg in chat_history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Generate response using Gemini
    response = model.models.generate_content(
        model=model_name,
        contents=conversation
    )

    return response.text