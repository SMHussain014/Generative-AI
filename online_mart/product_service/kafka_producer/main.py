from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from kafka_producer.routes import product
from kafka_producer.producers.producer import create_kafka_topic

# Create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_kafka_topic()
    yield

# Create FastAPI
app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Products",
    description="This is a Products API with KAFKA and Protobuff",
    version="0.2.0",
    servers=[{
        "url": "http://127.0.0.1:9001",
        "description": "Development Server"
    }]
)

# include API Routers
app.include_router(router=product.router)
