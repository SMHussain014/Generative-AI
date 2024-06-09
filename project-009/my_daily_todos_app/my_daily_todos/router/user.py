from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from my_daily_todos.models import User, Register_User
from my_daily_todos.authentication import get_user_from_database, hash_password, current_user
from my_daily_todos.database import get_session

# create external router
user_router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {
        "description" : "Not Found"
        }
    }
)

# create decorators
@user_router.get("/")
async def welcome_message_from_user_route():
    return {
        "message" : "Welcome to Users Page"
    }

@user_router.post("/register")
async def register_user(new_user:Annotated[Register_User, Depends()], 
                        session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_database(session, new_user.username, new_user.email)
    if db_user:
        HTTPException(status_code=409, detail="This user already exists!")
    user = User(username = new_user.username, 
                email = new_user.email,
                password = hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f"""The User titled {user.username} successfully registered"""}

@user_router.get("/secure")
async def secure_route(current_user:Annotated[User, Depends(current_user)]):
    return current_user