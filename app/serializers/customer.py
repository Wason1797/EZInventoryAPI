from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr

from .base import BaseTable, Address
from app.utils.constants import DniTypes


class Customer(BaseTable):
    uuid: UUID
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: dict


class CustomerCreate(BaseModel):
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: Optional[str]
    meta: Optional[dict]