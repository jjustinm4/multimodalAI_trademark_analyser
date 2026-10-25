"""initial schema: marks, precedent_chunks, nice_classes with pgvector

Revision ID: 001
Revises:
"""
from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.execute(
        """
        CREATE TABLE marks (
            id SERIAL PRIMARY KEY,
            mark_text VARCHAR(120) NOT NULL,
            nice_class INTEGER NOT NULL,
            goods_description TEXT NOT NULL,
            status VARCHAR(20) NOT NULL,
            owner_name VARCHAR(120) NOT NULL,
            filing_date DATE NOT NULL,
            logo_svg TEXT,
            phonetic_keys JSONB NOT NULL DEFAULT '[]'::jsonb,
            text_embedding vector(384),
            goods_embedding vector(384),
            logo_embedding vector(512)
        )
        """
    )
    op.execute("CREATE INDEX ix_marks_mark_text ON marks (mark_text)")
    op.execute("CREATE INDEX ix_marks_nice_class ON marks (nice_class)")
    op.execute("CREATE INDEX ix_marks_phonetic_keys ON marks USING gin (phonetic_keys)")
    op.execute("CREATE INDEX ix_marks_text_embedding ON marks USING hnsw (text_embedding vector_cosine_ops)")
    op.execute("CREATE INDEX ix_marks_logo_embedding ON marks USING hnsw (logo_embedding vector_cosine_ops)")

    op.execute(
        """
        CREATE TABLE precedent_chunks (
            id SERIAL PRIMARY KEY,
            proceeding_number VARCHAR(20) NOT NULL,
            decision_date DATE NOT NULL,
            mark_a VARCHAR(120) NOT NULL,
            mark_b VARCHAR(120) NOT NULL,
            outcome VARCHAR(20) NOT NULL,
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            embedding vector(384)
        )
        """
    )
    op.execute("CREATE INDEX ix_precedent_proceeding ON precedent_chunks (proceeding_number)")
    op.execute("CREATE INDEX ix_precedent_embedding ON precedent_chunks USING hnsw (embedding vector_cosine_ops)")

    op.execute(
        """
        CREATE TABLE nice_classes (
            id SERIAL PRIMARY KEY,
            class_number INTEGER NOT NULL,
            class_name VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            embedding vector(384)
        )
        """
    )
    op.execute("CREATE INDEX ix_nice_classes_number ON nice_classes (class_number)")
    op.execute("CREATE INDEX ix_nice_classes_embedding ON nice_classes USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS nice_classes")
    op.execute("DROP TABLE IF EXISTS precedent_chunks")
    op.execute("DROP TABLE IF EXISTS marks")
