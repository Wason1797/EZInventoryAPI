import uuid
from datetime import datetime

import sqlalchemy as sqla
from app.db.postgre_connector import PostgreSqlConnector
from app.utils.constants import DniTypes, OperationConstants, StatusConstants
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
        backref=backref('roles_by_tenant', order_by=user_uuid))


class PermisionTemplate(PostgreSqlConnector.Base):
    __tablename__ = 'permision_template'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False, unique=True)
    detail = sqla.Column(sqla.String(500), nullable=True)
    resources = sqla.Column(JSON(none_as_null=False), nullable=False)


class ProductBase(TemporalTracking):
    __abstract__ = True

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    description = sqla.Column(sqla.String(500))
    # NOTE: We store prices as an integer ammount of cents to avoid presicion errors
    public_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    provicer_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    reorder_level = sqla.Column(sqla.Integer(), nullable=True)
    reorder_ammount = sqla.Column(sqla.Integer(), nullable=True)
    picture_path = sqla.Column(sqla.String(500))
    meta = sqla.Column(JSON(none_as_null=False), nullable=False)
    status = sqla.Column(sqla.Enum(StatusConstants))


class ProductTemplate(ProductBase):
    __tablename__ = 'product_template'


class Product(ProductBase):
    __tablename__ = 'product'

    tenant_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('tenant.uuid'))
    category_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('category.uuid'))

    tenant = relationship(
        'Tenant',
        primaryjoin=f"and_(Product.tenant_uuid==Tenant.uuid, Tenant.status!='{StatusConstants.DELETED}')",
        backref=backref('products', order_by=uuid))

    category = relationship(
        'Category',
        primaryjoin=f"and_(Product.category_uuid==Category.uuid, Category.status!='{StatusConstants.DELETED}')",
        backref=backref('products', order_by=uuid))


class Stock(PostgreSqlConnector.Base):
    __tablename__ = 'stock'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('product.uuid'))
    current_ammount = sqla.Column(sqla.Integer(), nullable=False)
    changed_by = sqla.Column(sqla.Integer(), nullable=False)
    operation = sqla.Column(sqla.Enum(OperationConstants))
    updated_at = sqla.Column(sqla.DateTime(), default=datetime.utcnow)


class Category(TemporalTracking):
    __tablename__ = 'category'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    description = sqla.Column(sqla.String(500))
    status = sqla.Column(sqla.Enum(StatusConstants))


class Provider(TemporalTracking):
    __tablename__ = 'provider'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    main_address = sqla.Column(JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(30), nullable=False)
    description = sqla.Column(sqla.String(500))
    status = sqla.Column(sqla.Enum(StatusConstants))
    meta = sqla.Column(JSON(none_as_null=False), nullable=True)


class ProductProviders(PostgreSqlConnector.Base):
    __tablename__ = 'product_providers'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    product_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('product.uuid'))
    provider_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('provider.uuid'))

    product = relationship(
        'Product',
        primaryjoin=f"and_(ProductProviders.product_uuid==Product.uuid, Product.status!='{StatusConstants.DELETED}')",
        backref=backref('providers', order_by=uuid))

    provider = relationship(
        'Provider',
        primaryjoin=f"and_(ProductProviders.provider_uuid==Provider.uuid, Provider.status!='{StatusConstants.DELETED}')",
        backref=backref('products', order_by=uuid))


class Customer(TemporalTracking):
    __tablename__ = 'customer'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    dni = sqla.Column(sqla.String(20), nullable=False)
    dni_type = sqla.Column(sqla.Enum(DniTypes))
    main_address = sqla.Column(JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(30), nullable=False)
    description = sqla.Column(sqla.String(500))
    status = sqla.Column(sqla.Enum(StatusConstants))
    meta = sqla.Column(JSON(none_as_null=False), nullable=True)


class Invoice(TemporalTracking):
    __tablename__ = 'invoice'

    uuid = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('product.uuid'))
    customer_uuid = sqla.Column(UUID(as_uuid=True), sqla.ForeignKey('provider.uuid'))
    product_ammount = sqla.Column(sqla.Integer(), nullable=False)
    # NOTE: We store prices as an integer ammount of cents to avoid presicion errors
    product_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    meta = sqla.Column(JSON(none_as_null=False), nullable=True)

    product = relationship(
        'Product',
        backref=backref('invoices', order_by=uuid))

    customer = relationship(
        'Customer',
        backref=backref('invoices', order_by=uuid))
