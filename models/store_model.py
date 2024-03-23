from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
