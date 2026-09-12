# -*- coding: utf-8 -*-
# Generated from proto/product.proto. DO NOT EDIT MANUALLY.
"""Generated protocol buffer code for products.v1."""

from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\rproduct.proto\x12\x0bproducts.v1"J\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\x13\n\x0bdescripcion\x18\x03 \x01(\t\x12\x0e\n\x06precio\x18\x04 \x01(\t"K\n\x14CreateProductRequest\x12\x0e\n\x06nombre\x18\x01 \x01(\t\x12\x13\n\x0bdescripcion\x18\x02 \x01(\t\x12\x0e\n\x06precio\x18\x03 \x01(\t"\x1f\n\x11GetProductRequest\x12\n\n\x02id\x18\x01 \x01(\x03"4\n\x13ListProductsRequest\x12\r\n\x05limit\x18\x01 \x01(\x05\x12\x0e\n\x06offset\x18\x02 \x01(\x05"M\n\x14ListProductsResponse\x12&\n\x08products\x18\x01 \x03(\x0b\x32\x14.products.v1.Product\x12\r\n\x05total\x18\x02 \x01(\x03"W\n\x14UpdateProductRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\x13\n\x0bdescripcion\x18\x03 \x01(\t\x12\x0e\n\x06precio\x18\x04 \x01(\t""\n\x14DeleteProductRequest\x12\n\n\x02id\x18\x01 \x01(\x03"8\n\x0fProductResponse\x12%\n\x07product\x18\x01 \x01(\x0b\x32\x14.products.v1.Product"<\n\x15DeleteProductResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\ndeleted_id\x18\x02 \x01(\x03\x32\xad\x03\n\x0eProductService\x12P\n\rCreateProduct\x12!.products.v1.CreateProductRequest\x1a\x1c.products.v1.ProductResponse\x12J\n\nGetProduct\x12\x1e.products.v1.GetProductRequest\x1a\x1c.products.v1.ProductResponse\x12S\n\x0cListProducts\x12 .products.v1.ListProductsRequest\x1a!.products.v1.ListProductsResponse\x12P\n\rUpdateProduct\x12!.products.v1.UpdateProductRequest\x1a\x1c.products.v1.ProductResponse\x12V\n\rDeleteProduct\x12!.products.v1.DeleteProductRequest\x1a".products.v1.DeleteProductResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR,
    "app.grpc.generated.product_pb2",
    _globals,
)
