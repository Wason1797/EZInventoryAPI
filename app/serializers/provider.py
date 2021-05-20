from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr

from .base import BaseTable, Address


class Provider(BaseTable):
    uuid: UUID
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: dict


class ProviderCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[dict]
