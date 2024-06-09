from passlib.context import CryptContext
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from my_daily_todos.database import get_session
from my_daily_todos.models import Todo, User, Token, TokenData, RefreshTokenData
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta


# password_context = CryptContext(schemes="bcrypt")
password_context = CryptContext(schemes="bcrypt", deprecated="auto")
def hash_password(password):
    return password_context.hash(password)

def verify_password(password, hash_password):
    return password_context.verify(password, hash_password)

def get_user_from_database(session:Annotated[Session, Depends(get_session)], 
                           username: str | None = None, 
                           email: str | None = None):
    statement_for_user = select(User).where(User.username == username)
    user = session.exec(statement_for_user).first()
    if not user:
        statement_for_email = select(User).where(User.email == email)
        user = session.exec(statement_for_email).first()
        if user:
            return user
    return user

def authenticate_user (username, 
                       email, 
                       password, 
                       session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_database(session, username=username, email=email)
    if not db_user:
        return {"message" : "Invalid Username"}
    if not verify_password(password=password, hash_password=db_user.password):
        return {"message" : "Invalid Password"}
    return db_user

SECRET_KEY = "ed125th74lj9573u879ub806kjgytkgy6hfytk989ghvkjh"
ALGORITHYM = "HS256"
EXPIRY_TIME = 1

def create_access_token(data:dict, expiry_time:timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
        # expire = datetime.utcnow() + expire_time
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHYM)
    return encoded_jwt

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def current_user(token:Annotated[str, Depends(oauth_scheme)], 
                 session:Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Token, Please login again",
        headers = {"www-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        username: str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    
    except JWTError as e:
        return {"error" : "str(e)"}
    user = get_user_from_database(session, username=token_data.username, email=None)
    if not user:
        raise credential_exception
    return user

def create_refresh_token(data:dict, expiry_time:timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHYM)
    return encoded_jwt

def validate_refresh_token(token: str,
                           session: Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        email: str | None = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = RefreshTokenData(email=email)
    except JWTError as e:
        return {"error" : "str(e)"}
    user = get_user_from_database(session, email=token_data.email)
    if not user:
        raise credential_exception
    return user