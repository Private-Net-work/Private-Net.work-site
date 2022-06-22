import datetime

from flask import render_template, request, jsonify
from flask_babel import gettext


def default_error_handler(e, title, default_description):
    description = default_description if e.description == type(e).description else e.description
    if request.path.startswith('/api/'):
        description = description.replace("<br>", "")
        return jsonify(error=e.name, code=e.code, message=description), e.code
    else:
        return render_template('disposable_notes/errors/basic_error.jinja2',
                               code=e.code, title=title, message=description,
                               year=datetime.datetime.now().year), e.code


def bad_request(e):
    title = gettext("Bad request")  # "Ошибка в запросе"
    default_description = gettext("400 description")
    return default_error_handler(e, title, default_description)


def forbidden(e):
    title = gettext("Forbidden")  # "Доступ запрещён"
    default_description = gettext("403 description")
    return default_error_handler(e, title, default_description)


def not_found(e):
    title = gettext("Not found")  # "Страница не найдена"
    default_description = gettext("404 description")
    return default_error_handler(e, title, default_description)


def method_not_allowed(e):
    title = gettext("Unallowed method")  # "Недопустимый метод"
    default_description = gettext("405 description", method=request.method)
    return default_error_handler(e, title, default_description)


def internal_server_error(e):
    title = gettext("Internal Server Error")  # "Внутренняя ошибка сервера"
    default_description = gettext("500 description")
    return default_error_handler(e, title, default_description)
