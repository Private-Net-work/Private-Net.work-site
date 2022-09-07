"""
DB initialisation and creating sessions
"""
# pylint: disable=invalid-name, global-statement, global-variable-not-assigned
import os

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
from sqlalchemy import orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    """
    DB initialisation
    :param db_file: path to DB
    """
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Path to database file is required")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    if not os.path.exists("data/db"):
        os.mkdir("data/db")
    print(f"Connecting to DB {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """
    Creates a new DB session
    :return: session object
    """
    global __factory
    return __factory()
