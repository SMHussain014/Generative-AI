from fastapi.testclient import TestClient
from daily_todo import setting
from sqlmodel import SQLModel, create_engine, Session
from daily_todo.main import app, get_session
import pytest

# create server connection
conn_str: str = str(setting.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(
    conn_str, 
    connect_args={"sslmode": "require"}, 
    pool_recycle=300, 
    pool_size=10,
    echo=True
)

# reuse code with pytest fixture
@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)

@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session
    app.dependency_overrides[get_session] = test_session
    with TestClient(app = app) as client:
        yield client

def test_root():
    client = TestClient(app = app)
    response = client.get('/')
    data = response.json()
    assert response.status_code == 200
    assert data == {"message": "Welcome to the daily_todo app"}

def test_create_todos(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app = app)
    test_todo = {"id": 20, "title": "Title000", "content": "Content000", "is_completed": False}
    response = test_app.post('/todos/', json=test_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]

def test_get_all(test_app):
    test_todo = {"id": 21, "title": "Title111", "content": "Content111", "is_completed": False}
    response = test_app.post('/todos/', json=test_todo)
    data = response.json()
    response = test_app.get('/todos/')
    assert response.status_code == 200
    todo_list_last = response.json()[-1]
    assert todo_list_last["content"] == test_todo["content"]

def test_get_single_todo(test_app):
    test_todo = {"id": 22, "title": "Title222", "content": "Content222", "is_completed": False}
    response = test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    response = test_app.get(f'/todos/{todo_id}')
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]

def test_edit_todo(test_app):
    test_todo = {"id": 23, "title": "Title23", "content": "Content23", "is_completed": False}
    response = test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    edited_todo = {"id": 23, "title": "Title333", "content": "Content333", "is_completed": False}
    response = test_app.put(f'/todos/{todo_id}', json=edited_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == edited_todo["content"]

def test_del_todo(test_app):
    test_todo = {"id": 24, "title": "Title444", "content": "Content444", "is_completed": False}
    response = test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    response = test_app.delete(f'/todos/{todo_id}')
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Task deleted successfully"