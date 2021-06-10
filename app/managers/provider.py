from datetime import datetime
from typing import Union

from app.models.ezinventory_models import Provider
from app.serializers.provider import ProviderCreate
from app.utils.constants import StatusConstants
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager


class ProviderManager(BaseManager):
    model = Provider
    columns = Provider.__table__.columns

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Provider, None]:
        query = select(Provider).where(Provider.uuid == uuid, Provider.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def create_provider(cls, db: AsyncSession, provider: ProviderCreate) -> Union[Provider, None]:
        db_role = cls.add_to_session(db, Provider(**provider.dict()))

        await db.commit()
        await db.refresh(db_role)
        return db_role

    @classmethod
    async def update_provider_by_uuid(cls, db: AsyncSession, uuid: str, update_values: dict) -> Union[Provider, None]:
        query = update(Provider)\
            .where(Provider.uuid == uuid)\
            .values(**update_values)
        result = await cls.execute_update_stmt_by_uuid(db, query, cls.columns, cls.fetch_by_uuid, uuid)
        return result

    @classmethod
    async def delete_provider(cls, db: AsyncSession, uuid: str) -> dict:
        return await cls.uppdate_provider_by_uuid(db, uuid, {'status': StatusConstants.DELETED,
                                                             'deleted_on': datetime.utcnow()})
