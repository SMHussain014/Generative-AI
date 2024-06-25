from aiokafka import AIOKafkaProducer
from kafka_producer.settings import BOOTSTRAP_SERVER
from fastapi import Depends
from typing import Annotated
from kafka_producer import message_pb2

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=str(BOOTSTRAP_SERVER))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

# creating Kafka_variable to be used as a dependency
KAFKA_VARIABLE = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]

# Calling function for Protobuf
def get_protobuf_data(new_data):
    return message_pb2.Order(
        id=new_data.id,
        product_id=new_data.product_id,
        user_id=new_data.user_id,
        amount=new_data.amount,
        status=new_data.status
    )

# Calling function for Protobuf
def get_protobuf_update(new_update):
    return message_pb2.Order(
        quantity=new_update.quantity,
        amount=new_update.amount
    )
