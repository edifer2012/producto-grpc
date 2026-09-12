import grpc
import pytest

from app.grpc.generated import product_pb2


def test_crud_product(grpc_stub):
    created = grpc_stub.CreateProduct(
        product_pb2.CreateProductRequest(
            nombre="Monitor 27",
            descripcion="Monitor IPS",
            precio="1299999.90",
        )
    )
    assert created.product.id > 0
    assert created.product.nombre == "Monitor 27"
    assert created.product.precio == "1299999.90"

    fetched = grpc_stub.GetProduct(product_pb2.GetProductRequest(id=created.product.id))
    assert fetched.product.id == created.product.id

    listed = grpc_stub.ListProducts(product_pb2.ListProductsRequest(limit=10, offset=0))
    assert listed.total == 1
    assert len(listed.products) == 1

    updated = grpc_stub.UpdateProduct(
        product_pb2.UpdateProductRequest(
            id=created.product.id,
            nombre="Monitor 32",
            descripcion="Monitor 4K",
            precio="1899999.00",
        )
    )
    assert updated.product.nombre == "Monitor 32"
    assert updated.product.precio == "1899999.00"

    deleted = grpc_stub.DeleteProduct(product_pb2.DeleteProductRequest(id=created.product.id))
    assert deleted.success is True
    assert deleted.deleted_id == created.product.id

    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetProduct(product_pb2.GetProductRequest(id=created.product.id))
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


def test_invalid_price_returns_invalid_argument(grpc_stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.CreateProduct(
            product_pb2.CreateProductRequest(
                nombre="Producto inválido",
                descripcion="",
                precio="0",
            )
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_invalid_id_returns_invalid_argument(grpc_stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetProduct(product_pb2.GetProductRequest(id=0))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_pagination(grpc_stub):
    for index in range(3):
        grpc_stub.CreateProduct(
            product_pb2.CreateProductRequest(
                nombre=f"Producto {index}",
                descripcion="",
                precio="10.00",
            )
        )

    response = grpc_stub.ListProducts(product_pb2.ListProductsRequest(limit=2, offset=1))
    assert response.total == 3
    assert len(response.products) == 2
    assert response.products[0].nombre == "Producto 1"
