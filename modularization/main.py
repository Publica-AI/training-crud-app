# # main.py

# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import Base, Item
# from database import engine, get_db
# import schemas  # <-- import schemas
# from fastapi.security import OAuth2PasswordRequestForm
# from auth import verify_password, create_access_token, fake_user, oauth2_scheme
# from schemas import Token

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # --- CREATE ---
# @app.post("/item/", response_model=schemas.ItemOut)
# async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     new_item = Item(name=item.name, description=item.description, price=item.price)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item

# # --- READ ---
# @app.get("/item", response_model=list[schemas.ItemOut])
# async def get_all_items(db: Session = Depends(get_db)):
#     items = db.query(Item).all()
#     return items

# # --- UPDATE ---
# @app.put("/item/{item_id}", response_model=schemas.ItemOut)
# async def update_item(item_id: int, updated_data: schemas.ItemUpdate, db: Session = Depends(get_db)):
#     item = db.query(Item).filter(Item.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")

#     item.name = updated_data.name
#     item.description = updated_data.description
#     item.price = updated_data.price

#     db.commit()
#     db.refresh(item)
#     return item

# # --- DELETE ---
# @app.delete("/item/{item_id}")
# async def delete_item(item_id: int, db: Session = Depends(get_db)):
#     item = db.query(Item).filter(Item.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")

#     db.delete(item)
#     db.commit()
#     return {"message": f"Item with ID {item_id} has been deleted"}

# # --- TOKEN ROUTE ---
# @app.post("/token", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     if form_data.username != fake_user["username"] or not verify_password(form_data.password, fake_user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
#     access_token = create_access_token(data={"sub": form_data.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import Base, Item
import schemas
import auth  # Handles password hashing and token generation
from auth import fake_user, verify_password, create_access_token, get_current_user
app = FastAPI()

# ============================
# CRUD ROUTES
# ============================

# --- CREATE ---
@app.post("/item/", response_model=schemas.ItemOut)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db),\
                       current_user: dict = Depends(get_current_user)): # <-- authenticate the user):
    new_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# --- READ ---
@app.get("/item", response_model=list[schemas.ItemOut])
async def get_all_items(db: Session = Depends(get_db),\
                       current_user: dict = Depends(get_current_user)): # <-- authenticate the user):
    return db.query(Item).all()

# --- UPDATE ---
@app.put("/item/{item_id}", response_model=schemas.ItemOut)
async def update_item(item_id: int, updated_data: schemas.ItemUpdate, db: Session = Depends(get_db),\
                       current_user: dict = Depends(get_current_user)): # <-- authenticate the user):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.name = updated_data.name
    item.description = updated_data.description
    item.price = updated_data.price

    db.commit()
    db.refresh(item)
    return item

# --- DELETE ---
@app.delete("/item/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db),\
                       current_user: dict = Depends(get_current_user)): # <-- authenticate the user):):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": f"Item with ID {item_id} has been deleted"}

# ============================
# AUTH ROUTES
# ============================

# --- Login route to authenticate and return JWT ---
@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simulating user lookup (this should query a real DB)
    user_dict = auth.fake_user

    if form_data.username != user_dict["username"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not auth.verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # If authenticated, generate a token
    access_token = auth.create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Protected route that requires a valid token ---
@app.get("/profile")
async def get_profile(username: str = Depends(auth.get_current_user)):
    return {"message": f"Welcome {username}, this is your protected profile."}
