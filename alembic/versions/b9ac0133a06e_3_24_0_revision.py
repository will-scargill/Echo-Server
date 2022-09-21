"""3.24.0 Revision

Revision ID: b9ac0133a06e
Revises: 
Create Date: 2022-09-20 14:37:55.226426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ac0133a06e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("userRoles") as batch_op:
        batch_op.add_column(sa.Column("publicKey", sa.String(300)))
        batch_op.drop_column("eID")


def downgrade() -> None:
    with op.batch_alter_table("userRoles") as batch_op:
        batch_op.add_column(sa.Column("eID", sa.String(64)))
        batch_op.drop_column("publicKey")
