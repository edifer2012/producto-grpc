from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
