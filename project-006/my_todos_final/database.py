from my_todos_final import settings
from sqlmodel import create_engine, Session

# create server connection (only one engine for whole application)
conn_str: str = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(
    conn_str, 
    connect_args={"sslmode": "require"}, 
    pool_recycle=300, 
    pool_size=10,
    echo=True
)

# create session (separate session for each functionality/transaction)
def get_session():
    with Session(engine) as session:
        yield session