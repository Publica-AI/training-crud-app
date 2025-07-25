# Import required libraries
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration - Create a new SQLAlchemy engine instance  to manage DB connection
# Replace 'user', 'password', 'host', and 'database' with your actual database
engine = create_engine('mysql+pymysql://user:password@localhost:port/database-name')
                       

# Base class for declaring ORM models                   
Base = declarative_base()

# Define the Item Model - This class defines the "items" table in the database
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    price = Column(Integer)

# Automatically create the table (if not exists)
Base.metadata.create_all(engine)

# Create a session factory (used to interact with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)