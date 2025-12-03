# Create Engine is responsibe for managing the db connections and db pooling and it should be created once per app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()