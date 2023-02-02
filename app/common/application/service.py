from abc import ABC

from app.common.domain import Repository


class Service(ABC):
    _repository: Repository

    def __init__(self, repository: Repository):
        self._repository = repository
