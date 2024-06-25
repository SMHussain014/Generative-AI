from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import asyncio
from kafka_consumers.consumers.consumer import consume_message
from kafka_consumers.depandencies.depandency import create_tables

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    loop = asyncio.get_event_loop()
    task = loop.create_task(consume_message())
    yield
    task.cancel()
    await task

# create FastAPI
app: FastAPI = FastAPI(
    lifespan = lifespan, 
    title = "Orders", 
    description = "This is an Orders API with KAFKA and Protobuff", 
    version = "0.2.0",
    servers=[{
            "url": "http://127.0.0.1:9008",
            "description": "Development Server"
    }]
)
