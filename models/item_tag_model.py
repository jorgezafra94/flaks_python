from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.db import db


class ItemTagModel(db.Model):
    """
    This is going to be the middle table to create the many to many relationship
    """
    __tablename__ = "items_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
