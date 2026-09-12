import logging

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.init_db import init_db
from app.db.session import create_db_engine, create_session_factory
from app.grpc.server import build_server


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = logging.getLogger(__name__)

    engine = create_db_engine(settings.database_url)
    init_db(engine)
    session_factory = create_session_factory(engine)

    server = build_server(
        session_factory,
        max_workers=settings.grpc_max_workers,
    )
    address = f"{settings.grpc_host}:{settings.grpc_port}"
    server.add_insecure_port(address)
    server.start()
    logger.info("%s escuchando en %s", settings.app_name, address)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Deteniendo servidor gRPC")
        server.stop(grace=5)


if __name__ == "__main__":
    main()
