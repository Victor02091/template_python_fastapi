from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    """Shared Item payload fields."""

    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    """Payload used to create an Item."""


class ItemRead(ItemBase):
    """API representation returned to clients."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
