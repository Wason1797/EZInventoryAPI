from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Json, validator, AnyURL, EmailStr

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
    meta: Json


class CustomerCreate(BaseModel):
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: Optional[str]
    meta: Optional[Json]