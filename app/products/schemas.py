from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(default="", max_length=500)
    precio: Decimal = Field(gt=Decimal("0"), max_digits=12, decimal_places=2)

    @field_validator("nombre")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        return value

    @field_validator("descripcion")
    @classmethod
    def normalize_description(cls, value: str) -> str:
        return value.strip()


class ProductUpdate(ProductCreate):
    pass


class ProductRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: Decimal

    model_config = ConfigDict(from_attributes=True)
