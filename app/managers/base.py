from typing import Any, Coroutine, Iterable, Union

from app.utils.constants import DbDialects
from app.utils.functions import build_from_key_value_arrays
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import Executable


class BaseManager:

    model: Any = None

    @staticmethod
    async def execute_stmt(db: AsyncSession, stmt: Executable) -> Result:
        return await db.execute(stmt)

    @classmethod
    def add_to_session(cls, db: AsyncSession, obj: Any):
        '''
        We will let the parent methods manage the session commit and rollback
        This will allow method compossition with just one session.
        Example here: https://stribny.name/blog/fastapi-asyncalchemy/
        '''
        session_add = db.add_all if isinstance(obj, list) else db.add
        session_add(obj)
        return obj

    @classmethod
    async def execute_update_stmt_by_uuid(cls, db: AsyncSession, update_stmt: Executable, columns: Iterable,
                                          fetch_coro: Coroutine, uuid: str) -> Union[dict, type(model)]:
        if db.bind.dialect.name == DbDialects.POSTGRESQL.value:
            result = (await cls.execute_stmt(db, update_stmt.returning(*columns))).first()
            await db.commit()
            return build_from_key_value_arrays(columns.keys(), result)
        else:
            await cls.execute_stmt(db, update_stmt)
            await db.commit()
            result = await fetch_coro(db, uuid, filter_status=None)
            return result
