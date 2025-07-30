import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./books.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
