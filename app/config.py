import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key' # Replace with a real secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
