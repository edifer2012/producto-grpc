# producto-grpc

Aplicación de referencia para gestionar productos mediante **gRPC**, **Protocol Buffers**, **Python**, **SQLAlchemy** y **PostgreSQL**. El proyecto aplica separación de responsabilidades y un enfoque cercano a arquitectura hexagonal: gRPC actúa como adaptador de entrada, la lógica de negocio se mantiene en la capa de aplicación y la persistencia queda aislada detrás de un puerto de repositorio.

## 1. Objetivo

Implementar un CRUD de productos con las operaciones:

- Crear producto.
- Consultar producto por identificador.
- Listar productos con paginación básica.
- Actualizar producto.
- Eliminar producto.

Cada producto contiene:

| Campo | Tipo | Regla |
|---|---|---|
| `id` | entero | generado por la base de datos |
| `nombre` | texto | obligatorio, máximo 120 caracteres |
| `descripcion` | texto | máximo 500 caracteres |
| `precio` | decimal | mayor que cero, precisión `NUMERIC(12,2)` |

En el contrato Protobuf, `precio` se transmite como `string` para evitar pérdida de precisión propia de los números binarios de punto flotante.

## 2. Arquitectura de solución

```text
┌──────────────────────────────┐
│ Cliente gRPC / CLI           │
└──────────────┬───────────────┘
               │ HTTP/2 + Protobuf
               ▼
┌──────────────────────────────┐
│ Adaptador gRPC               │
│ ProductServicer              │
│ - Traducción request/response│
│ - Mapeo de errores gRPC      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Capa de aplicación           │
│ ProductService               │
│ - Reglas de negocio          │
│ - Casos de uso CRUD          │
└──────────────┬───────────────┘
               │ ProductRepositoryPort
               ▼
┌──────────────────────────────┐
│ Adaptador de persistencia    │
│ SQLAlchemyProductRepository  │
└──────────────┬───────────────┘
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│ PostgreSQL                   │
│ tabla products               │
└──────────────────────────────┘
```

La dependencia va hacia el núcleo: `ProductService` conoce el **puerto** del repositorio, pero no conoce gRPC ni PostgreSQL.

## 3. Componentes

```text
producto-grpc/
├── proto/
│   └── product.proto              # Contrato gRPC/Protobuf
├── app/
│   ├── core/
│   │   ├── config.py              # Configuración por variables de entorno
│   │   └── logging.py             # Configuración de logs
│   ├── db/
│   │   ├── base.py                # Base declarativa SQLAlchemy
│   │   ├── session.py             # Engine y Session factory
│   │   └── init_db.py             # Creación inicial de tablas
│   ├── products/
│   │   ├── model.py               # Modelo ORM Product
│   │   ├── schemas.py             # Validación Pydantic
│   │   ├── exceptions.py          # Excepciones de dominio
│   │   ├── ports.py               # Puerto ProductRepositoryPort
│   │   ├── repository.py          # Adaptador SQLAlchemy
│   │   └── service.py             # Casos de uso de Producto
│   ├── grpc/
│   │   ├── generated/             # Stubs generados desde product.proto
│   │   ├── mappers.py             # ORM -> Protobuf
│   │   ├── product_servicer.py    # Implementación de ProductService gRPC
│   │   └── server.py              # Construcción del servidor gRPC
│   └── main.py                    # Punto de entrada
├── client/
│   └── product_client.py          # Cliente CLI de ejemplo
├── scripts/
│   ├── generate_proto.py          # Regeneración de stubs
│   └── healthcheck.py             # Health check para Docker
├── tests/
│   ├── conftest.py                # Servidor gRPC de prueba + SQLite
│   ├── test_product_service.py    # Pruebas unitarias
│   └── test_products_grpc.py      # Pruebas de integración gRPC
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── pyproject.toml
└── .env.example
```

## 4. Contrato gRPC

El archivo `proto/product.proto` es la fuente de verdad del contrato externo.

```proto
service ProductService {
  rpc CreateProduct(CreateProductRequest) returns (ProductResponse);
  rpc GetProduct(GetProductRequest) returns (ProductResponse);
  rpc ListProducts(ListProductsRequest) returns (ListProductsResponse);
  rpc UpdateProduct(UpdateProductRequest) returns (ProductResponse);
  rpc DeleteProduct(DeleteProductRequest) returns (DeleteProductResponse);
}
```

Las llamadas CRUD son RPC **unary**: una solicitud produce una respuesta. No se usa streaming porque no agrega valor al caso de uso básico de gestión de productos.

## 5. Requisitos

