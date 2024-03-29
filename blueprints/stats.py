"""
Stats pages for admin
"""
from flask import Blueprint, abort

from blueprints.auth import is_admin
from data import db_session
from data.stats import Stats

stats_bp = Blueprint("stats", "stats")


@stats_bp.route("/stats")
def stats():
    """Stats endpoint

    :return: rendered stats page
    """
    if is_admin():
        session = db_session.create_session()
        created = session.query(Stats).filter(Stats.name == "created").first().value
        viewed = session.query(Stats).filter(Stats.name == "viewed").first().value
        mycreated = session.query(Stats).filter(Stats.name == "mycreated").first().value
        myviewed = session.query(Stats).filter(Stats.name == "myviewed").first().value
        return f"""
        <table>
        <tr><td>created</td><td>{created}</td>
        <tr><td>viewed</td><td>{viewed}</td>
        <tr><td></td></tr>
        <tr><td>my created</td><td>{mycreated}</td>
        <tr><td>my viewed</td><td>{myviewed}</td>
        </table>
        """
    abort(403)
    return ""


@stats_bp.route("/construction/on")
def enable_construction_mode():
    """Enabling construction mode endpoint

    :return: response with confirmation word
    """
    if is_admin():
        session = db_session.create_session()
        construction_mode = session.query(Stats).filter(Stats.name == "construction").first()
        construction_mode.value = 1
        session.commit()
        return "ON!"
    abort(403)
    return ""


@stats_bp.route("/construction/off")
def disable_construction_mode():
    """Disabling construction mode endpoint

    :return: response with confirmation word
    """
    if is_admin():
        session = db_session.create_session()
        construction_mode = session.query(Stats).filter(Stats.name == "construction").first()
        construction_mode.value = 0
        session.commit()
        return "OFF!"
    abort(403)
    return ""
