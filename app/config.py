from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URL')



class Config(BaseSettings):
    sqla_engine: str = DATABASE_URL
    mongo_uri: str = "mongodb://127.0.0.1:27017/demo"
    mongo_host: str = "mongodb://127.0.0.1:27017/"
    mongo_db: str = "demo"
    upload_dir: str = "upload/"
    secret: str = "123456789"
    gtag: Optional[str] = None


config = Config()
