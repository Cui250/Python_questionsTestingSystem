"""empty message

Revision ID: b05475e624a6
Revises: 226329cae96c
Create Date: 2024-06-01 19:52:14.208654

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b05475e624a6'
down_revision = '226329cae96c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choicequestion', schema=None) as batch_op:
        batch_op.alter_column('question',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('option',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('answer',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('analysis',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('course',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('knowledge_point',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('level',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choicequestion', schema=None) as batch_op:
        batch_op.alter_column('level',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('knowledge_point',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('course',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('analysis',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('answer',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('option',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('question',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)

    # ### end Alembic commands ###