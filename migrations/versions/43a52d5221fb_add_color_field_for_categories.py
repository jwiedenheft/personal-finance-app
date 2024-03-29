"""Add color field for categories

Revision ID: 43a52d5221fb
Revises: 2bb9415ce46c
Create Date: 2024-01-06 11:51:59.649615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "43a52d5221fb"
down_revision = "2bb9415ce46c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "color", sa.String(length=6), nullable=False, server_default="ffffff"
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.drop_column("color")

    # ### end Alembic commands ###
