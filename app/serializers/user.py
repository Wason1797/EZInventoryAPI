from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .base import BaseTable


class User(BaseTable):
    uuid: UUID
    username: str
    password: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    tenant_uuid: UUID
    roles: Optional[List[UUID]]
    username: str
    password: str
    email: str
    phone: str
