from typing import Union, Optional
import boto3
import orjson
from pydantic import BaseModel


class TaskQueue:

    def __init__(
        self,
        queue_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str
    ):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.queue_url = self.sqs.get_queue_url(
            QueueName=queue_name
        )['QueueUrl']

    def push(self, body: str, group_id: Optional[str] = None):
        kwargs = {
            'QueueUrl': self.queue_url,
            'MessageBody': body,
        }
        if group_id:
            kwargs['MessageGroupId'] = group_id

        return self.sqs.send_message(**kwargs)

    def push_task(self, message: BaseModel, group_id: Optional[str] = None):
        """
        Push task to queue
        :param message: Message Model
        :param group_id: Group ID for FIFO Queue
        """
        body = message.model_dump()
        return self.push(orjson.dumps(body).decode(), group_id=group_id)

    def receive_messages(self, num: int, wait_secs: Optional[int] = None) -> dict:

        kwargs = {
            'QueueUrl': self.queue_url,
            'MaxNumberOfMessages': num,
        }
        if wait_secs:
            kwargs['WaitTimeSeconds'] = wait_secs

        return self.sqs.receive_message(**kwargs)

    def pop(self, num: int = 1, wait_secs: Optional[int] = None) -> Union[dict, list]:
        messages = self.receive_messages(num=num, wait_secs=wait_secs)
        if num == 1:
            return messages['Messages'][0] if 'Messages' in messages else None
        else:
            return messages['Messages'] if 'Messages' in messages else []

    def pop_task(self, num: int = 1, wait_secs: Optional[int] = None):
        message = self.pop(num=num, wait_secs=wait_secs)
        if message:
            if num == 1:
                message['Body'] = orjson.loads(message['Body'])
            else:
                for m in message:
                    m['Body'] = orjson.loads(m['Body'])
        return message

    def confirm(self, receipt: str):
        return self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt
        )

    @staticmethod
    def delete_message(message):
        return message.delete()
