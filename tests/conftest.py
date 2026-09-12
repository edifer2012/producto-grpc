from collections.abc import Iterator
from concurrent import futures

import grpc
import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.grpc.generated import product_pb2_grpc
from app.grpc.product_servicer import ProductServicer


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    yield factory
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def grpc_stub(session_factory) -> Iterator[product_pb2_grpc.ProductServiceStub]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductServicer(session_factory), server
    )
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()

    channel = grpc.insecure_channel(f"127.0.0.1:{port}")
    grpc.channel_ready_future(channel).result(timeout=5)
    try:
        yield product_pb2_grpc.ProductServiceStub(channel)
    finally:
        channel.close()
        server.stop(grace=0).wait()
