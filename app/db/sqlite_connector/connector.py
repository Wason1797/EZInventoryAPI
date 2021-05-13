from app.utils.env_config import EnvConfig

from ..base_connector import BaseConnector


class SqLiteConnector(BaseConnector):
    DB_URL: str = EnvConfig.TESTING_DB_URL
