"""
Doc model
"""
# pylint: disable=too-few-public-methods
import sqlalchemy

from .db_session import SqlAlchemyBase


class Doc(SqlAlchemyBase):
    """
    Doc model
    """
    __tablename__ = 'docs'

    id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True, index=True, unique=True)
    counter = sqlalchemy.Column(sqlalchemy.Integer)
    content = sqlalchemy.Column(sqlalchemy.String)
    filename = sqlalchemy.Column(sqlalchemy.String)
    delete_date = sqlalchemy.Column(sqlalchemy.DateTime)
