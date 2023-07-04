from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_

from json import dumps
from typing import List

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel, ContactResponseModel
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])    

@router.get("/", response_model=List[ContactResponseModel])
async def get_contacts(limit: int = Query(10, le=100), skip: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, skip, db)
    
    return contacts


@router.get("/week_birthday_people", response_model=List[ContactResponseModel])
async def get_week_birthday_people(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_week_birthday_people(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponseModel)
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    
    return contact


@router.get("/first_name/{contact_first_name}", response_model=ContactResponseModel)
async def get_contact_by_first_name(contact_first_name, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_first_name(contact_first_name, db)

    return contact


@router.get("/last_name/{contact_last_name}", response_model=ContactResponseModel)
async def get_contact_by_last_name(contact_last_name, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_last_name(contact_last_name, db)

    return contact


@router.get("/email/{contact_email}", response_model=ContactResponseModel)
async def get_contact_by_email(contact_email, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)

    return contact


@router.post("/", response_model=ContactResponseModel, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)

    return contact
    

@router.put("/{contact_id}", response_model=ContactResponseModel)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(body, contact_id, db)

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    await repository_contacts.remove_contact(contact_id, db)
