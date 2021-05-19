from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Json, validator, AnyURL, EmailStr

from .base import BaseTable, Address


class Provider(BaseTable):
    uuid: UUID
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Json


class ProviderCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[Json]
