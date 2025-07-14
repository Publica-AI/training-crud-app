from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
connection_string = os.getenv("DATABASE_URL")

print("Loaded DATABASE_URL:", connection_string)
# load_dotenv()
# connection_string = os.getenv("DATABASE_URL")

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()