from flask import Blueprint, render_template, request, send_from_directory, current_app
from flask_babel import gettext

pseudo_static_bp = Blueprint("pseudo_static", "pseudo_static")


@pseudo_static_bp.route('/robots.txt')
@pseudo_static_bp.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


@pseudo_static_bp.route('/static/notes/create_note.js')
def create_note_js():
    data = {
        'Некорректная длина записки!': gettext('Некорректная длина записки!'),
        'link info': gettext('link info'),
        'Скопировать': gettext('Скопировать'),
        'Скопировано': gettext('Скопировано'),
        'js 400 error': gettext('js 400 error'),
        'js 500 error': gettext('js 500 error'),
        'js unknown error': gettext('js unknown error'),
        'heavy doc': gettext('heavy doc'),
        'heavy content': gettext('heavy content')
    }
    return render_template("disposable_notes/js/create_note.js", data=data)


@pseudo_static_bp.route('/static/notes/view_note.js')
def view_note_js():
    data = {
        'js save data': gettext('js save data'),
        'Выйти': gettext('Выйти'),
        'js already read': gettext('js already read'),
        'js 500 error': gettext('js 500 error'),
        'js unknown error': gettext('js unknown error'),
        'download file': gettext('download file')
    }
    return render_template("disposable_notes/js/view_note.js", data=data)
