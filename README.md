Тестовое

1) Create .env with your settings like .env.examples
2) poetry install
3) poetry shell
4) docker compose up -d --build
5) docker compose exec web alembic revision --autogenerate -m "init commit"
6) docker compose exec web alembic upgrade head
7) docker compose exec web pytest
