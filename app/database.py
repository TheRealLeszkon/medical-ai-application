from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME=os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASE_HOST=os.getenv("DATABASE_HOST", "localhost")
DATABASE_URL = f"postgresql+psycopg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"


engine = create_engine(
    DATABASE_URL,
    echo=True
)

def get_session():
    with Session(engine) as session:
        yield session