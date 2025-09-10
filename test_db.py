# test_db.py
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
print("Using DB URL:", db_url)

engine = create_engine(db_url, future=True, echo=False, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        r = conn.execute(text("SELECT 1 AS ok"))
        print("DB responded:", r.all())
except Exception as e:
    print("Connection failed:", type(e).__name__, str(e))