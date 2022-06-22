import datetime
import hashlib
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

import requests
from flask import request, current_app, render_template
from flask_babel import gettext
from werkzeug.exceptions import InternalServerError

from blueprints.auth import is_admin
from blueprints.errorhandling import default_error_handler
from config import Config
from data.db_session import create_session
from data.stats import Stats


class TgHandler(logging.StreamHandler):
    on_same_line = False

    def emit(self, record):
        msg = record.message
        if "Traceback" in msg:
            msg = msg.replace("Error: ", "Error: <b>") + "</b>"
        else:
            msg = f"<b>{msg}</b>"
        res = requests.get(f'https://api.telegram.org/bot{current_app.config["TG_LOGGER_TOKEN"]}/sendMessage',
                           params={"chat_id": Config.TG_ADMIN_ID,
                                   "text": msg,
                                   "parse_mode": "HTML"})
        logger.info(str(res))


tg_handler = TgHandler()
tg_handler.setLevel(logging.ERROR)
tg_handler.setFormatter(logging.Formatter(
    '%(levelname)s %(asctime)s: %(message)s'
))

file_handler = TimedRotatingFileHandler("./logs/main.log", when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(levelname)s %(asctime)s: %(message)s'
))


def before_request():
    s = create_session()
    construction_mode = s.query(Stats).filter(Stats.name == "construction").first()
    if construction_mode.value == 1:
        if not is_admin() and request.path != "/auth" or \
                is_admin() and request.path != "/construction/off":
            code = 503
            title = gettext("Проводятся технические работы")
            description = gettext("construction description")
            return render_template('disposable_notes/errors/construction.jinja2',
                                   code=code, title=title, message=description,
                                   year=datetime.datetime.now().year), code


def after_request(response):
    ip = request.headers.get("Cf-Connecting-Ip", None)
    ip_hash = hashlib.sha512(ip.encode()).hexdigest()[:15] if ip else "NoIp"
    path = request.full_path[:-1] if request.full_path[-1] == "?" else request.full_path
    status_type = int(str(response.status_code)[0])
    country = request.headers.get("Cf-Ipcountry", "NoCountry")
    referer = request.headers.get("Referer", "NoReferer")
    modified = request.headers.get("If-Modified-Since", "NoIfModif")
    if ip_hash == "NoIp":
        ip_hash = request.remote_addr
    if path.startswith("/static"):
        logger.debug('%s %s %s %s %s %s %s Referer: %s IfModif: %s', ip_hash, country, request.method,
                     request.scheme,
                     request.host, path, response.status, referer, modified)
    else:
        if status_type == 5:
            logger.error('%s %s %s %s %s %s %s Referer: %s IfModif: %s', ip_hash, country, request.method,
                         request.scheme,
                         request.host, path, response.status, referer, modified)
        elif status_type == 4:
            logger.warning('%s %s %s %s %s %s %s Referer: %s IfModif: %s', ip_hash, country, request.method,
                           request.scheme,
                           request.host, path, response.status, referer, modified)
        else:
            logger.info('%s %s %s %s %s %s %s Referer: %s IfModif: %s', ip_hash, country, request.method,
                        request.scheme,
                        request.host, path, response.status, referer, modified)

    return response


def exceptions(e):
    tb = traceback.format_exc()
    logger.error('\n%s', tb[:-1])
    title = gettext("Internal server error")
    default_description = gettext("500 description")
    return default_error_handler(InternalServerError(), title, default_description)


logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
