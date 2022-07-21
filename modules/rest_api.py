import datetime
from random import choice, randint
from string import ascii_letters, digits

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.docs import Doc
from data.notes import Note
from data.stats import Stats


def abort_if_note_not_found(note_id):
    session = db_session.create_session()
    note = session.query(Note).get(note_id)
    if not note:
        doc = session.query(Doc).get(note_id)
        if not doc:
            abort(404, message=f"Note {note_id} not found")
        if doc.delete_date < datetime.datetime.now():
            session.delete(doc)
            session.commit()
            abort(404, message=f"Note {note_id} not found")
    else:
        if note.delete_date < datetime.datetime.now():
            session.delete(note)
            session.commit()
            abort(404, message=f"Note {note_id} not found")


class NoteResource(Resource):
    def get(self, note_id):
        abort_if_note_not_found(note_id)
        return jsonify({'exist': True})

    def delete(self, note_id):
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        note = session.query(Note).get(note_id)
        doc, ext = False, None
        if not note:
            note = session.query(Doc).get(note_id)
            ext = note.filename
            doc = True
        session.delete(note)
        session.commit()
        Stats.view_note(session)
        return jsonify({'content': note.content, "counter": note.counter, "doc": doc, "ext": ext})


class NotesResource(Resource):
    def post(self):
        session = db_session.create_session()

        parser = reqparse.RequestParser()
        parser.add_argument('content', required=True)
        parser.add_argument('counter', required=True)
        parser.add_argument('deletein', required=True)
        parser.add_argument('doc', required=True)
        parser.add_argument('ext', required=True)
        args = parser.parse_args()

        if "deletein" in args.keys():
            delta_min = int(args["deletein"]) if 0 < int(args["deletein"]) <= 10080 else 10080
        else:
            delta_min = 10080

        if len(args["counter"]) < 16 or len(args["counter"]) > 30:
            abort(400, message=f"Counter length {len(args['counter'])} is invalid!")

        delete_date = datetime.datetime.now() + datetime.timedelta(minutes=delta_min)

        note_id = "".join([choice(ascii_letters + digits) for _ in range(randint(9, 12))])
        while session.query(Note).get(note_id):
            note_id = "".join([choice(ascii_letters + digits) for _ in range(randint(9, 12))])

        if args['doc'] == "true":
            if len(args["content"]) < 8400000:
                doc = Doc(
                    id=note_id,
                    content=args['content'],
                    counter=args['counter'],
                    delete_date=delete_date,
                    filename=args['ext']
                )
                session.add(doc)
                session.commit()

                Stats.new_note(session)
                return jsonify({'id': doc.id})
            return abort(413, message=f"Content length {len(args['content'])} is invalid!")

        else:
            if 0 < len(args["content"]) <= 10000:
                note = Note(
                    id=note_id,
                    content=args['content'],
                    counter=args['counter'],
                    delete_date=delete_date
                )
                session.add(note)
                session.commit()

                Stats.new_note(session)
                return jsonify({'id': note.id})
            return abort(413, message=f"Content length {len(args['content'])} is invalid!")
