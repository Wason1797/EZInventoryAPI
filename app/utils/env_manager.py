import os


class EnvManager:
    ENV: str = os.environ.get('ENV', 'DEV')
    DB_URL: str = os.environ.get('AUTH_API_DB_URL', '').strip()
    TESTING_DB_URL:  str = os.environ.get('TESTING_DB_URL', '').strip()
