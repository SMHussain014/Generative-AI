from sqlmodel import SQLModel, Field
from typing import Optional

# creating Todo Table
class Todo(SQLModel, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   name: str = Field(index=True)
   description: str

class TodoCreate(SQLModel):
   name: str
   description: str

class TodoResponse(SQLModel):
   id: int
   name: str
   description: str

def create_db():
   SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
   create_db()