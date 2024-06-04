# IM SQS Consumer

## Get Started
아래의 명령어를 통해 SQS Consumer를 실행할 수 있습니다.
```shell
$ python main.py run Job:Consumer <queue_name>
```

필요하다면 ProducerSample Job을 통해 메시지를 큐에 전송할 수 있습니다.
```shell
$ python main.py run Job:ProducerSample <queue_name> task_num=10
```

# References
- https://github.com/iml1111/IMJob
