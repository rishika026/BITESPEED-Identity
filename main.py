from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


from database import SessionLocal, engine
import models, schemas
from models import Contact, LinkPrecedence

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify")
def identify_contact(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email, phone = payload.email, payload.phoneNumber
    if not email and not phone:
        return {"error": "Email or PhoneNumber required"}

    contacts = db.query(Contact).   filter(
        (Contact.email == email) | (Contact.phoneNumber == phone)
    ).all()

    if not contacts:
        new_contact = Contact(email=email, phoneNumber=phone)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email],
            "phoneNumbers": [new_contact.phoneNumber],
            "secondaryContactIds": []
        }

    # Sort by createdAt to determine primary
    primary_contact = min(contacts, key=lambda c: c.createdAt)
    secondary_ids = []

    for c in contacts:
        if c.id != primary_contact.id and c.linkPrecedence == LinkPrecedence.primary:
            c.linkPrecedence = LinkPrecedence.secondary
            c.linkedId = primary_contact.id
            db.commit()
        if c.linkPrecedence == LinkPrecedence.secondary:
            secondary_ids.append(c.id)

    emails = {c.email for c in contacts if c.email}
    phones = {c.phoneNumber for c in contacts if c.phoneNumber}

    return {
        "primaryContactId": primary_contact.id,
        "emails": list(emails),
        "phoneNumbers": list(phones),
        "secondaryContactIds": secondary_ids
    }

