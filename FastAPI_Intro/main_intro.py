from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

contacts = [
    {"id": 1, "name": "Moji", "phone": "876654326"},
    {"id": 2, "name": "Alex", "phone": "123456789"}
]

class Contact(BaseModel):
    name: str
    phone: str= Field(..., max_length=15)

@app.get("/contacts")
async def get_contacts():
    return contacts

@app.post("/contacts", status_code=201)
async def create_contact(contact: Contact):
    new_id = max([c["id"] for c in contacts], default=0) + 1
    new_contact = {"id": new_id, **contact.dict()}
    contacts.append(new_contact)
    return {"message": "Contact added", "contact": new_contact}

@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: Contact):
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            contacts[i] = {"id": contact_id, **contact.dict()}
            return {"message": "Contact updated", "contact": contacts[i]}
    raise HTTPException(status_code=404, detail="Contact not found")

@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            removed = contacts.pop(i)
            return {"message": "Contact deleted", "contact": removed}
    raise HTTPException(status_code=404, detail="Contact not found")