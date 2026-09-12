.PHONY: install generate test lint run docker-up docker-down clean

install:
	python -m pip install -r requirements-dev.txt

generate:
	python scripts/generate_proto.py

test:
	pytest -q --cov=app --cov-report=term-missing

lint:
	ruff check app client tests scripts

run:
	python -m app.main

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	docker compose down -v --remove-orphans
