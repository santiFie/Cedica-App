from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from src.core import auth

bp = Blueprint('auth',__name__,url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        auth.create_user(email=request.form["email"], nickname=request.form["nickname"], password=request.form["password"])
    return render_template("auth/register.html")

@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def verification():
    params = request.form

    user = auth.check_user(params["email"],params["password"])

    if not user:
        redirect(url_for("auth.login"))

    session["user"] = user.email

    return redirect(url_for('home'))

@bp.get("/logout")
def logout():
    pass