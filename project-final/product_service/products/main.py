from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager
from products.database import engine
import asyncio
from products.consumers.product_consumer import consume_products
from products import settings
from products.models.product_model import Product, ProductUpdate
from products.depandencies.product_depandency import get_session, get_kafka_producer
from products.curd.product_curd import add_new_product, get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id, validate_product_by_id
from products.producers.product_producer import create_kafka_topic
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from products import products_pb2

# Now create real time tables with the help of engine
def create_tables() -> None:
    SQLModel.metadata.create_all(engine)

# create sequence of transactions
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_kafka_topic()
    task1 = asyncio.create_task(
        consume_products(
            mytopics1=str(settings.KAFKA_PRODUCTS_TOPIC), 
            myserver1=str(settings.BOOTSTRAP_SERVER)
        )
    )
    print("Consumer created successfully ...")
    create_tables()
    print("Creating Tables ...")
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

@app.post("/manage-products/", response_model=Product)
async def create_new_product(
    product: Product, 
    session: Annotated[Session, Depends(get_session)], 
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    products_protobuf = products_pb2.Product(
        id = product.id,
        name = product.name,
        description = product.description,
        price = product.price,
        expiry = product.expiry,
        brand = product.brand,
        weight = product.weight,
        category = product.category,
        sku = product.sku
    )
    products_protobuf.operation = products_pb2.OperationType.CREATE
    serialized_products = products_protobuf.SerializeToString()
    await producer.send_and_wait(str(settings.KAFKA_PRODUCTS_TOPIC), serialized_products)
    # new_product = add_new_product(product, session)
    return product

@app.get("/manage-products/all", response_model=list[Product])
def get_products(session: Annotated[Session, Depends(get_session)]):
    return get_all_products(session)

@app.get("/manage-products/{product_id}", response_model=Product)
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/manage-products/{product_id}", response_model=dict)
def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/manage-products/{product_id}", response_model=Product)
def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))