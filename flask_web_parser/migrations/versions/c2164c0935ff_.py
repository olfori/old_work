"""empty message

Revision ID: c2164c0935ff
Revises: 
Create Date: 2020-10-09 05:49:29.980302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2164c0935ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=180), nullable=True),
    sa.Column('price', sa.String(length=120), nullable=True),
    sa.Column('href', sa.String(length=180), nullable=True),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('view_count', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ad_name'), 'ad', ['name'], unique=False)
    op.create_table('search_query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=180), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_search_query_name'), 'search_query', ['name'], unique=True)
    op.create_table('ads',
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.Column('sq_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['ad.id'], ),
    sa.ForeignKeyConstraint(['sq_id'], ['search_query.id'], ),
    sa.PrimaryKeyConstraint('ad_id', 'sq_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ads')
    op.drop_index(op.f('ix_search_query_name'), table_name='search_query')
    op.drop_table('search_query')
    op.drop_index(op.f('ix_ad_name'), table_name='ad')
    op.drop_table('ad')
    # ### end Alembic commands ###
