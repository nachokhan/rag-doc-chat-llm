
.PHONY: build run stop logs format test init_db migrate debug

debug:
	docker-compose -f docker-compose.yml -f docker-compose.debug.yml up --build

migrate:
	docker-compose run --rm api alembic upgrade head

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f api

format:
	docker-compose run --rm api black .
	docker-compose run --rm api isort .

test:
	docker-compose run --rm api pytest

init_db:
	docker-compose run --rm api python scripts/init_db.py

