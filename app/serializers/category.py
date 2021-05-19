from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Json, validator, AnyURL

from .base import BaseTable


class Category(BaseTable):
    uuid: UUID
    name: str
    description: str


class CategoryCreate(BaseModel):
    name: str
    descrition: str
