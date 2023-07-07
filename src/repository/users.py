from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserModel



async def get_user_by_email(email: EmailStr, db: Session):
    user = db.query(User).filter_by(email=email).first()
    return user


async def create_user(body: UserModel, db: Session = Depends(get_db)):
    avatar = None

    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    user = User(**body.dict(), avatar=avatar)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: Session = Depends(get_db)):
    user.refresh_token = token
    db.commit()


