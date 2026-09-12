from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.products.model import Product
from app.products.schemas import ProductCreate, ProductUpdate


class SQLAlchemyProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        self.session.flush()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def list(self, *, limit: int, offset: int) -> tuple[list[Product], int]:
        stmt = select(Product).order_by(Product.id).limit(limit).offset(offset)
        products = list(self.session.scalars(stmt).all())
        total = self.session.scalar(select(func.count()).select_from(Product)) or 0
        return products, int(total)

    def update(self, product: Product, data: ProductUpdate) -> Product:
        for field, value in data.model_dump().items():
            setattr(product, field, value)
        self.session.flush()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.flush()
