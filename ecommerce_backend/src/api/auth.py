from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .models import User

settings = get_settings()

# OAuth2 scheme for Swagger "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash."""
    if hashed_password is None:
        return False
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def create_access_token(*, user_id: int, expires_minutes: Optional[int] = None) -> str:
    """Create a signed JWT for the given user id."""
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def _decode_with_secret(token: str, secret: str) -> Optional[int]:
    """Attempt to decode JWT and return user_id (sub)."""
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except JWTError:
        return None


# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Resolve the current authenticated user from the JWT token.
    Attempts verification against local JWT secret first, then optional Supabase secret if provided.
    Raises 401 if invalid or user not found.
    """
    user_id = _decode_with_secret(token, settings.JWT_SECRET)

    # Optional Supabase JWT verification if primary fails and secret available
    if user_id is None and settings.SUPABASE_JWT_SECRET:
        user_id = _decode_with_secret(token, settings.SUPABASE_JWT_SECRET)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
