import asyncio
from abc import ABCMeta, abstractmethod
from settings import Settings


class Job(metaclass=ABCMeta):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        return asyncio.run(self.run(*args, **kwargs))


# Jobs
from job.hello import HelloWorld, SlowWork, BadWork


JOB_ROUTER = {
    "HelloWorld": HelloWorld,
    "SlowWork": SlowWork,
    "BadWork": BadWork
}