### Ejecución con Docker

- Docker Engine.
- Docker Compose v2.

### Ejecución local

- Python 3.13 o compatible.
- PostgreSQL 17 o compatible.
- `pip`.

## 6. Configuración

Copie el archivo de ejemplo:

```bash
cp .env.example .env
```

Variables principales:

```dotenv
APP_NAME=producto-grpc
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
GRPC_MAX_WORKERS=10
DATABASE_URL=postgresql+psycopg://producto:producto@db:5432/producto
LOG_LEVEL=INFO
```

> Para ejecución local sin Docker, cambie `db` por `localhost` en `DATABASE_URL`.

## 7. Ejecución con Docker Compose

Construir e iniciar:

```bash
docker compose up --build -d
```

Consultar estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f producto-grpc
```

El servicio queda disponible en:

```text
localhost:50051
```

Detener contenedores:

```bash
docker compose down
```

Eliminar además los volúmenes de PostgreSQL:

```bash
docker compose down -v --remove-orphans
```

También puede usar:

```bash
make docker-up
make docker-down
make clean
```

## 8. Ejecución local

Crear entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements-dev.txt
```

Regenerar stubs:

```bash
python scripts/generate_proto.py
```

Configurar una base PostgreSQL y ajustar `DATABASE_URL` en `.env`.

Iniciar el servidor:

```bash
python -m app.main
```

## 9. Generación de código desde Protobuf

Después de modificar `proto/product.proto`, ejecute:

```bash
make generate
```

o:

```bash
python scripts/generate_proto.py
```

El script ejecuta `grpc_tools.protoc` y actualiza:

```text
app/grpc/generated/product_pb2.py
app/grpc/generated/product_pb2_grpc.py
```

No modifique estos archivos manualmente.

## 10. Uso del cliente CLI

El proyecto incluye un cliente Python que consume exactamente el contrato gRPC.

### Crear

```bash
python -m client.product_client create \
  --nombre "Monitor 27" \
  --descripcion "Monitor IPS QHD" \
  --precio "1299999.90"
```

### Consultar por ID

```bash
python -m client.product_client get 1
```

### Listar

```bash
python -m client.product_client list --limit 20 --offset 0
```

### Actualizar

```bash
python -m client.product_client update 1 \
  --nombre "Monitor 32" \
  --descripcion "Monitor 4K" \
  --precio "1899999.00"
```

### Eliminar

```bash
python -m client.product_client delete 1
```

Para conectarse a otro host:

```bash
python -m client.product_client --target servidor:50051 list
```

## 11. Pruebas con grpcurl

Si dispone de `grpcurl`, el servidor publica **gRPC Reflection**, por lo que puede inspeccionar el contrato sin indicar manualmente el `.proto`.

Listar servicios:

```bash
grpcurl -plaintext localhost:50051 list
```

Describir el servicio:

```bash
grpcurl -plaintext localhost:50051 describe products.v1.ProductService
```

Crear un producto:

```bash
grpcurl -plaintext \
  -d '{"nombre":"Teclado","descripcion":"Mecánico","precio":"250000.00"}' \
  localhost:50051 \
  products.v1.ProductService/CreateProduct
```

Listar productos:

```bash
grpcurl -plaintext \
  -d '{"limit":20,"offset":0}' \
  localhost:50051 \
  products.v1.ProductService/ListProducts
```

Consultar:

```bash
grpcurl -plaintext \
  -d '{"id":1}' \
  localhost:50051 \
  products.v1.ProductService/GetProduct
```

## 12. Códigos de error gRPC

El adaptador traduce los errores del dominio a códigos del protocolo:

| Situación | Código gRPC |
|---|---|
| Solicitud válida | `OK` |
| ID, precio o campos inválidos | `INVALID_ARGUMENT` |
| Producto inexistente | `NOT_FOUND` |
| Error inesperado de persistencia | `INTERNAL` |

Ejemplo conceptual:

```text
ProductNotFoundError
        ↓
ProductServicer
        ↓
grpc.StatusCode.NOT_FOUND
```

De esta forma las excepciones propias de la aplicación no se filtran directamente al consumidor.

## 13. Manejo de transacciones

Cada RPC crea una sesión SQLAlchemy independiente:

```text
RPC
 │
 ▼
crear Session
 │
 ▼
ProductService
 │
 ▼
Repository
 │
 ├── éxito ──► COMMIT
 │
 └── error ──► ROLLBACK
 │
 ▼
cerrar Session
```

Esto evita compartir una misma sesión entre los hilos del servidor gRPC.

## 14. Health check y Reflection

