from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import AsyncGenerator, Annotated
from place_an_order.models import Order
from place_an_order import settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

async def consume_orders(mytopics2, myserver2):
    consumer = AIOKafkaConsumer(
        str(settings.KAFKA_ORDERS_TOPIC), 
        bootstrap_servers=str(settings.BOOTSTRAP_SERVER), 
        group_id=str(settings.GROUP_ID),
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print("consumer: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            print(f"Received message: {msg.value.decode()} on topic {msg.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        await consumer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Calling Kafka Consumer ...")
    task2 = asyncio.create_task(
        consume_orders(
            mytopics2=str(settings.KAFKA_ORDERS_TOPIC), 
            myserver2=str(settings.BOOTSTRAP_SERVER)
        )
    )
    yield

app = FastAPI(
    lifespan=lifespan, 
    title="Orders Placement Service", 
    description = "This is an API with KAFKA", 
    version="0.1.7",
    servers=[{
            "url": "http://127.0.0.1:8001",
            "description": "Development Server"
    }])

@app.get("/")
def welcome_message():
    return {"message": "Welcome to Place_an_Order App using KAFKA"}

# @app.post("/create_orders")
# async def create_orders(orders: Orders):
#     producer = AIOKafkaProducer(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
#     await producer.start()
#     orderJSON = json.dumps(orders.__dict__).encode("utf-8")
#     try:
#         await producer.send_and_wait(str(settings.KAFKA_ORDERS_TOPIC), orderJSON)
#     finally:
#         await producer.stop()
#     return orderJSON

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/create_orders/")
async def create_orders(
    orders: Order, 
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    orders_json = json.dumps(orders.__dict__).encode("utf-8")
    await producer.send_and_wait(str(settings.KAFKA_ORDERS_TOPIC), orders_json)
    return orders_json