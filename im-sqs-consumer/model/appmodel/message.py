from uuid import uuid4
from typing import Any, Dict
from pydantic import BaseModel, field_validator
from controller.job.exception import InvalidVersion, InvalidCreator
from controller.util import utc_now


class MessageV1Job(BaseModel):
    name: str
    param: Dict[str, Any]


class MessageV1(BaseModel):
    version: int = 1
    job: MessageV1Job
    job_id: str = str(uuid4())
    retry: int = 0
    creator: str = "nepto-task-queue-worker"
    created_at: str = utc_now().isoformat()

    @field_validator("version")
    def version_valid(cls, version: int):
        if version != 1:
            raise InvalidVersion(version)
        return version

    @field_validator("creator")
    def creator_valid(cls, creator: str):
        # Check creator is valid
        return creator
