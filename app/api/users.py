from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.core.security import pwd_context
from app.db.models.user_model import User

from app.db.session import get_db
from app.schemas.user import UserBase


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/signup")
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()
    db_username = db.query(User).filter(User.username == user.username).first()

    if db_email or db_username is not None:
        raise HTTPException(status_code=400, detail="User with the same email or username already exists.")
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=pwd_context.hash(user.password),
        is_active = user.is_active,
        is_staff=user.is_staff,
     )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
