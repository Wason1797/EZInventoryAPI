from app.db import Base
from app.utils.env_manager import EnvManager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgreSqlConnector:
    engine = create_async_engine(EnvManager.DB_URL, echo=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    Base = Base

    @classmethod
    async def get_db(cls) -> AsyncSession:
        async with cls.SessionLocal() as session:
            yield session
