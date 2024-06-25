from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)

BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_TOPIC = config("KAFKA_TOPIC", cast=str)
GROUP_ID = config("GROUP_ID", cast=str)

# TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)