import uuid
from datetime import datetime

import sqlalchemy as sqla
from app.db.postgre_connector import PostgreSqlConnector
from app.utils.constants import StatusConstants
from passlib.hash import bcrypt
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import backref, relationship


class TemporalTracking(PostgreSqlConnector.Base):
    __abstract__ = True

    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    activated_on = sqla.Column(sqla.DateTime(), nullable=True)
    deleted_on = sqla.Column(sqla.DateTime(), nullable=True)
    reactivated_on = sqla.Column(sqla.DateTime(), nullable=True)


class Tenant(TemporalTracking):
    __tablename__ = 'tenant'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    main_address = sqla.Column(JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(30), nullable=False)
    description = sqla.Column(sqla.String(500))
    status = sqla.Column(sqla.Enum(StatusConstants))

    def __repr__(self) -> str:
        return f'Tenant[{self.uuid}] {self.name}'


class User(TemporalTracking):
    __tablename__ = 'user'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = sqla.Column(sqla.String(100), nullable=False, unique=True, index=True)
    password = sqla.Column(sqla.String(300), nullable=False)
    email = sqla.Column(sqla.String(30), nullable=False)
    phone = sqla.Column(sqla.String(15))
    status = sqla.Column(sqla.Enum(StatusConstants))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.password:
            self.password = bcrypt.hash(self.password)

    def __repr__(self) -> str:
        return f'User[{self.uuid}] {self.name}'

    def validate_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def set_password(self, password: str) -> None:
        if password:
            self.password = bcrypt.hash(password)


class Role(PostgreSqlConnector.Base):
    __tablename__ = 'role'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    permissions = sqla.Column(JSON(none_as_null=False), nullable=False)
    status = sqla.Column(sqla.Enum(StatusConstants))

    def __repr__(self) -> str:
        return f'Role[{self.uuid}] {self.name}'


class UserRolesByTenant(PostgreSqlConnector.Base):
    __tablename__ = 'user_roles_by_tenant'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('tenant.uuid'))
    user_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('user.uuid'))
    role_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('role.uuid'))
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)

    user = relationship(
        'User',
        primaryjoin=f"and_(UserRolesByTenant.user_uuid==User.uuid, User.status!='{StatusConstants.DELETED}')",
        backref=backref('roles', order_by=user_uuid))
