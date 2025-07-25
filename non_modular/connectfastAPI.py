# Import required libraries
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration - Create a new SQLAlchemy engine instance  to manage DB connection
#DATABASE_URL = 'mysql+pymysql://user:password@localhost:port/database-name'

DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/sales'
engine = create_engine(DATABASE_URL)

# Base class for declaring ORM models                   
Base = declarative_base()

# Create a session factory (used to interact with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session. This function will be used to get a database connection for each request
# and ensure it is properly closed after the request is handled.
def get_db():
    db = SessionLocal()   # Create a new database session
    try:
        yield db          # Yield the session to the caller
    finally:
        db.close()        # Close the session after use

app = FastAPI()           # Create a FastAPI application instance

# Define a simple route to test the connection
@app.get("/")
async def read_root(db: Session = Depends(get_db)): # Use the dependency to get a database session
     return {"message": "Welcome to the FastAPI CRUD application!"}
