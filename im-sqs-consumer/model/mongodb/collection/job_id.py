from pymongo import IndexModel, ASCENDING
from model.mongodb.collection import Model, Schema


class JobIdSchema(Schema):
    queue_name: str
    job_name: str
    job_id: str


class JobId(Model):

    def indexes(self) -> list[IndexModel]:
        return [
            IndexModel([('job_id', ASCENDING)], unique=True, expireAfterSeconds=3600),
        ]

    async def insert_one(
        self, document: JobIdSchema
    ):
        return await self.col.insert_one(
            document.model_dump(by_alias=True)
        )
