from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from api.entities.entity_base import EntityBase

T = TypeVar("T", bound=EntityBase)
DTO = TypeVar("DTO")
DTO_RESPONSE = TypeVar("DTO_RESPONSE")
ID = TypeVar("ID")


class GenericService(ABC, Generic[T, DTO, DTO_RESPONSE, ID]):
    @abstractmethod
    def find_all(self) -> list[DTO_RESPONSE]: ...

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> DTO_RESPONSE | None: ...

    @abstractmethod
    def create(self, dto: DTO) -> DTO_RESPONSE: ...

    @abstractmethod
    def update(self, entity_id: ID, dto: DTO) -> DTO_RESPONSE: ...

    @abstractmethod
    def delete(self, entity_id: ID) -> None: ...
