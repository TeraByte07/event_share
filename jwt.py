from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
from app.models.user_models import BlacklistedToken
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_access_token(data: dict, expire_timedelta: timedelta = None):
    now = datetime.utcnow()
    expiry_time = now + (expire_timedelta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    data_to_encode = {**data, "exp": expiry_time, "scope": "access_token"}
    return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expire_timedelta: timedelta = None):
    now = datetime.utcnow()
    expiry_time = now + (expire_timedelta or timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    data_to_encode = {**data, "exp": expiry_time, "scope": "refresh_token"}
    return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str, db: Session, scope: str = "access_token") -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("scope") != scope:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token scope.")
        if db.query(BlacklistedToken).filter_by(token=token).first():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")

def decode_refresh_token(token: str, db: Session, scope: str = "refresh_token") -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("scope") != scope:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token scope.")
        if db.query(BlacklistedToken).filter_by(token=token).first():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")

def blacklist_token(db: Session, token: str):
    if not db.query(BlacklistedToken).filter_by(token=token).first():
        blacklist = BlacklistedToken(token=token)
        db.add(blacklist)
        db.commit()

def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(BlacklistedToken).filter_by(token=token).first() is not None