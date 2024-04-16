from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from config import SECRET_KEY, ALGORITHM
from hash import Hasher
from model import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def authenticate_user(db: Session, username: str, password: str) -> Optional[Users]:
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not Hasher.verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_by_username(db:Session,username:str):
    return db.query(Users).filter(Users.username == username).first()

def get_current_user(db:Session,token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user_by_username(db,username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_superuser(user: Users = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="User is not a superuser")
    return user

