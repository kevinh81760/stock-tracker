import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db", "stocks.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
