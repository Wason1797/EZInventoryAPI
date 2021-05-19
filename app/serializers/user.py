from .base import BaseTable
from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import List
<< << << < HEAD

== == == =

>>>>>> > develop


class User(BaseTable):
    uuid: UUID
    username: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    tenant_uuid: UUID
    roles: List[UUID]
    username: str
    password: str
    email: EmailStr
    phone: str
