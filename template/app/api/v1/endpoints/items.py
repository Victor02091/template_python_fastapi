from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.db.crud.item import create_item, get_item_by_id, list_items
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items")


@router.get("")
async def read_items(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[ItemRead]:
    """List all items."""
    items = await list_items(db)
    return [ItemRead.model_validate(item) for item in items]


@router.get("/{item_id}")
async def read_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ItemRead:
    """Get one item by id."""
    item = await get_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return ItemRead.model_validate(item)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_item(
    item_in: ItemCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ItemRead:
    """Create a new item."""
    item = await create_item(db, item_in)
    return ItemRead.model_validate(item)
