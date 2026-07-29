.PHONY: help up down logs autogenerate migrate downgrade history

m ?= "auto_migration"

alembic-revision: ## Generate a new Alembic manual migration
	@echo "Generating migration: $(m)"
	docker compose exec api alembic revision -m "$(m)"

alembic-autogenerate: ## Generate a new Alembic migration
	docker compose exec api alembic revision --autogenerate -m "$(m)"

alembic-migrate: ## Apply all pending migrations to the database
	@echo "Applying migrations..."
	docker compose exec api alembic upgrade head

alembic-downgrade: ## Revert the last migration step
	@echo "Downgrading database by 1 revision..."
	docker compose exec api alembic downgrade -1

alembic-history: ## Show the migration history
	docker compose exec api alembic history --verbose
