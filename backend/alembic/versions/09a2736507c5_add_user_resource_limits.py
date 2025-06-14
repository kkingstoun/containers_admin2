"""Add user resource limits

Revision ID: 09a2736507c5
Revises: 075dc4526f80
Create Date: 2025-06-05 12:12:36.387870

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09a2736507c5"
down_revision = "075dc4526f80"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("max_containers", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("max_gpus", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "max_gpus")
    op.drop_column("users", "max_containers")
    # ### end Alembic commands ###
