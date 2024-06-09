from sqlmodel import SQLModel, Field
from typing import Optional, Union, Annotated
from pydantic import BaseModel
from fastapi import Form

# Create Model for Todos
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)
    is_completed: bool | None = Field(default=False)
    user_id: int = Field(foreign_key="user.id")

# Create Model for Users
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, min_length=20, max_length=40)
    email: str = Field(min_length=20, max_length=40)
    password: str = Field(min_length=8, max_length=24)

# create functionality for register_user route
class Register_User(BaseModel):
    username: Annotated[str, Form()]
    email: Annotated[str, Form()]
    password: Annotated[str, Form()]

# create Model for generating Access_Token
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

# create Model for decoded jwt data
class TokenData(BaseModel):
    username: str

# create Model for decoded jwt data
class RefreshTokenData (BaseModel):
    email:str

# Create Model for Todos verification
class Todo_Created(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)

# Create Model for Todos verification
class Todo_Edited(BaseModel):
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)
    is_completed: bool | None = Field(default=False)