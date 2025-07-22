# user_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin, Token, UserOut, UserCreate
from auth import get_password_hash, verify_password

router = APIRouter()

# --- CREATE USER ---
@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- READ ALL USERS ---
@router.get("/users/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# --- READ USER BY ID ---
@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- UPDATE USER ---
@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = user_update.username
    user.hashed_password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user

# --- DELETE USER ---
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}
