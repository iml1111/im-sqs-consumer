"""
https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
https://www.mongodb.com/developer/languages/python/farm-stack-fastapi-react-mongodb/
"""
from collections import namedtuple
from motor.motor_asyncio import AsyncIOMotorClient


MongoDBConnection = namedtuple(
    'MongoDBConnection',
    ['client', 'db']
)


def get_client(uri: str) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        uri,
        connect=False,
        minPoolSize=1,
        maxPoolSize=100,
    )
