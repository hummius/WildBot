from typing import Optional, Dict, Any

from dotenv import load_dotenv, find_dotenv
import os

from pydantic.v1 import BaseSettings, PostgresDsn, validator
from sqlalchemy.engine import URL

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

DB_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=str(os.getenv('POSTGRES_USER')),
    password=str(os.getenv('POSTGRES_PASSWORD')),
    host=str(os.getenv('POSTGRES_HOST')),
    database=str(os.getenv('POSTGRES_DB')),
    port=os.getenv('POSTGRES_PORT'),
)


# class Settings(BaseSettings):
#     POSTGRES_HOST: str
#     POSTGRES_PORT: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DBNAME: str
#
#     BOT_TOKEN: str
#
#     SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn]
#
#     @validator('SQLALCHEMY_DATABASE_URL', pre=True)
#     def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
#         if isinstance(v, str):
#             return v
#         return PostgresDsn.build(
#             scheme='postgresql',
#             user=values.get('POSTGRES_USER'),
#             password=values.get('POSTGRES_PASSWORD'),
#             host=values.get('POSTGRES_HOST'),
#             port=values.get('POSTGRES_PORT'),
#             path=f'/{values.get("POSTGRES_DBNAME") or ""}',
#         )
#
#     class Config:
#         env_file = '.env'
#         env_file_encording = 'utf-8'
#         case_sensitive = True
#
# settings = Settings()