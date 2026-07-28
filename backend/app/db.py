from sqlmodel import SQLModel, create_engine, Session
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'db')
DB_DIR = os.path.abspath(DB_DIR)
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR, exist_ok=True)

sqlite_file_name = os.path.join(DB_DIR, 'crops.db')
sqlite_url = f"sqlite:///{sqlite_file_name}"

# echo=False to keep logs tidy; set echo=True for SQL debugging
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
