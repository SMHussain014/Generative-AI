from sqlmodel import Session, SQLModel
from kafka_consumers.database import engine

# create session (separate session for each functionality/transaction)
def get_session():
    with Session(engine) as session:
        yield session

# Now create real time tables with the help of engine
def create_tables() -> None:
    SQLModel.metadata.create_all(engine)