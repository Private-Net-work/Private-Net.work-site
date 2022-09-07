"""
All public endpoints (notes-related, docs, contacts, etc.)
"""
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
    """Note creating endpoint

    :return: rendered main page
    """
    if request.method == "POST":  # used for uptime monitoring
        return "OK"
    show_description = bool(request.cookies.get('showdescription') != "false")
    return render_template("disposable_notes/create_note.jinja2", year=datetime.datetime.now().year,
                           show_descriprion=show_description, is_admin=is_admin())


@notes_bp.route('/note/<string:note_id>')
@notes_bp.route('/<string:note_id>')
def view_note(note_id):
    """Viewing note endpoint

    :param note_id: Note id from URL
    :return: rendered page of note viewing
    """
    if not 9 <= len(note_id) <= 12:
        abort(404)
    show_description = bool(request.cookies.get('showdescription') != "false")
    session = db_session.create_session()
    note = session.query(Note).get(note_id)
    if note:
        if note.delete_date < datetime.datetime.now():
            session.delete(note)
            session.commit()
            abort(404)
    else:
        doc = session.query(Doc).get(note_id)
        if doc:
            if doc.delete_date < datetime.datetime.now():
                session.delete(doc)
                session.commit()
                abort(404)
        else:
            abort(404)
    return render_template("disposable_notes/view_note.jinja2", year=datetime.datetime.now().year,
                           note_id=note_id, show_descriprion=show_description,
                           is_admin=is_admin(), old="false")


@notes_bp.route('/about')
def about_notes():
    """Endpoint with site description

    :return: rendered about page
    """
    return render_template("disposable_notes/about_notes.jinja2", year=datetime.datetime.now().year)


@notes_bp.route('/about/formatting')
def formatting():
    """Formatting guide endpoint

    :return: rendered page
    """
    return render_template("disposable_notes/formatting.jinja2", year=datetime.datetime.now().year,
                           escape=escape)


@notes_bp.route('/support')
def support():
    """Support page endpoint

    :return: rendered support page
    """
    return render_template("disposable_notes/support.jinja2", year=datetime.datetime.now().year)


@notes_bp.route('/donate')
def donate():
    """Donate page endpoint

    :return rendered donate page
    """
    btc = "bc1qceazcfujhdatpgpxnpdy7aj5wyh8ljxsxnz60e"
    eth = "0xa281cC5Eb0c6fCCfc1120209297E504170EAC06a"
    trx = "TTokMLQwvrm3FfH6LQaEY46vCYGRCJJXcm"
    bnb = "bnb1a7prktewjjejm98u7ysdpdzgvukr2sges6xx3m"
    xrp = "rnwWE36sYAscpmUY5bgR9gGGfTHmtRf8Bw"
    doge = "DR2DhCXnW6T9QK8K6yoqG64Ro1yT7HoWDR"
    ltc = "ltc1q6nur0ym53vemtfs0wrsm6skktln4amfs6kgzsk"
    xmr = "8Agen4JiAMYEnwyhyyDKkZLZUuhVFwQqiTYGuocJ15sv" \
          "Bv3FBg2gzzyjU6D5tCWhZcDKxZb8VQ2zm1gZXNx1H2n9Li6HmyF"
    return render_template("disposable_notes/donate.jinja2",
                           btc=btc, eth=eth, trx=trx, bnb=bnb, xrp=xrp, doge=doge, ltc=ltc, xmr=xmr,
                           year=datetime.datetime.now().year)
