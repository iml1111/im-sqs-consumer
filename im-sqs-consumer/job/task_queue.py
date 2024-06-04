from typing import Optional
import traceback
from loguru import logger
from pymongo.errors import DuplicateKeyError
from job import Job, JOB_ROUTER
from controller.job.exception import UnknownJob, InvalidVersion, InvalidCreator
from controller.job.util import convert_param, Timer
from controller.task_queue.queue import TaskQueue
from controller.task_queue.module import get_consumer_modules, ConsumerModules
from model.appmodel.message import MessageV1
from model.mongodb import get_client
from model.mongodb.collection.job_id import JobId, JobIdSchema


class Consumer(Job):

    async def run(self, queue_name: str, timeout: Optional[int] = None):
        mongodb_cli = get_client(self.settings.mongodb_uri)
        mongodb_db = mongodb_cli[self.settings.mongodb_db_name]
        timeout, converted = convert_param(timeout, int)
        timer = Timer(enabled=timeout is not None)
        wait_secs = 20

        task_queue = TaskQueue(
            queue_name,
            self.settings.sqs_access_key_id,
            self.settings.sqs_secret_access_key,
            self.settings.sqs_region_name,
        )
        modules: ConsumerModules = get_consumer_modules(queue_name, self.settings)
        job_id_model = JobId(mongodb_db)

        while (
            (converted and timer.elapsed < timeout)
            or timeout is None
        ):
            if converted:
                # noinspection PyUnresolvedReferences
                wait_secs = int(timeout - timer.elapsed)
                if wait_secs <= 0:
                    wait_secs = 1
                elif wait_secs > 20:
                    wait_secs = 20
            with timer:
                message = task_queue.pop_task(num=1, wait_secs=wait_secs)

            if not message:
                continue

            task = message['Body']
            logger.info(f"Received Task: {task}")

            # Check Idempotent
            if modules.idempotent:
                try:
                    if task['job_id']:
                        await job_id_model.insert_one(
                            JobIdSchema(
                                queue_name=queue_name,
                                job_name=task['job']['name'],
                                job_id=task['job_id']
                            )
                        )
                except DuplicateKeyError:
                    logger.warning(f"Duplicate Task[{task['job']['name']}]: {task['job_id']}")
                    task_queue.confirm(message['ReceiptHandle'])
                    continue

            try:
                # Message V1 Validation & Parsing
                task = MessageV1(**task).model_dump()
                with timer:
                    if task['job']['name'] not in JOB_ROUTER:
                        raise UnknownJob(task['job']['name'])
                    await JOB_ROUTER[task['job']['name']](
                        self.settings,
                        modules=modules,
                    ).run(**task['job']['param'])

            except (UnknownJob, InvalidVersion, InvalidCreator, Exception) as e:
                # Need Handle Exception
                logger.error(f"Error: {e}")
                logger.error(traceback.format_exc())
            finally:
                task_queue.confirm(message['ReceiptHandle'])


class ProducerSample(Job):

    async def run(self, queue_name: str, task_num: int = 1):
        task_num, converted = convert_param(task_num, int)
        task_queue = TaskQueue(
            queue_name,
            self.settings.sqs_access_key_id,
            self.settings.sqs_secret_access_key,
            self.settings.sqs_region_name,
        )

        for i in range(task_num):
            task_queue.push_task(
                MessageV1(
                    job={
                        'name': "HelloWorld",
                        'param': {
                            'name': 'Tony'
                        }
                    }
                )
            )
            logger.info(f"Pushed task {i}!")
