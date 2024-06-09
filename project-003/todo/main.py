from todo.model import Todo, TodoCreate, TodoResponse
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, Annotated
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

load_dotenv()

# creating sever link
conn_str = os.getenv("DATABASE_URL")
engine = create_engine(conn_str)

def create_db():
   SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
   create_db()

# creating a session
def get_data():
   with Session(engine) as session:
      yield session

# creating fast api
app: FastAPI = FastAPI(
   title = "Todo App",
   description = "A Simple Todo Application",
   version = "0.1.0",
   servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
    ]
)

# creating CURD
@app.get("/")
def root():
   return {
      "message": "Welcome to Todo-App"
   } 
@app.get("/todo")
def get_todo(session: Annotated[Session, Depends(get_data)]):
   todo = session.exec(select(Todo)).all()
   return todo

@app.post("/todo/add", response_model=TodoResponse)
def add_todo(todo: TodoCreate, session: Annotated[Session, Depends(get_data)]):
   todo_added = Todo.model_validate(todo)
   session.add(todo_added)
   session.commit()
   session.refresh(todo_added)
   return todo_added

@app.delete("/todo/delete/{id}", response_model=TodoResponse)
def del_todo(id: int, session: Annotated[Session, Depends(get_data)]):
   todo_deleted = session.get(Todo, id)
   if not todo_deleted:
      return {"message" : "todo not found"}
   session.delete(todo_deleted)
   session.commit()
   return todo_deleted

@app.put("/todo/update/{id}", response_model=TodoResponse)
def update_todo(id: int, todo: TodoCreate, session: Annotated[Session, Depends(get_data)]):
   todo_updated = session.get(Todo, id)
   if not todo_updated:
      return {"message" : "todo not found"}
   todo_updated.name = todo.name
   todo_updated.description = todo.description
   session.commit()
   session.refresh(todo_updated)
   return todo_updated