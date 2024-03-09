from dotenv import load_dotenv, find_dotenv
import os

from sqlalchemy.engine import URL

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

# ip = str(os.getenv('ip'))
# PGUSER = str(os.getenv('PGUSER'))
# PGPASSWORD = str(os.getenv('PGPASSWORD'))
# DATABASE = str(os.getenv('DATABASE'))
# PORT = str(os.getenv('PORT'))

DB_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=str(os.getenv('PGUSER')),
    password=str(os.getenv('PGPASSWORD')),
    host=str(os.getenv('ip')),
    database=str(os.getenv('DATABASE')),
    port=os.getenv('PORT'),
)
