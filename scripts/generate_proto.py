from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROTO = ROOT / "proto" / "product.proto"
OUT = ROOT / "app" / "grpc" / "generated"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{PROTO.parent}",
        f"--python_out={OUT}",
        f"--grpc_python_out={OUT}",
        str(PROTO),
    ]
    subprocess.run(command, check=True)

    grpc_file = OUT / "product_pb2_grpc.py"
    text = grpc_file.read_text(encoding="utf-8")
    text = text.replace(
        "import product_pb2 as product__pb2",
        "from . import product_pb2 as product__pb2",
    )
    grpc_file.write_text(text, encoding="utf-8")
    print(f"Stubs generados en {OUT}")


if __name__ == "__main__":
    main()
