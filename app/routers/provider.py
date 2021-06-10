
from app.db.postgre_connector import PostgreSqlConnector
from app.managers.provider import ProviderManager
from app.serializers.provider import ProviderCreate as ProviderCreateSerializer
from app.serializers.provider import ProviderUpdate as ProviderUpdateSerializer
from app.serializers.provider import Provider as ProviderSerializer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.functions import filter_dict_keys

router = APIRouter()


@router.get('/{uuid}', response_model=ProviderSerializer)
async def get_provider(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=ProviderSerializer)
async def create_provider(provider: ProviderCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.create_provider(db, provider)


@router.patch('', response_model=ProviderSerializer)
async def basic_provider_update(provider: ProviderUpdateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    update_values = filter_dict_keys(provider.dict(), {'uuid'}, prune_null=True)
    return await ProviderManager.update_provider_by_uuid(db, provider.uuid, update_values)


@router.delete('/{uuid}', response_model=ProviderSerializer)
async def delete_provider(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.delete_provider(db, uuid)
