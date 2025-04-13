# app/config.py
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("postgresql://neondb_owner:npg_d9JMeauYP4Oj@ep-damp-unit-a59836nl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
    LLAMA_MODEL_PATH: str = os.getenv("LLAMA_MODEL_PATH")  ##LLAMA MODEL LOCATION
    SECRET_KEY: str = os.getenv("SECRET_KEY")   ##USe JK_GEN_bookmanagement' for this currenlty
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()

# Example .env file:
# DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
# LLAMA_MODEL_PATH=/path/to/your/llama/model
# SECRET_KEY=your_secret_key
