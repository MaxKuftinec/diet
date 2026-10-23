import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")

# postgresql://postgres:<password>@localhost:5432/fastapi
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{DB_PASS}@localhost:5432/{DB_NAME}"

engine = create_engine()