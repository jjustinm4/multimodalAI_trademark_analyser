from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mark_text: Mapped[str] = mapped_column(String(120), index=True)
    nice_class: Mapped[int] = mapped_column(Integer, index=True)
    goods_description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20))
    owner_name: Mapped[str] = mapped_column(String(120))
    filing_date: Mapped[date] = mapped_column(Date)
    logo_svg: Mapped[str | None] = mapped_column(Text, nullable=True)
    phonetic_keys: Mapped[list] = mapped_column(JSONB, default=list)
    text_embedding = mapped_column(Vector(384))
    goods_embedding = mapped_column(Vector(384))
    logo_embedding = mapped_column(Vector(512), nullable=True)


class PrecedentChunk(Base):
    __tablename__ = "precedent_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    proceeding_number: Mapped[str] = mapped_column(String(20), index=True)
    decision_date: Mapped[date] = mapped_column(Date)
    mark_a: Mapped[str] = mapped_column(String(120))
    mark_b: Mapped[str] = mapped_column(String(120))
    outcome: Mapped[str] = mapped_column(String(20))
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(Vector(384))


class NiceClass(Base):
    __tablename__ = "nice_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_number: Mapped[int] = mapped_column(Integer, index=True)
    class_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(Vector(384))
