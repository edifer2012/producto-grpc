import os
import sys

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc


def main() -> int:
    target = f"localhost:{os.getenv('GRPC_PORT', '50051')}"
    try:
        with grpc.insecure_channel(target) as channel:
            response = health_pb2_grpc.HealthStub(channel).Check(
                health_pb2.HealthCheckRequest(service=""), timeout=2
            )
        return 0 if response.status == health_pb2.HealthCheckResponse.SERVING else 1
    except grpc.RpcError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
