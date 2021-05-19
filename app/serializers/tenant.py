from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, validator, EmailStr

from .base import BaseTable, Address


class Tenant(BaseTable):
    uuid: UUID
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str


class TenantCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: str
    description: str
