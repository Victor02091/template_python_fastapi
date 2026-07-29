import importlib
import pkgutil

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)


def load_all_models() -> None:
    """Dynamically import all modules from app.models for Alembic discovery."""
    import app.models as models_package

    for _, module_name, _ in pkgutil.walk_packages(
        models_package.__path__, models_package.__name__ + "."
    ):
        importlib.import_module(module_name)


load_all_models()
