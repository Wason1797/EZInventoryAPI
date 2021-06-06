from typing import Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel

from .base import BaseTable


class Product(BaseTable):
    uuid: UUID
    name: str
    description: str
    public_unit_price: int
    provicer_unit_price: int
    reorder_level: int
    reorder_ammount: int
    picture_path: AnyUrl
    meta: Optional[dict]

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    tenant_uuid: UUID
    category_uuid: UUID
    provider_uuid: Optional[UUID]
    name: str
    description: str
    public_unit_price: int
    provicer_unit_price: int
    reorder_level: int
    reorder_ammount: int
    picture_path: Optional[AnyUrl]
    meta: Optional[dict]
    initial_stock: int