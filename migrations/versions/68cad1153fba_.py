"""empty message

Revision ID: 68cad1153fba
Revises:
Create Date: 2024-03-08 13:45:54.261582

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "68cad1153fba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cards",
        sa.Column("code", sa.String(length=12), nullable=False),
        sa.Column("cardType", sa.Enum("500", "1000", "2000", "5000", "10000"), nullable=False),
        sa.Column("isValid", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("publicId", sa.String(length=36), nullable=False),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("publicId"),
    )
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("isActive", sa.Boolean(), nullable=False),
        sa.Column("isAdmin", sa.Boolean(), nullable=False),
        sa.Column("passwordHash", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("publicId", sa.String(length=36), nullable=False),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("publicId"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("cards")
    # ### end Alembic commands ###