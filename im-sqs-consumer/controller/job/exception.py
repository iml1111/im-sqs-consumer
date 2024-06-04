class IsNotJob(Exception):

    def __str__(self):
        return 'This Object is not Job.'


class UnknownJob(Exception):
    def __init__(self, job_name: str):
        self.job_name = job_name

    def __str__(self):
        return f'[{self.job_name}] job is not registered.'


class InvalidVersion(Exception):
    def __init__(self, version: int):
        self.version = version

    def __str__(self):
        return f'version [{self.version}] unsupported.'


class InvalidCreator(Exception):
    def __init__(self, creator: str):
        self.creator = creator

    def __str__(self):
        return f'creator [{self.creator}] unsupported.'