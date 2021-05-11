from .base import BaseManager
from typing import Union
from app.utils.constants import StatusConstants
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ezinventory_models import User


class UserManager(BaseManager):
    model = User

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filter_status: str = StatusConstants.DELETED) -> Union[User, None]:
        query = select(User).where(User.uuid == uuid, User.status != filter_status)
        result = await cls.fetch(db, query)
        return result.one_or_none()
