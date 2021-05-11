from datetime import datetime

from pydantic import BaseModel


class BaseTable(BaseModel):
    created_on: datetime
    updated_on: datetime
    status: str
    activated_on: datetime
    deleted_on: datetime
    reactivated_on: datetime
