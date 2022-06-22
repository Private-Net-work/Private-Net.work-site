import hashlib
from secrets import compare_digest

from flask import Blueprint, request, current_app, make_response

auth_bp = Blueprint("auth", "auth")


def is_admin():
    return False if not request.cookies.get("auth") else \
        compare_digest(request.cookies.get("auth"), current_app.config["AUTH_COOKIE"])


@auth_bp.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        password = request.form["password"]
        if compare_digest(hashlib.sha512(bytes(password, encoding='utf-8')).digest().hex(),
                          current_app.config["ADMIN_PASSWORD"]):
            response = make_response("You have logged in successfully!")
            response.set_cookie("auth", current_app.config["AUTH_COOKIE"],
                                max_age=3600 * 24 * 365 * 100, secure=True)
            return response
        else:
            return "Wrong password!"
    else:
        return "<form method='post'>" \
               "<input type='password' name='password' placeholder='password'\\>" \
               "<button type='submit'>Log in</button>" \
               "</form>"
