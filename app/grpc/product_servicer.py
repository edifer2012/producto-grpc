import logging
from collections.abc import Callable
from contextlib import contextmanager
from typing import Iterator

import grpc
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.grpc.generated import product_pb2, product_pb2_grpc
from app.grpc.mappers import product_to_proto
from app.products.exceptions import ProductNotFoundError
from app.products.repository import SQLAlchemyProductRepository
from app.products.schemas import ProductCreate, ProductUpdate
from app.products.service import ProductService

logger = logging.getLogger(__name__)


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory

    @contextmanager
    def _service(self) -> Iterator[ProductService]:
        session = self.session_factory()
        try:
            yield ProductService(SQLAlchemyProductRepository(session))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def _abort_validation(context: grpc.ServicerContext, exc: Exception) -> None:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))

    @staticmethod
    def _abort_not_found(context: grpc.ServicerContext, exc: ProductNotFoundError) -> None:
        context.abort(grpc.StatusCode.NOT_FOUND, str(exc))

    @staticmethod
    def _abort_internal(context: grpc.ServicerContext, exc: Exception) -> None:
        logger.exception("Error interno procesando RPC", exc_info=exc)
        context.abort(grpc.StatusCode.INTERNAL, "Error interno del servidor")

    def CreateProduct(self, request, context):  # noqa: N802
        try:
            data = ProductCreate(
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
            )
            with self._service() as service:
                product = service.create(data)
                return product_pb2.ProductResponse(product=product_to_proto(product))
        except (ValidationError, ValueError) as exc:
            self._abort_validation(context, exc)
        except SQLAlchemyError as exc:
            self._abort_internal(context, exc)

    def GetProduct(self, request, context):  # noqa: N802
        try:
            if request.id <= 0:
                raise ValueError("id debe ser mayor que cero")
            with self._service() as service:
                product = service.get(request.id)
                return product_pb2.ProductResponse(product=product_to_proto(product))
        except ProductNotFoundError as exc:
            self._abort_not_found(context, exc)
        except ValueError as exc:
            self._abort_validation(context, exc)
        except SQLAlchemyError as exc:
            self._abort_internal(context, exc)

    def ListProducts(self, request, context):  # noqa: N802
        try:
            with self._service() as service:
                products, total = service.list(limit=request.limit, offset=request.offset)
                return product_pb2.ListProductsResponse(
                    products=[product_to_proto(product) for product in products],
                    total=total,
                )
        except ValueError as exc:
            self._abort_validation(context, exc)
        except SQLAlchemyError as exc:
            self._abort_internal(context, exc)

    def UpdateProduct(self, request, context):  # noqa: N802
        try:
            if request.id <= 0:
                raise ValueError("id debe ser mayor que cero")
            data = ProductUpdate(
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
            )
            with self._service() as service:
                product = service.update(request.id, data)
                return product_pb2.ProductResponse(product=product_to_proto(product))
        except ProductNotFoundError as exc:
            self._abort_not_found(context, exc)
        except (ValidationError, ValueError) as exc:
            self._abort_validation(context, exc)
        except SQLAlchemyError as exc:
            self._abort_internal(context, exc)

    def DeleteProduct(self, request, context):  # noqa: N802
        try:
            if request.id <= 0:
                raise ValueError("id debe ser mayor que cero")
            with self._service() as service:
                deleted_id = service.delete(request.id)
                return product_pb2.DeleteProductResponse(success=True, deleted_id=deleted_id)
        except ProductNotFoundError as exc:
            self._abort_not_found(context, exc)
        except ValueError as exc:
            self._abort_validation(context, exc)
        except SQLAlchemyError as exc:
            self._abort_internal(context, exc)
