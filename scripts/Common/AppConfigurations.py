import os
from dotenv import load_dotenv


load_dotenv()

class AppConfig:
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("CONTAINER_NAME")
    PORT = os.getenv("PORT", 8000)




class Services:
    static_images = 'static/images'

APP_CONFIG = AppConfig()