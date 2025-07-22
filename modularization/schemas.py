# schemas.py
# import necessary libraries
from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating an item
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

# Schema for updating an item
class ItemUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

# Schema for response (if needed)
class ItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int

    class Config:
        orm_mode = True

# Schema for user creation
# --- User Schemas ---

# Schema for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Schema for displaying user data (response)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# Schema for user updates
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str