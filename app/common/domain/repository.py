from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def start_transaction(self):
        pass

    @abstractmethod
    def commit_transaction(self):
        pass

    @abstractmethod
    def rollback_transaction(self):
        pass
