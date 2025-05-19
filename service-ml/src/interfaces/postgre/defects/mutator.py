from abc import ABC
from abc import abstractmethod
from uuid import UUID

from src.domain.defect import DefectModel


class IDefectsMutator(ABC):

    @abstractmethod
    async def create(self, defect: DefectModel) -> UUID:
        pass
