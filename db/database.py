# Description: Database configuration file.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define the database file path
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"


# Create a database engine instance
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# Create a session maker instance for the database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for the database models
Base = declarative_base()


#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()