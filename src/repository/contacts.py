from fastapi import Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from datetime import date

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).order_by(Contact.id).limit(limit).offset(offset).all()
    
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return contact


async def get_contact_by_first_name(contact_first_name: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(first_name=contact_first_name).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return contact


async def get_contact_by_last_name(contact_last_name: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(last_name=contact_last_name).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return contact


async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=contact_email).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return contact


async def get_week_birthday_people(db: Session):
    birthday_people = []

    today = date.today()
    week = [date(year=today.year, month=today.month, day=today.day+num) for num in range(7)]

    objs = db.query(Contact).all()

    for obj in objs:
        this_year_birthday = obj.birth_date.replace(year=today.year)

        if this_year_birthday in week:
            birthday_people.append(obj)

    return birthday_people


async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=body.email).first()

    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email exists")
    
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact
    

async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(and_(Contact.id!=contact_id, Contact.email==body.email)).first()

    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email exists")
    
    contact = db.query(Contact).filter_by(id=contact_id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.email = body.email
    contact.birth_date = body.birth_date
    contact.additional_data = body.additional_data
    db.commit()

    return contact


async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(contact)
    db.commit()
