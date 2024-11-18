from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.schemas.token_schema import Token, TokenRefreshRequest
from app.services.auth_service import authenticate_user, create_access_token, create_refresh_token, store_tokens
from app.utils.token_utils import verify_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate the user
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate new tokens
    access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})

    # Store the tokens in the database and delete old ones
    store_tokens(db, user.id, access_token, new_refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# routes.py
@router.post("/token/refresh", response_model=Token)
async def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    # Verify the refresh token and fetch the user
    user = verify_refresh_token(request.refresh_token, db)

    if not user:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    # Generate new tokens
    new_access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})

    # Store new tokens in the database and delete old ones
    print(user)
    store_tokens(db, user.id, new_access_token, new_refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }









