import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/stocks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
