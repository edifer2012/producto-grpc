import argparse
import json

import grpc

from app.grpc.generated import product_pb2, product_pb2_grpc


def _print_product(product) -> None:
    print(
        json.dumps(
            {
                "id": product.id,
                "nombre": product.nombre,
                "descripcion": product.descripcion,
                "precio": product.precio,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente CLI de producto-grpc")
    parser.add_argument("--target", default="localhost:50051")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--nombre", required=True)
    create.add_argument("--descripcion", default="")
    create.add_argument("--precio", required=True)

    get = sub.add_parser("get")
    get.add_argument("id", type=int)

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--limit", type=int, default=50)
    list_cmd.add_argument("--offset", type=int, default=0)

    update = sub.add_parser("update")
    update.add_argument("id", type=int)
    update.add_argument("--nombre", required=True)
    update.add_argument("--descripcion", default="")
    update.add_argument("--precio", required=True)

    delete = sub.add_parser("delete")
    delete.add_argument("id", type=int)

    args = parser.parse_args()

    try:
        with grpc.insecure_channel(args.target) as channel:
            stub = product_pb2_grpc.ProductServiceStub(channel)

            if args.command == "create":
                response = stub.CreateProduct(
                    product_pb2.CreateProductRequest(
                        nombre=args.nombre,
                        descripcion=args.descripcion,
                        precio=args.precio,
                    )
                )
                _print_product(response.product)
            elif args.command == "get":
                response = stub.GetProduct(product_pb2.GetProductRequest(id=args.id))
                _print_product(response.product)
            elif args.command == "list":
                response = stub.ListProducts(
                    product_pb2.ListProductsRequest(limit=args.limit, offset=args.offset)
                )
                print(f"Total: {response.total}")
                for product in response.products:
                    _print_product(product)
            elif args.command == "update":
                response = stub.UpdateProduct(
                    product_pb2.UpdateProductRequest(
                        id=args.id,
                        nombre=args.nombre,
                        descripcion=args.descripcion,
                        precio=args.precio,
                    )
                )
                _print_product(response.product)
            elif args.command == "delete":
                response = stub.DeleteProduct(product_pb2.DeleteProductRequest(id=args.id))
                print(json.dumps({"success": response.success, "deleted_id": response.deleted_id}))
    except grpc.RpcError as exc:
        print(f"gRPC error: {exc.code().name} - {exc.details()}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
