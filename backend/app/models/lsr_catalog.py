"""
IOGP Life-Saving Rules Reference Catalog Model
Source of Truth: docs/09_DATABASE_DESIGN.md §28, §62
"""

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class LSRReferenceCatalog(Base):
    __tablename__ = "lsr_reference_catalogs"

    lsr_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    rule_number: Mapped[int] = mapped_column(Integer, nullable=False)
    rule_title: Mapped[str] = mapped_column(String(100), nullable=False)
    icon_name: Mapped[str] = mapped_column(String(50), nullable=False)
    canonical_definition: Mapped[str] = mapped_column(Text, nullable=False)
    active_version: Mapped[str] = mapped_column(String(50), nullable=False)
