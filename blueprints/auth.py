"""
Admin authentication
"""
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import compare_digest

from flask import Blueprint, request, current_app, make_response

auth_bp = Blueprint("auth", "auth")


def is_admin():
    """
    Checking if the visitor is the administrator of the site
    :return: true if admin, else false
    """
    return False if not request.cookies.get("auth") else \
        compare_digest(request.cookies.get("auth"), current_app.config["AUTH_COOKIE"])


@auth_bp.route("/auth", methods=["GET", "POST"])
def auth():
    """
    Authentication page for admin
    :return: rendered authentication page
    """
    if request.method == "POST":
        password = request.form["password"]
        if check_password_hash(current_app.config["ADMIN_PASSWORD"], password):
            response = make_response("You have logged in successfully!")
            response.set_cookie("auth", current_app.config["AUTH_COOKIE"],
                                max_age=3600 * 24 * 365 * 100, secure=True)
            return response
        return "Wrong password!"
    return "<form method='post'>" \
           "<input type='password' name='password' placeholder='password'\\>" \
           "<button type='submit'>Log in</button>" \
           "</form>"
