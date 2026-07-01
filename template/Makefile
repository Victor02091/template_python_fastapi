.PHONY: help up down logs autogenerate migrate downgrade history

m ?= "auto_migration"

revision: ## Generate a new Alembic manual migration (Usage: make autogenerate m="your_message")
	@echo "Generating migration: $(m)"
	docker compose exec api alembic revision -m "$(m)"

autogenerate: ## Generate a new Alembic migration (Usage: make autogenerate m="your_message")
	@echo "Generating migration: $(m)"
	docker compose exec api alembic revision --autogenerate -m "$(m)"

migrate: ## Apply all pending migrations to the database
	@echo "Applying migrations..."
	docker compose exec api alembic upgrade head

downgrade: ## Revert the last migration step
	@echo "Downgrading database by 1 revision..."
	docker compose exec api alembic downgrade -1

history: ## Show the migration history
	docker compose exec api alembic history --verbose
