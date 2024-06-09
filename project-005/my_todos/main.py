from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, Union, Annotated, AsyncGenerator
from my_todos.database import engine, get_session
from contextlib import asynccontextmanager

# create Model
    # data model
    # table model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)
    is_completed: bool | None = Field(default=False)

# Now create real time tables with the help of engine
def create_tables() -> None:
    SQLModel.metadata.create_all(engine)

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating Tables ...")
    create_tables()
    yield

# create FastAPI
app: FastAPI = FastAPI(
    lifespan = lifespan, 
    title = "A Todos API integrated with Docker", 
    description = "This is an API of Todos integrated with Docker", 
    version = "0.1.2",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
    ]
)

# create decorator
@app.get("/")
async def root():
    return {"message": "Welcome to My_Todos App with Docker"}

@app.post("/todos/", response_model=Todo)
async def create_todos(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos/", response_model=list[Todo])
async def get_all(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    if todos:
        return todos
    else:
        raise HTTPException(status_code=404, detail="opps! no task found.")
    
@app.get("/todos/{id}", response_model=Todo)
async def get_single_todo(id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="opps! id not found.")

@app.patch("/todos/{id}")
async def update_todo():
    ...

@app.put("/todos/{id}")
async def edit_todo(todo: Todo, id: int, session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.exec(select(Todo).filter(Todo.id == id)).first()
    if existing_todo:
        existing_todo.title = todo.title
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code=404, detail="opps! id not found.")

@app.delete("/todos/{id}")
async def del_todo(id: int, session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.get(Todo, id)
    if existing_todo:
        session.delete(existing_todo)
        session.commit()
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="opps! id not found.")