import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(os.getenv('DB_URL'), future=True, echo=True)
db_pool = async_sessionmaker(engine, expire_on_commit=False)