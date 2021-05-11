from typing import Any
from pydantic import BaseModel
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import Executable


class BaseManager:

    model: Any = None

    @staticmethod
    async def fetch(db: AsyncSession, stmt: Executable) -> Result:
        return await db.execute(stmt)

    @classmethod
    def add_to_session(cls, db: AsyncSession, obj: 'BaseModel'):
        '''
        We will let the parent methods manage the session commit and rollback
        This will allow method compossition with just one session.
        Example here: https://stribny.name/blog/fastapi-asyncalchemy/
        '''
        new_obj = cls.model(**obj.dict())
        db.add(new_obj)
        return new_obj
