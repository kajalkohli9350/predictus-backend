from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.services.auth_service import (
    get_user_by_email,
    create_user,
    authenticate_user,
    generate_token_for_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = generate_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}