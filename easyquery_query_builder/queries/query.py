from abc import ABC, abstractmethod

class Query(ABC):

    @abstractmethod
    def parse(self) -> str:
        pass