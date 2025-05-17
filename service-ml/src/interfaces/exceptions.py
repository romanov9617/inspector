from abc import ABC
from abc import abstractmethod


class AppException(Exception, ABC):

    @abstractmethod
    def __str__(self) -> str:
        pass
