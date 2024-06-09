from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from daily_todo import setting
from typing import Annotated
from contextlib import asynccontextmanager

# create Model
    # data model
    # table model
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=5, max_length=30)
    content: str = Field(min_length=7, max_length=60)
    is_completed: bool | None = Field(default=False)

# create server connection (only one engine for whole application)
conn_str: str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(
    conn_str, 
    connect_args={"sslmode": "require"}, 
    pool_recycle=300, 
    pool_size=10,
    echo=True
)

# Now create real time tables with the help of engine
def create_tables():
    SQLModel.metadata.create_all(engine)

# create session (separate session for each functionality/transaction)
def get_session():
    with Session(engine) as session:
        yield session

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables ...")
    create_tables()
    yield

# create FastAPI
app: FastAPI = FastAPI(
    lifespan = lifespan, 
    title = "Daily_Todo App", 
    description = "This is a simple Todo App", 
    version = "0.1.1",
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
    return {"message": "Welcome to the Daily_Todo App"}

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
