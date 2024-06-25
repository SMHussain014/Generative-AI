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
        yield
    finally:
        await producer.stop()

# creating Kafka_variable to be used as a dependency
KAFKA_VARIABLE = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]

# Calling function for Protobuf
def get_protobuf_data(new_data):
    return message_pb2.Product(
        id=new_data.id,
        name=new_data.name,
        description=new_data.description,
        price=new_data.price,
        category=new_data.category,
        brand=new_data.brand,
        color=new_data.color,
        weight=new_data.weight,
        stock=new_data.stock,
        sku=new_data.sku
    )

# Calling function for Protobuf
def get_protobuf_update(new_update):
    return message_pb2.Product(
        name=new_update.name,
        description=new_update.description,
        price=new_update.price,
        category=new_update.category,
        brand=new_update.brand,
        color=new_update.color,
        weight=new_update.weight,
        stock=new_update.stock,
        sku=new_update.sku
    )
