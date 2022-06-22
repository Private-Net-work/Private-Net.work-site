import sqlalchemy

from blueprints.auth import is_admin
from data.db_session import create_session
from .db_session import SqlAlchemyBase


class Stats(SqlAlchemyBase):
    __tablename__ = 'stats'

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.Integer)

    @staticmethod
    def create_fields():
        s = create_session()
        fields = ["created", "viewed", "mycreated", "myviewed", "construction"]
        for field in fields:
            row = s.query(Stats).filter(Stats.name == field).first()
            if not row:
                s.add(Stats(name=field, value=0))
        s.commit()

    @staticmethod
    def new_note(session):
        if is_admin():
            mycreated = session.query(Stats).filter(Stats.name == "mycreated").first()
            mycreated.value += 1
        else:
            created = session.query(Stats).filter(Stats.name == "created").first()
            created.value += 1
        session.commit()

    @staticmethod
    def view_note(session):
        if is_admin():
            myviewed = session.query(Stats).filter(Stats.name == "myviewed").first()
            myviewed.value += 1
        else:
            viewed = session.query(Stats).filter(Stats.name == "viewed").first()
            viewed.value += 1
        session.commit()
