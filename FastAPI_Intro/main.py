from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import csv
import os
from typing import List

app = FastAPI()
CSV_FILE = "contacts.csv"

class Contact(BaseModel):
    name: str
    phone: int = Field(..., max_length=15)

class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str

def read_contacts_from_csv():
    contacts = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "phone"])
        return contacts
    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "phone": row["phone"]
                })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")
    return contacts

def write_contacts_to_csv(contacts):
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["id", "name", "phone"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing CSV: {str(e)}")

def get_next_id():
    contacts = read_contacts_from_csv()
    if not contacts:
        return 1
    return max([c["id"] for c in contacts]) + 1

@app.get("/contacts", response_model=List[ContactResponse])
async def get_contacts():
    return read_contacts_from_csv()

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int):
    contacts = read_contacts_from_csv()
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

@app.post("/contacts", status_code=201)
async def create_contact(contact: Contact):
    contacts = read_contacts_from_csv()
    new_id = get_next_id()
    new_contact = {"id": new_id, **contact.dict()}
    contacts.append(new_contact)
    write_contacts_to_csv(contacts)
    return {"message": "Contact added", "contact": new_contact}

@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: Contact):
    contacts = read_contacts_from_csv()
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            contacts[i] = {"id": contact_id, **contact.dict()}
            write_contacts_to_csv(contacts)
            return {"message": "Contact updated", "contact": contacts[i]}
    raise HTTPException(status_code=404, detail="Contact not found")

@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    contacts = read_contacts_from_csv()
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            removed = contacts.pop(i)
            write_contacts_to_csv(contacts)
            return {"message": "Contact deleted", "contact": removed}
    raise HTTPException(status_code=404, detail="Contact not found")
