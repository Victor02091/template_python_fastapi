from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from sqlalchemy.sql import func


@declarative_mixin
class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp when the record was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when the record was last updated",
    )
