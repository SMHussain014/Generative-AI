from sqlmodel import SQLModel, Field
from typing import Optional, Union
from pydantic import BaseModel

# create Model
    # data model
    # table model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)
    is_completed: bool | None = Field(default=False)

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