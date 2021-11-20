"""empty message

Revision ID: de316f0831f9
Revises: 60f151e462e9
Create Date: 2021-11-19 23:38:39.754126

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "de316f0831f9"
down_revision = "60f151e462e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_balance_operation", table_name="balance")
    op.drop_index("ix_balance_type", table_name="balance")
    op.drop_column("balance", "type")
    op.alter_column("clients", "email", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("clients", "phone", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("clients", "owner_id", existing_type=postgresql.UUID(), nullable=False)
    op.add_column(
        "orders",
        sa.Column(
            "payment_type",
            sa.Enum("PAYMENT_OF_EMPLOYEES", "PAYMENT_OF_SUPPLIERS", "ANOTHER_PAYMENTS", name="paymenttype"),
            nullable=False,
        ),
    )
    op.alter_column("orders", "owner_id", existing_type=postgresql.UUID(), nullable=False)
    op.add_column("clients", sa.Column("zip_code", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column("clients", sa.Column("address", sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("orders", "owner_id", existing_type=postgresql.UUID(), nullable=True)
    op.drop_column("orders", "payment_type")
    op.alter_column("clients", "owner_id", existing_type=postgresql.UUID(), nullable=True)
    op.alter_column("clients", "phone", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("clients", "email", existing_type=sa.VARCHAR(), nullable=True)
    op.add_column(
        "balance",
        sa.Column("type", postgresql.ENUM("DEBT", "CREDIT", name="balancetype"), autoincrement=False, nullable=True),
    )
    op.create_index("ix_balance_type", "balance", ["type"], unique=False)
    op.create_index("ix_balance_operation", "balance", ["operation"], unique=False)
    op.drop_column("clients", "address")
    op.drop_column("clients", "zip_code")

    # ### end Alembic commands ###
