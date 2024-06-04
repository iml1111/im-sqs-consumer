import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__AUTHOR__ = "IML"
__VERSION__ = "0.1.1"

APP_NAME = "IMSQSConsumer"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):

    # Basic settings
    app_name: str = Field(APP_NAME, env="APP_NAME")
    description: str = "IMSQS Consumer"
    contact_name: str = __AUTHOR__
    contact_url: str = "https://github.com/iml1111"
    contact_email: str = "shin10256@gmail.com"

    mongodb_uri: str
    mongodb_db_name: str

    sqs_access_key_id: str
    sqs_secret_access_key: str
    sqs_region_name: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR + '/.env',
        env_file_encoding='utf-8'
    )


class TestSettings(Settings):
    """Test Overriding settings"""
    test_mode: bool = True

    model_config = SettingsConfigDict(
        env_file=BASE_DIR + '/.test.env',
        env_file_encoding='utf-8'
    )
