from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.users import UserModel, UserResponseModel, TokenResponseModel
from src.repository.users import create_user, get_user_by_email, update_token
from src.services.auth import auth_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_hashed_password(body.password)
    user = await create_user(body, db)
    return {"user": user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenResponseModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await get_user_by_email(body.username, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = await auth_service.create_access_token({"sub": body.username})
    refresh_token = await auth_service.create_refresh_token({"sub": body.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/refresh_token", response_model=TokenResponseModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await get_user_by_email(email, db)

    if token != user.token:
        await update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    access_token = await auth_service.create_access_token({"sub": email})
    refresh_token = await auth_service.create_refresh_token({"sub": email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


