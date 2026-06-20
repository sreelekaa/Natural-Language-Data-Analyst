from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

from urllib.parse import quote_plus

password = quote_plus(os.getenv("DB_PASSWORD"))

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
try:
    conn = engine.connect()
    print("Database Connected Successfully!")
    conn.close()
except Exception as e:
    print(e)