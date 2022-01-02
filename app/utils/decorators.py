from typing import Callable
from functools import wraps
from app.models.ezinventory_models import ActionLog
from app.managers.base import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession

def log_action(action_name:str):

    def decorator_log_action(func):
        @wraps(func)
        async def wrapper_log_action(cls: BaseManager, db: AsyncSession, action_user_uuid:str, *args, **kwargs):
            action_log = {
                "action": action_name,
            } 
            if action_user_uuid:
                action_log["user_uuid"]: action_user_uuid

            db_category = cls.add_to_session(db, ActionLog(**action_log))
            await db.commit()
            await db.refresh(db_category)

            return await func(cls, db, action_user_uuid, *args, **kwargs)
        
        return wrapper_log_action

    return decorator_log_action
