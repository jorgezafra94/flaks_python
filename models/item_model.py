from typing import List

from sqlalchemy import Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), unique=False, nullable=True)
    store: Mapped["StoreModel"] = relationship(back_populates="items")
    tags: Mapped[List["TagModel"]] = relationship(back_populates="items", secondary="items_tags")
