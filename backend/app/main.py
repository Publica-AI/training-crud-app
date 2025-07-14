from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text
from app import models, schemas, crud, auth
from app.auth import authenticate_user, create_access_token, get_password_hash
from app.auth import get_current_user
from datetime import datetime
from uuid import uuid4
import os


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_userby_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
                )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/assignments", response_model=schemas.AssignmentOut)
def submit_assignment(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
   # Save file to disk
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_location = os.path.join(UPLOAD_DIR, file_name)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    return crud.create_assignment(
        db=db,
        title=title,
        file_path=file_location,
        user_id=current_user.id
    )
    
@app.get("/assignments/me", response_model=list[schemas.AssignmentOut])
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_assignment(db, current_user.id)

@app.post("/assignments/local", response_model=schemas.AssignmentOut)
def upload_assignment_local(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # Generate unique file name
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Save metadata to database
        return crud.create_assignment(
            db=db,
            title=title,
            file_path=file_path,
            user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))