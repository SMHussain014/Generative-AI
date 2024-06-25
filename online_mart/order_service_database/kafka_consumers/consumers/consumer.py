import logging
from aiokafka import AIOKafkaConsumer
from kafka_consumers import message_pb2
from kafka_consumers.settings import KAFKA_TOPIC, BOOTSTRAP_SERVER, GROUP_ID
from kafka_consumers.models.model import Order, OrderUpdate
from kafka_consumers.depandencies.depandency import get_session
# from products.curd.product_curd import add_new_product
# from products_consumers.database import engine
# from sqlmodel import Session

# configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_message():
    consumer = AIOKafkaConsumer(
            str(KAFKA_TOPIC), 
            bootstrap_servers=str(BOOTSTRAP_SERVER), 
            group_id=str(GROUP_ID)
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic {msg.topic}")
            serialized_data = message_pb2.Order()
            serialized_data.ParseFromString(msg.value)
            logger.info(f"Consumer's Deserialized data -> {serialized_data}")
            with next(get_session()) as session:
                # with Session(engine) as session:
                print("SAVING DATA TO DATABASE")
                try:
                    if serialized_data.operation == message_pb2.OperationType.CREATE:
                        new_data = Order(
                            id=serialized_data.id,
                            product_id=serialized_data.product_id,
                            user_id=serialized_data.user_id,
                            quantity=serialized_data.quantity,
                            amount=serialized_data.amount,
                            status=serialized_data.status
                        )
                        session.add(new_data)
                        session.commit()
                        session.refresh(new_data)
                        logger.info(f"Order added to Database -> {new_data}")
                    elif serialized_data.operation == message_pb2.OperationType.UPDATE:
                        # existing_product = session.get(Order, order_data.id)
                        existing_data = session.query(Order).filter_by(id=serialized_data.id).first()
                        if existing_data:
                            # Update only the fields that are present and non-empty
                            for field_name in ['product_id', 'user_id', 'quantity', 'amount', 'status']:
                                if hasattr(serialized_data, field_name) and getattr(serialized_data, field_name):
                                    setattr(existing_data, field_name, getattr(serialized_data, field_name))
                            session.commit()
                            session.refresh(existing_data)
                            logger.info(f"Order updated in Database -> {existing_data}")
                        else:
                            logger.warning(f"Order with ID {serialized_data.id} not found in Database for updation")
                    elif serialized_data.operation == message_pb2.OperationType.DELETE:
                        existing_data = session.query(Order).filter_by(id=serialized_data.id).first()
                        if existing_data:
                            session.delete(existing_data)
                            session.commit()
                            logger.info(f"Order deleted from Database -> {existing_data}")
                        else:
                            logger.warning(f"Order with ID {serialized_data.id} not found in Database for deletion")
                    else:
                        logger.warning(f"Unknown Operation Type -> {serialized_data.operation}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    session.rollback()
                finally:
                    session.close()
    finally:
        await consumer.stop()
