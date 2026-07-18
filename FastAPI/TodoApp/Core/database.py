from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase
from .config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL, pool_size=10, echo = False,
                    pool_pre_ping=True,
                    max_overflow=20,
                    pool_recycle=1800) # here check_same_thread is set to false so all conn will be working on their separate thread and no same thread will be used to serve multiple request
AsyncSessionLocal = async_sessionmaker(autoflush=False, class_=AsyncSession, bind = engine, expire_on_commit=False)