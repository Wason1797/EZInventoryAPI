from typing import Union
from datetime import datetime

from app.models.ezinventory_models import Product, Stock, OperationConstants
from app.serializers.product import ProductCreate
from app.utils.constants import StatusConstants
from app.utils.functions import filter_dict_keys
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager


class ProductManager(BaseManager):
    model = Product

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Product, None]:
        query = select(Product).where(Product.uuid == uuid, Product.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def add_first_stock_entry(cls, db:AsyncSession, product_uuid: str, initial_stock: int):
        initial_stock_entry = [
            Stock(
                product_uuid=product_uuid,
                current_ammount=initial_stock,
                changed_by=initial_stock,
                operation=OperationConstants.ADD
            )
        ]
        return cls.add_to_session(db, initial_stock_entry)

    @classmethod
    async def create_product(cls, db: AsyncSession, product: ProductCreate) -> Union[Product, None]:
        product_dict = filter_dict_keys(product.dict(), {'initial_stock', 'provider_uuid'})
        db_product = cls.add_to_session(db, Product(**product_dict))
        
        await db.flush()
        await cls.add_first_stock_entry(db, db_product.uuid, product.initial_stock)

        await db.commit()
        await db.refresh(db_product)
        return db_product

    @classmethod
    async def uppdate_product_by_uuid(cls, db: AsyncSession, uuid: str, update_values: dict) -> Union[dict, Product]:
        query = update(Product)\
            .where(Product.uuid == uuid)\
            .values(**update_values)

        await cls.execute_stmt(db, query)
        await db.commit()
        result = await cls.fetch_by_uuid(db, uuid, filter_status=None)
        return result
    
    @classmethod
    async def delete_product(cls, db: AsyncSession, uuid: str) -> dict:
        return await cls.uppdate_product_by_uuid(db, uuid, {'status': StatusConstants.DELETED,
                                                         'deleted_on': datetime.utcnow()})