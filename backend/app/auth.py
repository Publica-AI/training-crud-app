from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

#JWT Config

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

# PASSWORD Hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# OAuth2 scheme (Bearer token in header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password Utils

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# JWT Token Utils

def create_access_token(data:dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception()
        return schemas.TokenData(id=user_id)
    except  JWTError:
        raise credentials_exception()
    
# Get current user dependency

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = decode_token(token)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception()
    return user

# Login flow

def authenticate_user(db:Session, email:str, password: str):
    user = crud.get_userby_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
    
        
