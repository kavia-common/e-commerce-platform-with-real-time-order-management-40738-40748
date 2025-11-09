from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import hash_password, verify_password, create_access_token, get_current_user
from .database import get_db
from .models import User
from .schemas import UserCreate, UserLogin, UserOut, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserOut,
    summary="Register a new user",
    description="Create a new user account with email, password, and optional full_name.",
    responses={409: {"description": "Email already registered"}},
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user by email and password and return the profile."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login and obtain access token",
    description="Authenticate using email and password to receive a JWT bearer token.",
    responses={401: {"description": "Invalid credentials"}},
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return JWT token."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user profile",
    description="Return the profile of the current authenticated user.",
)
def me(current_user: User = Depends(get_current_user)):
    """Return current authenticated user's profile."""
    return current_user
