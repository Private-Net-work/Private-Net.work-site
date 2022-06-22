import datetime

from flask import Blueprint, abort, render_template, escape, request

from blueprints.auth import is_admin
from data import db_session
from data.docs import Doc
from data.notes import Note

notes_bp = Blueprint("notes", "notes")
SYMBOLS = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890")


@notes_bp.route('/', methods=["GET", "POST"])
def create_note():
    if request.method == "POST":  # used for uptime monitoring
        return "OK"
    show_description = False if request.cookies.get('showdescription') == "false" else True
    return render_template("disposable_notes/create_note.jinja2", year=datetime.datetime.now().year,
                           show_descriprion=show_description, is_admin=is_admin())


@notes_bp.route('/note/<string:note_id>')
@notes_bp.route('/<string:note_id>')
def view_note(note_id):
    if not 9 <= len(note_id) <= 12:
        abort(404)
    show_description = False if request.cookies.get('showdescription') == "false" else True
    session = db_session.create_session()
    note = session.query(Note).get(note_id)
    if not note:
        doc = session.query(Doc).get(note_id)
        if not doc:
            abort(404)
        elif doc.delete_date < datetime.datetime.now():
            session.delete(doc)
            session.commit()
            abort(404)
    elif note.delete_date < datetime.datetime.now():
        session.delete(note)
        session.commit()
        abort(404)
    return render_template("disposable_notes/view_note.jinja2", year=datetime.datetime.now().year,
                           note_id=note_id, show_descriprion=show_description,
                           is_admin=is_admin(), old="false")


@notes_bp.route('/about')
def about_notes():
    return render_template("disposable_notes/about_notes.jinja2", year=datetime.datetime.now().year)


@notes_bp.route('/about/formatting')
def formatting():
    return render_template("disposable_notes/formatting.jinja2", year=datetime.datetime.now().year,
                           escape=escape)


@notes_bp.route('/support')
def support():
    return render_template("disposable_notes/support.jinja2", year=datetime.datetime.now().year)
