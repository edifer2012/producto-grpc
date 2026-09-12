# Generated from proto/product.proto. DO NOT EDIT MANUALLY.
"""gRPC service definitions for products.v1.ProductService."""

import grpc

from . import product_pb2 as product__pb2


class ProductServiceStub:
    def __init__(self, channel: grpc.Channel) -> None:
        self.CreateProduct = channel.unary_unary(
            "/products.v1.ProductService/CreateProduct",
            request_serializer=product__pb2.CreateProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.GetProduct = channel.unary_unary(
            "/products.v1.ProductService/GetProduct",
            request_serializer=product__pb2.GetProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.ListProducts = channel.unary_unary(
            "/products.v1.ProductService/ListProducts",
            request_serializer=product__pb2.ListProductsRequest.SerializeToString,
            response_deserializer=product__pb2.ListProductsResponse.FromString,
        )
        self.UpdateProduct = channel.unary_unary(
            "/products.v1.ProductService/UpdateProduct",
            request_serializer=product__pb2.UpdateProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.DeleteProduct = channel.unary_unary(
            "/products.v1.ProductService/DeleteProduct",
            request_serializer=product__pb2.DeleteProductRequest.SerializeToString,
            response_deserializer=product__pb2.DeleteProductResponse.FromString,
        )


class ProductServiceServicer:
    def CreateProduct(self, request, context):  # noqa: N802
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def GetProduct(self, request, context):  # noqa: N802
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def ListProducts(self, request, context):  # noqa: N802
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def UpdateProduct(self, request, context):  # noqa: N802
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def DeleteProduct(self, request, context):  # noqa: N802
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_ProductServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateProduct": grpc.unary_unary_rpc_method_handler(
            servicer.CreateProduct,
            request_deserializer=product__pb2.CreateProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "GetProduct": grpc.unary_unary_rpc_method_handler(
            servicer.GetProduct,
            request_deserializer=product__pb2.GetProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "ListProducts": grpc.unary_unary_rpc_method_handler(
            servicer.ListProducts,
            request_deserializer=product__pb2.ListProductsRequest.FromString,
            response_serializer=product__pb2.ListProductsResponse.SerializeToString,
        ),
        "UpdateProduct": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateProduct,
            request_deserializer=product__pb2.UpdateProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "DeleteProduct": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteProduct,
            request_deserializer=product__pb2.DeleteProductRequest.FromString,
            response_serializer=product__pb2.DeleteProductResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "products.v1.ProductService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "products.v1.ProductService", rpc_method_handlers
    )
