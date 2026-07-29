from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate


async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
    """Create and persist a new Item."""
    item = Item(name=item_in.name, description=item_in.description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_item_by_id(db: AsyncSession, item_id: int) -> Item | None:
    """Return one Item by id if found."""
    stmt: Select[tuple[Item]] = select(Item).where(Item.id == item_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_items(db: AsyncSession) -> list[Item]:
    """Return all Items ordered by id."""
    stmt: Select[tuple[Item]] = select(Item).order_by(Item.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())
