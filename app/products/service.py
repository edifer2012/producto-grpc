from app.products.exceptions import ProductNotFoundError
from app.products.model import Product
from app.products.ports import ProductRepositoryPort
from app.products.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepositoryPort) -> None:
        self.repository = repository

    def create(self, data: ProductCreate) -> Product:
        return self.repository.create(data)

    def get(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def list(self, *, limit: int = 50, offset: int = 0) -> tuple[list[Product], int]:
        # El transporte puede enviar 0 como valor por defecto de proto3.
        normalized_limit = 50 if limit == 0 else limit
        if not 1 <= normalized_limit <= 200:
            raise ValueError("limit debe estar entre 1 y 200")
        if offset < 0:
            raise ValueError("offset no puede ser negativo")
        return self.repository.list(limit=normalized_limit, offset=offset)

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get(product_id)
        return self.repository.update(product, data)

    def delete(self, product_id: int) -> int:
        product = self.get(product_id)
        self.repository.delete(product)
        return product_id
