from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from datetime import datetime, timedelta

from src.database.db import get_db
from src.repository.users import get_user_by_email


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "3efdb0bd9fef572516d19aa6bff146e264708df086a559230cf358ebee036172"
    ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def get_hashed_password(self, password: str):
        hashed_password = self.pwd_context.hash(password)
        return hashed_password

    def verify_password(self, password, hashed_password):
        verify = self.pwd_context.verify(password, hashed_password)
        return verify

    async def create_access_token(self, data: dict):
        to_encode = data.copy()
        current_time = datetime.utcnow()
        expire = current_time + timedelta(minutes=15)
        scope = "access token"
        to_encode.update({"iat": current_time, "exp": expire, "scope": scope})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        current_time = datetime.utcnow()
        expire = current_time + timedelta(days=7)
        scope = "refresh token"
        to_encode.update({"iat": current_time, "exp": expire, "scope": scope})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_access_token

    async def decode_refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)

            if payload.get("scope") == "refresh token":
                email = payload.get("sub")
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})

        try:
            payload = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)

            if payload.get("scope") == "access token":
                email = payload.get("sub")

                if email is None:
                    raise credentials_exception
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except JWTError:
            raise credentials_exception
        
        user = await get_user_by_email(email, db)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't exist")
        return user
    

auth_service = Auth()
