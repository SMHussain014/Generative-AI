from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from products import settings
from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager
from products.models import Products
from products.database import engine, get_session
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from products import products_pb2
import asyncio

# Now create real time tables with the help of engine
def create_tables() -> None:
    SQLModel.metadata.create_all(engine)

async def consume_products(mytopics1, myserver1):
    consumer = AIOKafkaConsumer(
            str(settings.KAFKA_PRODUCTS_TOPIC), 
            bootstrap_servers=str(settings.BOOTSTRAP_SERVER), 
            group_id=str(settings.GROUP_ID)
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print(f"Received message: {msg.value.decode()} on topic {msg.topic}")
            new_product = products_pb2.Product()
            new_product.ParseFromString(msg.value)
            print(f"Consumer's Deserialized data -> {new_product}")
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            return new_product
    finally:
        await consumer.stop()

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Calling Kafka Consumer ...")
    task1 = asyncio.create_task(
        consume_products(
            mytopics1=str(settings.KAFKA_PRODUCTS_TOPIC), 
            myserver1=str(settings.BOOTSTRAP_SERVER)
        )
    )
    print("Creating Tables ...")
    create_tables()
    yield

# create FastAPI
app: FastAPI = FastAPI(
    lifespan = lifespan, 
    title = "Products", 
    description = "This is an API with KAFKA and Protobuff", 
    version = "0.2.0",
    servers=[{
            "url": "http://127.0.0.1:9001",
            "description": "Development Server"
    }]
)

# create decorators
@app.get("/")
async def read_message():
    return {"message": "Welcome to Product Service"}

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/products/", response_model=Products)
async def create_products(
    product: Products, 
    session: Annotated[Session, Depends(get_session)], 
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    products_protobuf = products_pb2.Products(
        id = product.id,
        product_category = product.product_category,
        product_name = product.product_name,
        size = product.size,
        price = product.price
    )
    serialized_products = products_protobuf.SerializeToString()
    await producer.send_and_wait(str(settings.KAFKA_PRODUCTS_TOPIC), serialized_products)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products/", response_model=list[Products])
def read_products(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(Products)).all()
    return products