from my_daily_todos.models import Todo, User, Token, Todo_Created, Todo_Edited
from my_daily_todos.database import engine, get_session
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from my_daily_todos.router import user
from typing import AsyncGenerator, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from my_daily_todos.authentication import authenticate_user, EXPIRY_TIME, create_access_token, current_user, create_refresh_token, validate_refresh_token 
from datetime import timedelta

# Now create real-time tables with the help of engine
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
    title = "My_Daily_Todos App", 
    description = "This is an API of Todos with Mutli-Users", 
    version = "0.1.6",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
    ]
)

# include API Routers
app.include_router(router=user.user_router)

# create decorator
@app.get("/")
async def root():
    return {
        "message": "Welcome to the My_Daily_Todos App"
    }

# login - username && password
@app.post("/token", response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                session:Annotated[Session, Depends(get_session)]):
    user = authenticate_user(username=form_data.username,
                             password=form_data.password,
                             email=None, 
                             session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Username or Password")
    expire_time = timedelta(minutes = EXPIRY_TIME)
    access_token = create_access_token({"sub": form_data.username}, expire_time)
    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

@app.post("/token/refresh")
def refresh_token(old_token:str,
                  session:Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )
    user = validate_refresh_token(old_token, session)
    if not user:
        raise credential_exception
    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub":user.username}, expire_time)
    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)
    return Token(access_token=access_token, token_type= "bearer", refresh_token=refresh_token)

@app.post("/todos/", response_model=Todo)
async def create_todos(current_user:Annotated[User, Depends(current_user)],
                       todo: Todo_Created,
                       session: Annotated[Session, Depends(get_session)]):
    new_todo = Todo(user_id = current_user.id, id = todo.id, title = todo.title, content = todo.content)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=list[Todo])
async def get_all_todos(current_user:Annotated[User, Depends(current_user)],
                        session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    if todos:
        return todos
    else:
        raise HTTPException(status_code=404, detail="No Task found")
    
@app.get("/todos/{id}", response_model=Todo)
async def get_single_todo(current_user:Annotated[User, Depends(current_user)],
                          id: int, 
                          session: Annotated[Session, Depends(get_session)]):
    user_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    matched_todos = next((todo for todo in user_todos if todo.id == id), None)
    if matched_todos:
        return matched_todos
    else:
        raise HTTPException(status_code=404, detail="No Task found")

@app.patch("/todos/{id}")
async def update_todo():
    ...

@app.put("/todos/{id}")
async def edit_todo(todo: Todo_Edited, 
                    id: int, 
                    current_user:Annotated[User, Depends(current_user)],
                    session: Annotated[Session, Depends(get_session)]):
    user_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    existing_todo = next((todo for todo in user_todos if todo.id == id), None)
    if existing_todo:
        existing_todo.title = todo.title
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code=404, detail="No Task found")

@app.delete("/todos/{id}")
async def del_todo(id: int, 
                   current_user:Annotated[User, Depends(current_user)],
                   session: Annotated[Session, Depends(get_session)]):
    user_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    existing_todo = next((todo for todo in user_todos if todo.id == id), None)
    if existing_todo:
        session.delete(existing_todo)
        session.commit()
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="No Task found")