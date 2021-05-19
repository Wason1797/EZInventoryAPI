from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Json, validator, AnyURL

from .base import BaseTable


class Product(BaseTable):
    uuid: UUID
    tenant_uuid: UUID
    category: str
    name: str
    description: str
    public_unit_price: int
    provicer_unit_price: int
    current_stock: int
    reorder_level: int
    reorder_ammount: int
    picture_path: AnyURL
    meta: Json


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
    picture_path: Optional[AnyURL]
    meta: Optional[Json]
    initial_stock: int
