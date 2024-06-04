from typing import Optional
from pydantic import BaseModel
from controller.task_queue.queue import TaskQueue
from model import mongodb
from model.mongodb import MongoDBConnection
from settings import Settings


class ConsumerModules(BaseModel):
    task_queue: Optional[TaskQueue] = None
    idempotent: bool

    class Config:
        arbitrary_types_allowed = True


def _get_nepto_mongodb_connection(
    mongodb_uri: str,
    mongodb_db_name: str,
) -> MongoDBConnection:
    client = mongodb.get_client(mongodb_uri)
    db = client[mongodb_db_name]
    return MongoDBConnection(client=client, db=db)


def _get_task_queue(queue_name: str, settings: Settings) -> TaskQueue:
    return TaskQueue(
        queue_name,
        settings.sqs_access_key_id,
        settings.sqs_secret_access_key,
        settings.sqs_region_name,
    )


def get_consumer_modules(queue_name: str, settings: Settings) -> ConsumerModules:
    return ConsumerModules(
        task_queue=_get_task_queue(queue_name, settings),
        idempotent=True,
    )


def get_all_consumer_modules(settings: Settings) -> ConsumerModules:
    """Get all consumer modules for Test"""
    return ConsumerModules(
        idempotent=True,
    )
