from app.auth_test import authenticate_user
from datetime import datetime, timedelta
from typing import Optional

from app.utils.env_config import EnvConfig
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends
from jose import jwt, JWTError

from .exeptions import NotEnoughPermissionsError, InvalidCredentialsError


class JWTFunctions:
    SECRET_KEY: str = EnvConfig.SECRET_KEY
    ALGORITHM: str = 'HS256'
    DEFAULT_EXPIRE_DELTA: int = 15

    @classmethod
    def create_access_token(cls, data: dict, expire_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + timedelta(expire_delta or cls.DEFAULT_EXPIRE_DELTA)
        data_to_encode = {**data, 'exp': expire}
        return jwt.encode(data_to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])


class AuthFunctions:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    @classmethod
    async def check_user_permissions(cls, permissions: SecurityScopes, token: str = Depends(oauth2_scheme)) -> dict:
        authenticate_header = f'Bearer {"scope="+permissions.scope_str if permissions.scopes else ""}'.strip()

        try:
            decoded_token = JWTFunctions.decode_token(token)
        except JWTError:
            raise InvalidCredentialsError(authenticate_header)

        if decoded_token.get('sub') is None:
            raise InvalidCredentialsError(authenticate_header)

        if not (permissions_by_tenant := decoded_token.get('permissions', {})):
            raise NotEnoughPermissionsError(authenticate_header)

        scope_set = set(permissions.scopes)
        valid_permissions_by_tenant = {tenant_uuid: permission
                                       for tenant_uuid, permission in permissions_by_tenant.items()
                                       if set(permission).issubset(scope_set)}

        if not valid_permissions_by_tenant:
            raise NotEnoughPermissionsError(authenticate_user)

        return valid_permissions_by_tenant
