from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from env import DB_URI

engine = create_engine(DB_URI, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base: DeclarativeBase = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()