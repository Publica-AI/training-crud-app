# ============================================
# auth.py — Handles password hashing and JWT logic
# ============================================

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from schemas import TokenData

# Secret key and algorithm for JWT encoding/decoding
SECRET_KEY = "your-secret-key"  # Change this to a more secure, random value in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme instance — tells FastAPI the URL to get the token from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------
# Password utility functions
# -------------------------

# Hashes a plain-text password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verifies a plain-text password against a hashed one
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------
# JWT Token functions
# -------------------------

# Creates and returns a signed JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verifies a JWT token and extracts the username (subject)
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# -------------------------
# Temporary mock user storage (for demo only)
# -------------------------

# In a real app, this should come from your user database
fake_user = {
    "username": "admin",
    "hashed_password": get_password_hash("admin123")  # Plain password is 'admin123'
}
