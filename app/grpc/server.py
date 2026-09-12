import logging
from concurrent import futures
from collections.abc import Callable

import grpc
from sqlalchemy.orm import Session

from app.grpc.generated import product_pb2, product_pb2_grpc
from app.grpc.product_servicer import ProductServicer

logger = logging.getLogger(__name__)


def build_server(
    session_factory: Callable[[], Session],
    *,
    max_workers: int = 10,
    enable_optional_services: bool = True,
) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductServicer(session_factory), server
    )

    if enable_optional_services:
        _register_health_and_reflection(server)

    return server


def _register_health_and_reflection(server: grpc.Server) -> None:
    service_name = product_pb2.DESCRIPTOR.services_by_name["ProductService"].full_name

    try:
        from grpc_health.v1 import health, health_pb2, health_pb2_grpc

        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
        health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
        health_servicer.set(service_name, health_pb2.HealthCheckResponse.SERVING)
    except ImportError:
        logger.warning("grpcio-health-checking no instalado; health service deshabilitado")

    try:
        from grpc_reflection.v1alpha import reflection

        reflection.enable_server_reflection(
            (service_name, reflection.SERVICE_NAME),
            server,
        )
    except ImportError:
        logger.warning("grpcio-reflection no instalado; reflection deshabilitada")
