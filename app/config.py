import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "chatbot_secreto_123")
    APP_SECRET: str = os.getenv("APP_SECRET", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID", "")

settings = Settings()
