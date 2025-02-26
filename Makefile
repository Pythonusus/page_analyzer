install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run --port=${PORT:-5050}

debug:
	poetry run flask --app page_analyzer:app --debug run --port=${PORT:-5050}

lint:
	poetry run flake8 page_analyzer

pylint:
	poetry run pylint page_analyzer

build:
	./build.sh

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:${PORT:-8000} page_analyzer:app

docker-build-dev:
	TARGET=development docker compose build

docker-build-prod:
	TARGET=production docker compose build

docker-start-dev:
	TARGET=development PORT=5050 docker compose up

docker-start-prod:
	TARGET=production PORT=${PORT:-8000} docker compose up

docker-rm-containers:
	docker compose down

docker-rm-volumes:
	docker compose down -v

.PHONY: install dev debug lint pylint build docker-build-dev docker-build-prod docker-start-dev docker-start-prod docker-rm-volumes start
