class ProductError(Exception):
    """Base para errores del dominio de productos."""


class ProductNotFoundError(ProductError):
    def __init__(self, product_id: int) -> None:
        self.product_id = product_id
        super().__init__(f"Producto {product_id} no encontrado")
