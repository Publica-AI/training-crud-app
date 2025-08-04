from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
import csv, os
app = FastAPI()
# --------------------------
# CONTACT SECTION
# --------------------------
CONTACTS_CSV = "contact.csv"
class Contact(BaseModel):
    name: str = Field(..., max_length=15)
    phone: str = Field(...)
    @validator("name")
    def name_must_be_letters(cls, v):
        if not v.isalpha():
            raise ValueError("Name must contain only letters")
        return v
    @validator("phone")
    def phone_must_be_digits(cls, v):
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(v) < 7:
            raise ValueError("Phone number must be at least 7 digits")
        return v
class ContactOut(Contact):
    id: int
def read_contacts() -> List[dict]:
    contacts = []
    if os.path.exists(CONTACTS_CSV):
        with open(CONTACTS_CSV, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "phone": row["phone"]
                })
    return contacts
def write_contacts(contacts: List[dict]):
    with open(CONTACTS_CSV, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "phone"])
        writer.writeheader()
        for c in contacts:
            writer.writerow(c)
@app.get("/contacts", response_model=List[ContactOut], tags=["Contacts"])
async def get_contacts():
    return read_contacts()
@app.post("/contacts", response_model=ContactOut, tags=["Contacts"])
async def create_contact(contact: Contact):
    contacts = read_contacts()
    for c in contacts:
        if c["name"].lower() == contact.name.lower() and c["phone"] == contact.phone:
            raise HTTPException(status_code=400, detail="Contact already exists")
    new_id = max([c["id"] for c in contacts], default=0) + 1
    new_contact = {"id": new_id, **contact.dict()}
    contacts.append(new_contact)
    write_contacts(contacts)
    return new_contact
@app.put("/contacts/{contact_id}", response_model=ContactOut, tags=["Contacts"])
async def update_contact(contact_id: int, updated: Contact):
    contacts = read_contacts()
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            contacts[i] = {"id": contact_id, **updated.dict()}
            write_contacts(contacts)
            return contacts[i]
    raise HTTPException(status_code=404, detail="Contact not found")
@app.delete("/contacts/{contact_id}", tags=["Contacts"])
async def delete_contact(contact_id: int):
    contacts = read_contacts()
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            removed = contacts.pop(i)
            write_contacts(contacts)
            return {"message": "Contact deleted", "contact": removed}
    raise HTTPException(status_code=404, detail="Contact not found")
# --------------------------
# USER REGISTRATION SECTION
# --------------------------
USERS_CSV = "user.csv"
class User(BaseModel):
    name: str
    track: str
    email: EmailStr
class UserOut(User):
    id: int
def read_users() -> List[dict]:
    users = []
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "track": row["track"],
                    "email": row["email"]
                })
    return users
def write_users(users: List[dict]):
    with open(USERS_CSV, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "track", "email"])
        writer.writeheader()
        for u in users:
            writer.writerow(u)
@app.get("/users", response_model=List[UserOut], tags=["Users"])
async def get_users():
    return read_users()
@app.post("/register", response_model=UserOut, tags=["Users"])
async def register_user(user: User):
    users = read_users()
    for u in users:
        if u["email"].lower() == user.email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")
    new_id = max([u["id"] for u in users], default=0) + 1
    new_user = {"id": new_id, **user.dict()}
    users.append(new_user)
    write_users(users)
    return new_user


