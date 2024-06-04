import pytz
from datetime import datetime
from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from bson.codec_options import CodecOptions
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import Field, BaseModel, ConfigDict, field_serializer


class Schema(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    version: int = Field(default=1, alias="__version__")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class EmbeddedSchema(BaseModel):
    """
    ObjectId Base Model (ObjectId Field를 위한 Config 중복 방지)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Model(metaclass=ABCMeta):

    def __init__(self, db: AsyncIOMotorDatabase):
        if not isinstance(db, AsyncIOMotorDatabase):
            raise TypeError('db must be AsyncIOMotorDatabase')
        self.col: AsyncIOMotorCollection = db[self.__class__.__name__]
        self.col = self.col.with_options(
            codec_options=CodecOptions(
                tz_aware=True,
                tzinfo=pytz.utc
            )
        )

    def indexes(self) -> list:
        """Collection indexes"""
        return []

    def create_indexes(self):
        """Create index"""
        indexes = self.indexes()
        if indexes:
            self.col.create_indexes(indexes)

    @staticmethod
    def _p(*args) -> dict:
        """projection shortcut method"""
        return {'_id': 0, **{field: 1 for field in args}}


from .job_id import JobId, JobIdSchema
