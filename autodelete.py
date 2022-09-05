"""
A service of deleting expired unread notes. Must be a crontab job
"""
import datetime

from config import Config
from data import db_session
from data.docs import Doc
from data.notes import Note

db_session.global_init(Config.DB)

session = db_session.create_session()
to_delete = session.query(Note).filter(Note.delete_date < datetime.datetime.now()).all()
to_delete += session.query(Doc).filter(Doc.delete_date < datetime.datetime.now()).all()
for i in range(0, len(to_delete), 10):
    for j in range(i, i + 10):
        try:
            session.delete(to_delete[j])
        except IndexError:
            break
    session.commit()
session.execute("VACUUM")
print("Success!")
