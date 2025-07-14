from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Defines what data can be received or sent for user creation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    

    class Config:
        orm_mode = True

# AUTH SCHEMA (LOGIN)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Assignment Schema
class AssignmentCreate(BaseModel):
    title: str
    
class AssignmentOut(BaseModel):
    id: int
    title: str
    file_path: str
    owner_id: int
    #createdAt: datetime

    class Config:
        orm_mode = True

# Token Schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    

