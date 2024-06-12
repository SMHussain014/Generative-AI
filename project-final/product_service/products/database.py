from products import settings
from sqlmodel import create_engine

# create server connection (only one engine for whole application)
conn_str: str = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(
    conn_str, 
    connect_args={}, 
    # pool_recycle=300, 
    # pool_size=10,
    # echo=True
)