Se habilitan dos capacidades operativas:

- **gRPC Health Checking** para comprobar que el servicio está disponible.
- **gRPC Server Reflection** para inspeccionar servicios y mensajes con herramientas como `grpcurl`.

El `Dockerfile` utiliza `scripts/healthcheck.py` para verificar el estado del contenedor.

## 15. Pruebas automatizadas

Las pruebas no necesitan PostgreSQL. Utilizan SQLite en memoria y levantan un servidor gRPC real en un puerto efímero.

Ejecutar:

```bash
pytest -q
```

Con cobertura:

```bash
pytest -q --cov=app --cov-report=term-missing
```

o:

```bash
make test
```

Se cubren, entre otros:

- Creación.
- Consulta.
- Listado y paginación.
- Actualización.
- Eliminación.
- `NOT_FOUND`.
- `INVALID_ARGUMENT`.
- Reglas de la capa de aplicación.

## 16. Separación de responsabilidades

### `product.proto`

Define el contrato externo. No contiene reglas de persistencia ni lógica de negocio.

### `ProductServicer`

Es el adaptador gRPC. Convierte mensajes Protobuf en objetos de aplicación y transforma excepciones en códigos gRPC.

### `ProductService`

Implementa los casos de uso. No depende de gRPC, SQLAlchemy ni PostgreSQL.

### `ProductRepositoryPort`

Define lo que la aplicación necesita de la persistencia.

### `SQLAlchemyProductRepository`

Implementa el puerto usando SQLAlchemy.

### `Product`

Representa la persistencia relacional del producto.

## 17. Flujo de una operación

Ejemplo `CreateProduct`:

```text
Cliente
  │
  │ CreateProductRequest
  ▼
Protocol Buffers
  │
  ▼
HTTP/2
  │
  ▼
ProductServicer
  │
  ▼
ProductCreate (validación)
  │
  ▼
ProductService.create()
  │
  ▼
ProductRepositoryPort
  │
  ▼
SQLAlchemyProductRepository
  │
  ▼
PostgreSQL
  │
  ▼
COMMIT
  │
  ▼
ProductResponse
  │
  ▼
Cliente
```

## 18. Comparación con REST y GraphQL

La arquitectura interna puede mantenerse prácticamente igual:

```text
REST       → Router   ┐
GraphQL    → Resolver ├─→ ProductService → Repository → PostgreSQL
gRPC       → Servicer ┘
```

Esto ilustra una idea arquitectónica importante: **REST, GraphQL y gRPC son mecanismos de exposición e integración; no deberían controlar la lógica del dominio**.

En una arquitectura hexagonal, cada uno puede implementarse como un adaptador de entrada diferente alrededor del mismo núcleo.

## 19. Seguridad para producción

El ejemplo usa `insecure_channel` y un puerto gRPC sin TLS para facilitar el laboratorio. Para producción se recomienda:

- TLS/mTLS.
- Autenticación mediante metadata e interceptores.
- Autorización por operación.
- Gestión externa de secretos.
- Límites de tamaño de mensajes.
- Timeouts/deadlines.
- Observabilidad con métricas y trazas.
- Migraciones de esquema con Alembic en lugar de `create_all`.

## 20. Decisiones arquitectónicas principales

1. **Contract-first:** `product.proto` gobierna la interfaz del servicio.
2. **Precio como string en Protobuf:** evita pérdida de precisión monetaria.
3. **Unary RPC para CRUD:** streaming no aporta valor al caso inicial.
4. **Repositorio como puerto:** desacopla la aplicación de SQLAlchemy.
5. **Sesión por RPC:** adecuado para concurrencia del servidor gRPC.
6. **PostgreSQL para producción y SQLite para pruebas:** permite pruebas rápidas sin acoplarlas a infraestructura externa.
7. **Reflection y health checking:** mejoran operación y diagnóstico.

## 21. Evolución posible

La solución puede evolucionar posteriormente con:

- TLS/mTLS.
- JWT/OAuth2 mediante metadata e interceptores.
- Alembic.
- OpenTelemetry.
- Prometheus.
- Server streaming para eventos de inventario.
- Interceptores para logging, autenticación y trazabilidad.
- API Gateway o transcodificación gRPC/REST para clientes web.
- Kubernetes/OpenShift.

---

Este proyecto está pensado como ejercicio de **arquitectura de software**, no sólo como implementación CRUD. La separación del adaptador gRPC respecto de la aplicación permite comparar el mismo dominio cuando se expone mediante REST, GraphQL o gRPC sin reescribir el núcleo funcional.
