from config.settings import Settings

settings = Settings()

def get_ollama_model_list():
    return [settings.GEMINI_MODEL]