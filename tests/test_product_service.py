from dataclasses import dataclass
from decimal import Decimal

import pytest

from app.products.exceptions import ProductNotFoundError
from app.products.schemas import ProductCreate
from app.products.service import ProductService


@dataclass
class FakeProduct:
    id: int
    nombre: str
    descripcion: str
    precio: Decimal


class FakeRepository:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def create(self, data):
        product = FakeProduct(id=self.next_id, **data.model_dump())
        self.items[self.next_id] = product
        self.next_id += 1
        return product

    def get_by_id(self, product_id):
        return self.items.get(product_id)

    def list(self, *, limit, offset):
        values = list(self.items.values())
        return values[offset : offset + limit], len(values)

    def update(self, product, data):
        for key, value in data.model_dump().items():
            setattr(product, key, value)
        return product

    def delete(self, product):
        self.items.pop(product.id)


def test_service_create_and_get():
    service = ProductService(FakeRepository())
    product = service.create(
        ProductCreate(nombre="Teclado", descripcion="Mecánico", precio="250000")
    )
    assert service.get(product.id).nombre == "Teclado"


def test_service_not_found():
    service = ProductService(FakeRepository())
    with pytest.raises(ProductNotFoundError):
        service.get(999)


def test_service_list_validates_limit():
    service = ProductService(FakeRepository())
    with pytest.raises(ValueError):
        service.list(limit=201, offset=0)
