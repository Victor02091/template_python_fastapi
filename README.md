# Modern Python FastAPI Template

A production-ready FastAPI project template powered by **uv**.

This template provides a batteries-included setup with modern tooling, strict linting, automatic formatting, and CI/CD integration, all configured to work out of the box.

## ✨ Features

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) with async support and automatic OpenAPI docs.
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (blazing fast replacement for pip/poetry).
* **Linter & Formatter:** [Ruff](https://github.com/astral-sh/ruff) (configured for strict imports and formatting).
* **Type Checking:** Standard Mypy.
* **Pre-commit:** Automatic hooks to ensure code quality before every commit (optional).
* **CI/CD:** CI pipelines for GitHub Actions, GitLab CI, or Bitbucket Pipelines (optional).
* **Containerization:** Dockerfile and docker-compose included.
* **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) ORM with async support, [Alembic](https://alembic.sqlalchemy.org/) migrations, and [PostgreSQL](https://www.postgresql.org/) via `asyncpg` pre-configured.
* **Editor:** VS Code settings (extensions, and linting) pre-configured.

## 📂 Project Structure

The template generates a clean, production-ready directory layout:

```
your-project/
├── app/
│   ├── api/          # Route definitions
│   ├── core/         # Settings and configuration
│   ├── db/           # Database session and engine
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI application entrypoint
├── migrations/       # Alembic migration files
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## 🛠️ Requirements

You **do not** need to install Python manually. The package manager `uv` handles Python versions automatically.

You only need:
1.  **Git**
2.  **uv**

### How to install uv

**On Linux / macOS:**

    curl -LsSf https://astral.sh/uv/install.sh | sh

**On Windows:**

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

*More info on the [official website](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1).*

## 📦 Installation

This template is built with **Copier**. You can install Copier globally using `uv` (recommended).

**Important:** This template uses custom extensions. You must install Copier with the `copier-template-extensions` plugin.

    uv tool install copier --with copier-template-extensions

## 🚀 Usage

**Prerequisites:**
1.  Create a new repository (or folder) and open it in your terminal.
2.  **Ensure the folder is completely empty** (except for the `.git` folder if you cloned a new repository).

Run the generation command inside your empty folder:

    copier copy --trust https://github.com/Victor02091/template_python_fastapi .

### Update values of an existing project

If you have already generated a project and want to change the current values, like updating the Python version:

    copier update --vcs-ref=:current: --trust --defaults --data python_version="3.13"

### Update template of an existing project

If you have already generated a project and want to pull the latest updates from the template:

    copier update --trust
