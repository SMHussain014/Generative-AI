from aiokafka import AIOKafkaConsumer
from products import settings
from products import products_pb2
from products.models.product_model import Product, ProductUpdate
from products.curd.product_curd import add_new_product
from products.depandencies.product_depandency import get_session
# from sqlmodel import Session

async def consume_products(mytopics, myserver):
    consumer = AIOKafkaConsumer(
            str(settings.KAFKA_PRODUCTS_TOPIC), 
            bootstrap_servers=str(settings.BOOTSTRAP_SERVER), 
            group_id=str(settings.GROUP_ID)
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic {msg.topic}")
            product_data = products_pb2.Product()
            product_data.ParseFromString(msg.value)
            print(f"Consumer's Deserialized data -> {product_data}")
            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_product = add_new_product(product_data=Product(**product_data), 
                                                    session=session)
                print("DB_INSERT_PRODUCT", db_insert_product)
    finally:
        await consumer.stop()
