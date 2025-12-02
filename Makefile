run-fastapi-dev:
	uv run fastapi dev app/main.py
build-docker-image:
	docker compose build --no-cache
