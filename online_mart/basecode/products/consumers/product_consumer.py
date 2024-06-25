from aiokafka import AIOKafkaConsumer
from products import settings
from products import products_pb2
from products.models.product_model import Product, ProductUpdate
# from products.curd.product_curd import add_new_product
from products.depandencies.product_depandency import get_session
# from products.database import engine
from sqlmodel import Session
import logging

# configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_products():
# async def consume_products(mytopics, myserver):
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
            # print("TYPE", (type(product_data)))
            # print(f"Consumer's Deserialized data -> {product_data}")
            logger.info(f"Consumer's Deserialized data -> {product_data}")

            with next(get_session()) as session:
            # with Session(engine) as session:
                print("SAVING DATA TO DATABSE")
                # db_insert_product = add_new_product(product_data=Product(**product_data), 
                #                                     session=session)
                # print("DB_INSERT_PRODUCT", db_insert_product)
                try:
                    if product_data.operation == products_pb2.OperationType.CREATE:
                        new_product = Product(
                            id = product_data.id,
                            name = product_data.name,
                            description = product_data.description,
                            price = product_data.price,
                            expiry = product_data.expiry,
                            brand = product_data.brand,
                            weight = product_data.weight,
                            category = product_data.category,
                            sku = product_data.sku
                        )
                        session.add(new_product)
                        session.commit()
                        session.refresh(new_product)
                        logger.info(f"Product added to Database -> {new_product}")
                    elif product_data.operation == products_pb2.OperationType.UPDATE:
                        existing_product = Session.query(Product).filter_by(id=product.id).first()
                        if existing_product:
                            existing_product.name = product.name,
                            existing_product.description = product.description,
                            existing_product.price = product.price,
                            existing_product.expiry = product.expiry,
                            existing_product.brand = product.brand,
                            existing_product.weight = product.weight,
                            existing_product.category = product.category,
                            existing_product.sku = product.sku
                            session.commit()
                            session.refresh(existing_product)
                            logger.info(f"Product updated in Database -> {existing_product}")
                        else:
                            logger.warning(f"Product with ID {product.id} not found in Database for updation")
                    elif product_data.operation == products_pb2.OperationType.DELETE:
                        existing_product = Session.query(Product).filter_by(id=product.id).first()
                        if existing_product:
                            session.delete(existing_product)
                            session.commit()
                            logger.info(f"Product deleted from Database -> {existing_product}")
                        else:
                            logger.warning(f"Product with ID {product.id} not found in Database for deletion")
                    else:
                        logger.warning(f"Unknown Operation Type -> {product.operation}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    session.rollback()
                finally:
                    session.close()
    finally:
        await consumer.stop()


# from aiokafka import AIOKafkaConsumer
# from products import settings
# from products import products_pb2
# from products.models.product_model import Product, ProductUpdate
# from products.depandencies.product_depandency import get_session
# from sqlmodel import Session
# import logging

# # configure the logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# async def consume_products():
#     consumer = AIOKafkaConsumer(
#         str(settings.KAFKA_PRODUCTS_TOPIC), 
#         bootstrap_servers=str(settings.BOOTSTRAP_SERVER), 
#         group_id=str(settings.GROUP_ID)
#     )
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             logger.info(f"Received message on topic {msg.topic}")
#             product_data = products_pb2.Product()
#             product_data.ParseFromString(msg.value)
#             logger.info(f"Consumer's Deserialized data -> {product_data}")
            
#             with next(get_session()) as session:
#                 try:
#                     if product_data.operation == products_pb2.OperationType.CREATE:
#                         new_product = Product(
#                             id=product_data.id,
#                             name=product_data.name,
#                             description=product_data.description,
#                             price=product_data.price,
#                             expiry=product_data.expiry,
#                             brand=product_data.brand,
#                             weight=product_data.weight,
#                             category=product_data.category,
#                             sku=product_data.sku
#                         )
#                         session.add(new_product)
#                         session.commit()
#                         session.refresh(new_product)
#                         logger.info(f"Product added to Database -> {new_product}")
                    
#                     elif product_data.operation == products_pb2.OperationType.UPDATE:
#                         existing_product = session.query(Product).filter_by(id=product_data.id).first()
#                         if existing_product:
#                             existing_product.name = product_data.name
#                             existing_product.description = product_data.description
#                             existing_product.price = product_data.price
#                             existing_product.expiry = product_data.expiry
#                             existing_product.brand = product_data.brand
#                             existing_product.weight = product_data.weight
#                             existing_product.category = product_data.category
#                             existing_product.sku = product_data.sku
#                             session.commit()
#                             session.refresh(existing_product)
#                             logger.info(f"Product updated in Database -> {existing_product}")
#                         else:
#                             logger.warning(f"Product with ID {product_data.id} not found in Database for update")
                    
#                     elif product_data.operation == products_pb2.OperationType.DELETE:
#                         existing_product = session.query(Product).filter_by(id=product_data.id).first()
#                         if existing_product:
#                             session.delete(existing_product)
#                             session.commit()
#                             logger.info(f"Product deleted from Database -> {existing_product}")
#                         else:
#                             logger.warning(f"Product with ID {product_data.id} not found in Database for deletion")
                    
#                     else:
#                         logger.warning(f"Unknown Operation Type -> {product_data.operation}")
                
#                 except Exception as e:
#                     logger.error(f"Error processing message: {e}")
#                     session.rollback()
#                 finally:
#                     session.close()
    
#     finally:
#         await consumer.stop()
