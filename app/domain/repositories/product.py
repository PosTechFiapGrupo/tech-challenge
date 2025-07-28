from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.product import ProductEntity


class ProductRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[ProductEntity]:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, id: str) -> ProductEntity:
        raise NotImplemented

    @abstractmethod
    async def add(self, product: ProductEntity) -> ProductEntity:
        raise NotImplemented

    @abstractmethod
    async def update(self, product: ProductEntity) -> ProductEntity:
        raise NotImplemented
