from fastapi import APIRouter, HTTPException
import logging
from kafka_producer import message_pb2
from kafka_producer.settings import KAFKA_TOPIC
from kafka_producer.models.model import Order, OrderUpdate
from kafka_producer.depandencies.depandency import KAFKA_VARIABLE, get_protobuf_data, get_protobuf_update

# create external router
router = APIRouter(
    prefix="/orders",
    tags=["Order"],
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
    return {"message": "Welcome to Order Service"}

@router.post("/")
async def create_order(
    fetch_data: Order,
    producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = get_protobuf_data(fetch_data)
        protobuf_data.operation = message_pb2.OperationType.CREATE
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"order": "created"}
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.delete("/{order_id}")
async def delete_order(
    order_id: str,
    producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = message_pb2.Order(
            id=int(order_id),
            operation=message_pb2.OperationType.DELETE
        )
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"order": "deleted"}
    except Exception as e:
        logger.error(f"Failed to delete order: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete order")

@router.patch("/{order_id}")
async def update_order(
    order_id: str,
    fetch_data: OrderUpdate,
    producer: KAFKA_VARIABLE
):
    try:
        protobuf_data = message_pb2.Order(
            id=int(order_id),
            operation=message_pb2.OperationType.UPDATE
        )
        update_data = get_protobuf_update(fetch_data)
        protobuf_data.MergeFrom(update_data)
        serialized_data = protobuf_data.SerializeToString()
        await producer.send_and_wait(str(KAFKA_TOPIC), serialized_data)
        return {"order": "updated"}
    except Exception as e:
        logger.error(f"Failed to update order: {e}")
        raise HTTPException(status_code=500, detail="Failed to update order")
