from fastapi import APIRouter, HTTPException
import logging
from kafka_producer.models.model import Product, ProductUpdate
from kafka_producer.depandencies.depandency import KAFKA_VARIABLE, get_protobuf_data, get_protobuf_update
from kafka_producer import message_pb2
from kafka_producer.settings import KAFKA_TOPIC

# create external router
router = APIRouter(
    prefix="/products", # defines route of a route
    tags=["Product"], # defines title of routes
    responses={404: {
        "description" : "Not Found"
        }
    }
)

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create decorators
@router.get("/")
async def read_message():
    return {"message": "Welcome to 'Product Service'"}

@router.post("/")
async def create_product(
    fetch_data: Product, producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = get_protobuf_data(fetch_data)
        protobuf_data.operation = message_pb2.OperationType.CREATE
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"product": "created"}
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.delete("/{product_id}")
async def delete_product(
    product_id: str, producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = message_pb2.Product(
            id=int(product_id),
            operation=message_pb2.OperationType.DELETE
        )
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"product": "deleted"}
    except Exception as e:
        logger.error(f"Failed to delete product: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete product")

@router.patch("/{product_id}")
async def update_product(
    product_id: str, fetch_data: ProductUpdate, producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = message_pb2.Product(
            id=int(product_id),
            operation=message_pb2.OperationType.UPDATE
        )
        update_data = get_protobuf_update(fetch_data)
        protobuf_data.MergeFrom(update_data)
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"product": "updated"}
    except Exception as e:
        logger.error(f"Failed to update product: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")
