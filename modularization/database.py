# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv() #  Load environment variables from .env file

# Database connection setup
# Ensure you have a DATABASE_URL in your .env file
connection_string = os.getenv("DATABASE_URL")
if not connection_string:
    raise ValueError("DATABASE_URL environment variable not set. Please set it in your .env file.")

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


