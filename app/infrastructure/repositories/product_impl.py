from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.domain.entities.product import ProductEntity, ProductEntityFactory
from app.domain.repositories.product import ProductRepository
from app.infrastructure.models.product import ProductModel
from app.infrastructure.database import database


class ProductRepositoryImpl(ProductRepository):
    
    def __init__(self):
        self.database = database

    async def get_all(self) -> List[ProductEntity]:
        async for session in self.database.get_session():
            stmt = select(ProductModel)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return [
                ProductEntityFactory.create(**product.to_dict()) 
                for product in products
            ]

    async def get_by_id(self, id: str) -> ProductEntity | None:
        async for session in self.database.get_session():
            stmt = select(ProductModel).where(ProductModel.id == id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            
            if product is None:
                return None
                
            return ProductEntityFactory.create(**product.to_dict())

    async def add(self, product: ProductEntity) -> ProductEntity:
        async for session in self.database.get_session():
            product_model = ProductModel(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                image=product.image
            )
            session.add(product_model)
            await session.flush()
            return product

    async def update(self, product: ProductEntity) -> ProductEntity:
        async for session in self.database.get_session():
            stmt = update(ProductModel).where(ProductModel.id == product.id).values(
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                image=product.image
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise ValueError(f"Product with id {product.id} not found")
            
            await session.flush()
            return product
