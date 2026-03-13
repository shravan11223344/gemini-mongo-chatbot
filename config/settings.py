from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGO_DB_URI: str = "mongodb+srv://shettyshravan2004:Umeshshetty@cluster0.cmd8ljb.mongodb.net/"
    MONGO_DB_NAME: str = "chat_gpt"

    GEMINI_API_KEY: str = "AIzaSyBNtBJfxKyzOrgzqj1xsp-5KZd8am5RjrA"
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"