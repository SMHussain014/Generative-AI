from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from my_daily_todos import settings
from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager
from my_daily_todos.models import Todo
from my_daily_todos.database import engine, get_session
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
from my_daily_todos import todos_pb2

# Now create real time tables with the help of engine
def create_tables() -> None:
    SQLModel.metadata.create_all(engine)

async def consume_todos(mytopics1, myserver1):
    consumer = AIOKafkaConsumer(
            str(settings.KAFKA_TODOS_TOPIC), 
            bootstrap_servers=str(settings.BOOTSTRAP_SERVER), 
            group_id=str(settings.GROUP_ID)
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print(f"Received message: {msg.value.decode()} on topic {msg.topic}")
            new_todos = todos_pb2.Todo()
            new_todos.ParseFromString(msg.value)
            print(f"Consumer's Deserialized data -> {new_todos}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        await consumer.stop()

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Calling Kafka Consumer ...")
    task1 = asyncio.create_task(
        consume_todos(
            mytopics1=str(settings.KAFKA_TODOS_TOPIC), 
            myserver1=str(settings.BOOTSTRAP_SERVER)
        )
    )
    print("Creating Tables ...")
    create_tables()
    yield

# create FastAPI
app: FastAPI = FastAPI(
    lifespan = lifespan, 
    title = "My_Daily_Todos", 
    description = "This is an API with KAFKA and Protobuff", 
    version = "0.1.8",
    servers=[{
            "url": "http://127.0.0.1:8000",
            "description": "Development Server"
    }]
)

# create decorators
@app.get("/")
async def read_message():
    return {"message": "Welcome to My_Daily_Todos using Kafka and Protobuff"}

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/todos/", response_model=Todo)
async def create_todo(
    todo: Todo, 
    session: Annotated[Session, Depends(get_session)], 
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    todos_protobuf = todos_pb2.Todo(
        id = todo.id,
        title = todo.title,
        content = todo.content,
        is_completed = todo.is_completed
    )
    serialized_todos = todos_protobuf.SerializeToString()
    await producer.send_and_wait(str(settings.KAFKA_TODOS_TOPIC), serialized_todos)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    return todos