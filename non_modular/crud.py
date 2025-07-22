# Import required libraries
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration - Create a new SQLAlchemy engine instance  to manage DB connection
DATABASE_URL = 'mysql+pymysql://user:password@localhost:port/database-name'

engine = create_engine(DATABASE_URL)

# Base class for declaring ORM models                   
Base = declarative_base()

# Define the Item Model - This class defines the "items" table in the database
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    price = Column(Integer)

# Create a session factory (used to interact with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
# This function will be used to get a database connection for each request
# and ensure it is properly closed after the request is handled.
def get_db():
    db = SessionLocal()   # Create a new database session
    try:
        yield db          # Yield the session to the caller
    finally:
        db.close()        # Close the session after use

app = FastAPI()           # Create a FastAPI application instance

# --- UPDATE ---
@app.post("/item/")   # Define a simple route to test the connection
async def create_item(name: str, description: str, price: int, db: Session = Depends(get_db)): 
    # Use the dependency to get a database session
    try:
       new_item = Item(name=name, description=description, price=price)  # Create a new item instance
       db.add(new_item)
       db.commit()
       db.refresh(new_item)
       return new_item
    except Exception as e:
        return {"error": str(e)}
    
# --- READ ---
    
@app.get("/item")   # Define a simple route to test the connection
async def get_all_items(db: Session = Depends(get_db)): # Use the dependency to get a database session
    items = db.query(Item).all() # Fetch all items from the database
    return items  # FastAPI will automatically convert the list of Item objects to JSON

# --- UPDATE ---
@app.put("/item/{item_id}")
async def update_item(item_id: int, name: str, description: str, price: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.name = name
    item.description = description
    item.price = price

    db.commit()
    db.refresh(item)
    return item

# --- DELETE ---
@app.delete("/item/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": f"Item with ID {item_id} has been deleted"}