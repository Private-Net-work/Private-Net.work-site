"""
Main project module, Flask application
"""
from flask import Flask, request
from flask_babel import Babel
from flask_restful import Api
from os import getcwd

from blueprints.auth import auth_bp
from blueprints.errorhandling import bad_request, forbidden, not_found, method_not_allowed, internal_server_error
from blueprints.notes import notes_bp
from blueprints.pseudo_static import pseudo_static_bp
from blueprints.stats import stats_bp
from config import DevelopmentConfig, ProductionConfig
from data import db_session
from data.stats import Stats
from modules import rest_api
from modules.logger import after_request, exceptions, before_request, logger, tg_handler

app = Flask(__name__)
babel = Babel(app)
api = Api(app)
DEBUG = False

if getcwd().startswith("C"):  # for testing machine
    app.debug = DEBUG
    ConfigObject = DevelopmentConfig
else:  # for production machine
    app.debug = False
    ConfigObject = ProductionConfig
    logger.addHandler(tg_handler)
    app.register_error_handler(Exception, exceptions)
    app.after_request(after_request)

app.config.from_object(ConfigObject())
db_session.global_init(app.config["DB"])
Stats.create_fields()


@babel.localeselector
def get_locale():
    """Get visitor's locale
    :return: country code
    """
    if request.cookies.get('lang'):
        return request.cookies.get('lang')
    if request.args.get("lang") == "ru" or request.headers.get("Cf-Ipcountry", "NoCountry") == "RU":
        return "ru"
    if request.args.get("lang") == "en":
        return "en"
    return request.accept_languages.best_match(app.config["LANGUAGES"].keys())


api.add_resource(rest_api.NoteResource, '/api/note/<string:note_id>')
api.add_resource(rest_api.NotesResource, '/api/note')

app.register_blueprint(notes_bp)
app.register_blueprint(pseudo_static_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(stats_bp)

app.register_error_handler(400, bad_request)
app.register_error_handler(403, forbidden)
app.register_error_handler(404, not_found)
app.register_error_handler(405, method_not_allowed)
app.register_error_handler(500, internal_server_error)
app.before_request(before_request)

if __name__ == '__main__':
    app.run("127.0.0.1")
