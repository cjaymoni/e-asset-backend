from pydantic import BaseSettings
from pathlib import Path
from babel import Locale
import os

BASE_DIR = Path(__file__).resolve().parent

ALLOWED_ORIGINS = ["*"]
ALLOWED_HEADERS = ["*"]
ALLOWED_METHODS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

os.environ['DOC'] = ''

JWT_ALGORITHM = 'HS256'

class Settings(BaseSettings):
    API_KEY: str
    BASE_URL: str
    ADMIN_EMAIL: str
    DATABASE_URL: str
    VERSION: str = '2.0.0'
    RESET_PASSWORD_PATH: str
    ACCOUNT_ACTIVATION_PATH: str
    MEDIA_FILE_BUCKET: str = None
    APP_NAME: str = "e-Asset api service"
    TWILIO_PHONE_NUMBER: str = '+16196584362'
    TWILIO_AUTH_TOKEN: str = '7b6c506ee07337cc3d02536d5119c4b2'
    TWILIO_ACCOUNT_SID: str = 'AC959cbde01aced5669b0121ffea2df117'
    SECRET: str = "I2YsMiClydMj9lCGkIsnSuM7NP7Wm7ilwRlBGKPNOl5UBQtl7mIcka9MKgvf"
    APP_DESCRIPTION: str = """eAsset API Documentation developed by Eli for Some Organization"""
    APP_DOC_DESC: str = f"{APP_DESCRIPTION}\n\n <a href='/' style='color:hotpink;cursor:help'>see official API docs</a>"
    APP_REDOC_DESC: str = f"{APP_DESCRIPTION}\n\n <a href='/docs' style='color:hotpink;cursor:help'>Interactive Swagger docs</a>"
    ACCESS_TOKEN_DURATION_IN_MINUTES: float = 60
    REFRESH_TOKEN_DURATION_IN_MINUTES: float = 60
    DEFAULT_TOKEN_DURATION_IN_MINUTES: float = 15
    RESET_TOKEN_DURATION_IN_MINUTES: float = 15
    ACTIVATION_TOKEN_DURATION_IN_MINUTES: float = 15

    class Config:
        env_file = ".env"
        secrets_dir = BASE_DIR

settings = Settings()

if settings.MEDIA_FILE_BUCKET:
    pass
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

    DOCUMENT_URL = "/docs/"
    DOCUMENT_ROOT = os.path.join(BASE_DIR, 'documents/')

    LOG_ROOT = os.path.join(BASE_DIR, 'logs/')

    if not os.path.isdir(DOCUMENT_ROOT):
        os.mkdir(DOCUMENT_ROOT)

    if not os.path.isdir(MEDIA_ROOT):
        os.mkdir(MEDIA_ROOT)

    if not os.path.isdir(LOG_ROOT):
        os.mkdir(LOG_ROOT)

locale = Locale('en', 'US')