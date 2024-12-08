from abc import ABC, abstractmethod

class AbstractVerifyService(ABC):
    @abstractmethod
    def send_code(self, code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_code(self) -> str:
        raise NotImplementedError