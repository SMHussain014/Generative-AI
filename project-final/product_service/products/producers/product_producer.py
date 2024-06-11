from products import settings
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError, KafkaConnectionError

MAX_RETRIES = 5
RETRY_INTERVALS = 10 
async def create_kafka_topic():
    admin_client = AIOKafkaAdminClient(bootstrap_servers=str(settings.BOOTSTRAP_SERVER))
    retries = 0
    while retries < MAX_RETRIES:
        try:
            await admin_client.start()
            topic_list = [NewTopic(name=str(settings.KAFKA_PRODUCTS_TOPIC), num_partitions=1, replication_factor=1)]
            try:
                await admin_client.create_topics(new_topics=topic_list, validate_only=False)
                print("Topic created successfully!")
            except TopicAlreadyExistsError:
                print("Topic already exists")
            finally:
                await admin_client.close()
            return
        except KafkaConnectionError:
            retries += 1
            print(f"Kafka connection failed, retrying {retries}/{MAX_RETRIES} ...")
            await asyncio.sleep(RETRY_INTERVALS)
    raise Exception("Failed to connect with kafka broker after serveral reties")