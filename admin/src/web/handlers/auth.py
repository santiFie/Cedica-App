from flask import Blueprint
from flask import render_template
from flask import request
from src.core import auth

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        auth.create_user(email=request.form["email"], nickname=request.form["nickname"], password=request.form["password"])
    return render_template("auth/register.html")
