"""
HTTP error handlers that render and return error pages
"""

# pylint: disable=invalid-name
import datetime

from flask import render_template, request, jsonify
from flask_babel import gettext


def default_error_handler(e, title, default_description):
    """Renders the error page with given error code,
    title and description

    :param e: error object instance
    :param title: error title to be displayed on the page
    :param default_description: error description to use unless redefined
    :return: rendered error page
    """
    description = default_description if e.description == type(e).description else e.description
    if request.path.startswith('/api/'):
        description = description.replace("<br>", "")
        return jsonify(error=e.name, code=e.code, message=description), e.code
    return render_template('disposable_notes/errors/basic_error.jinja2',
                           code=e.code, title=title, message=description,
                           year=datetime.datetime.now().year), e.code


def bad_request(e):
    """HTTP 400 Bad Request error handler

    :param e: error object instance
    :return: rendered error page
    """
    title = gettext("Bad request")  # "Ошибка в запросе"
    default_description = gettext("400 description")
    return default_error_handler(e, title, default_description)


def forbidden(e):
    """HTTP 403 Forbidden error handler

    :param e: error object instance
    return: rendered error page
    """
    title = gettext("Forbidden")  # "Доступ запрещён"
    default_description = gettext("403 description")
    return default_error_handler(e, title, default_description)


def not_found(e):
    """HTTP 404 Not Found error handler

    :param e: error object instance
    :return: rendered error page
    """
    title = gettext("Not found")  # "Страница не найдена"
    default_description = gettext("404 description")
    return default_error_handler(e, title, default_description)


def method_not_allowed(e):
    """HTTP 405 Method Not Allowed error handler

    :param e: error object instance
    :return: rendered error page
    """
    title = gettext("Unallowed method")  # "Недопустимый метод"
    default_description = gettext("405 description", method=request.method)
    return default_error_handler(e, title, default_description)


def internal_server_error(e):
    """HTTP 500 Internal Server Error error handler

    :param e: error object instance
    :return: rendered error page
    """
    title = gettext("Internal Server Error")  # "Внутренняя ошибка сервера"
    default_description = gettext("500 description")
    return default_error_handler(e, title, default_description)
