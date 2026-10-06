"""Initial SpiderVerse schema with users and permissions.

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)

    op.create_table(
        "universe",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column("actor", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "character",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("alias", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column("gender", sa.String(length=50), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("actor", sa.String(length=100), nullable=False),
        sa.Column("type", sa.String(length=150), nullable=False),
        sa.Column("powers", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "movie",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("poster", sa.String(length=255), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("director", sa.String(length=150), nullable=False),
        sa.Column("universe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["universe_id"], ["universe.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "character_universe",
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.Column("universe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["character_id"], ["character.id"]),
        sa.ForeignKeyConstraint(["universe_id"], ["universe.id"]),
        sa.PrimaryKeyConstraint("character_id", "universe_id"),
    )

    op.create_table(
        "character_movie",
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["character_id"], ["character.id"]),
        sa.ForeignKeyConstraint(["movie_id"], ["movie.id"]),
        sa.PrimaryKeyConstraint("character_id", "movie_id"),
    )


def downgrade():
    op.drop_table("character_movie")
    op.drop_table("character_universe")
    op.drop_table("movie")
    op.drop_table("character")
    op.drop_table("universe")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
