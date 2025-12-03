import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
print(sqlite_url)

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
