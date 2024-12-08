from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError
