from app.grpc.generated import product_pb2
from app.products.model import Product


def product_to_proto(product: Product) -> product_pb2.Product:
    return product_pb2.Product(
        id=product.id,
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=f"{product.precio:.2f}",
    )
