from sqlalchemy import Column, Date, DateTime, Integer, String, func, event
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime


class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "Contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    additional_data = Column(String, default=None)
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

