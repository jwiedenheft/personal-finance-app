"""Add category income divisions

Revision ID: 95de38c12724
Revises: 2bb9415ce46c
Create Date: 2024-01-07 18:08:31.274075

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95de38c12724"
down_revision = "2bb9415ce46c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category_income",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("income_id", sa.Integer(), nullable=False),
        sa.Column("category_code", sa.String(length=10), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_code"],
            ["category.code"],
        ),
        sa.ForeignKeyConstraint(
            ["income_id"],
            ["income.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("income", schema=None) as batch_op:
        batch_op.drop_column("percent_spend")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("income", schema=None) as batch_op:
        batch_op.add_column(sa.Column("percent_spend", sa.INTEGER(), nullable=False))

    op.drop_table("category_income")
    # ### end Alembic commands ###
