from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# User Functions

def get_userby_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db:Session, user:schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Assignment Functions

def create_assignment(db: Session, title: str, file_path: str, user_id: int):
    db_assignment = models.Assignment(
        title=title,
        file_path=file_path,
        owner_id=user_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_user_assignment(db:Session, user_id: int):
    return db.query(models.Assignment).filter(models.Assignment.owner_id == user_id).all()
