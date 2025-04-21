from typing import Optional

from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URL')
ASYNC_DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')



class Config(BaseSettings):
    sqla_engine: str = DATABASE_URL
    async_sqla_engine: str = ASYNC_DATABASE_URL
    mongo_uri: str = "mongodb://127.0.0.1:27017/demo"
    mongo_host: str = "mongodb://127.0.0.1:27017/"
    mongo_db: str = "demo"
    upload_dir: str = "upload/"
    secret: str = "123456789"
    gtag: Optional[str] = None


config = Config()
