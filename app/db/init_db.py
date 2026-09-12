from sqlalchemy.engine import Engine

from app.db.base import Base
# Importar modelos registra sus tablas en metadata.
from app.products import model as _product_model  # noqa: F401


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
