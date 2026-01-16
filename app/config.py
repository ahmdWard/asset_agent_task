import os
from dotenv import load_dotenv

load_dotenv()

class get_settings:
    DATABASE_URL:str = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = "Asset Management API"
    API_V1_PREFIX: str = "/api/v1"
    OPEN_API_KEY:str = os.getenv("OPEN_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True
 

settings = get_settings()

