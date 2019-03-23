"""empty message

Revision ID: 77fdab1d41b9
Revises: 
Create Date: 2019-03-16 12:32:44.518367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77fdab1d41b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicleMake',
    sa.Column('make_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('make_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicleModel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('make_id', sa.Integer(), nullable=False),
    sa.Column('year', sa.String(length=50), nullable=False),
    sa.Column('price', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['make_id'], ['vehicleMake.make_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicleModel')
    op.drop_table('vehicleMake')
    # ### end Alembic commands ###
