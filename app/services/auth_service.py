from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.db.models.user_model import User
from app.db.models.user_model import Token
from app.core.security import verify_password
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import jwt


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def store_tokens(db: Session, user_id: int, access_token: str, refresh_token: str):

    db.query(Token).filter(
        and_(Token.user_id == user_id
             )
    ).delete()

    # Step 2: Store the new access and refresh tokens
    new_token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token





