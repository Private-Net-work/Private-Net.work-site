"""
Note model
"""
# pylint: disable=too-few-public-methods
import sqlalchemy

from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase):
    """
    Note model
    """
    __tablename__ = 'notes'

    id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True, index=True, unique=True)
    counter = sqlalchemy.Column(sqlalchemy.Integer)
    content = sqlalchemy.Column(sqlalchemy.String)
    delete_date = sqlalchemy.Column(sqlalchemy.DateTime)
