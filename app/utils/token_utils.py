# services/auth_service.py
from jose import JWTError, jwt
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.user_model import Token
from app.db.models.user_model import User

def verify_refresh_token(refresh_token: str, db: Session):
    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_name = payload.get("sub")

        if user_name is None:
            raise JWTError("Invalid refresh token payload")

        # Find the user in the database
        user = db.query(User).filter(
            and_(User.username == user_name
                 )
        ).first()
        if not user:
            return None

        # Check if the refresh token exists in the database for the user
        stored_token = db.query(Token).filter(
            and_(Token.refresh_token == refresh_token, Token.user_id == user.id
                 )
        ).first()
        if stored_token is None:
            return None

        return user  # Return the user if the token is valid
    except JWTError as e:
        return None
