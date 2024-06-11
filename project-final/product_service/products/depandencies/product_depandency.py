from sqlmodel import Session
from products.database import engine
from aiokafka import AIOKafkaProducer
from products import settings

# create session (separate session for each functionality/transaction)
def get_session():
    with Session(engine) as session:
        yield session

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
