from sqlmodel import create_engine, Session, SQLModel
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ecomm.db')
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
