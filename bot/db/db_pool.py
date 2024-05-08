import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

engine = create_async_engine(os.getenv('DB_URL'), future=True, echo=False)
db_pool = async_sessionmaker(engine, expire_on_commit=False)