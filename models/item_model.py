from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    store_id: Mapped[int] = mapped_column(unique=False, nullable=True)
