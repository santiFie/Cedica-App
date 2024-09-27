from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from src.core import auth

bp = Blueprint('auth',__name__,url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        user = auth.check_user(request.form["email"], request.form["password"])

        if not user:
            auth.create_user(email=request.form["email"], nickname=request.form["nickname"], password=request.form["password"])
            return redirect(url_for("auth.login"))
        else:
            flash("Ya tienes una cuenta. Por favor, inicia sesión.", "info")
        

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
    if(session.get('user')):
        del session['user']
        session.clear()
    return redirect(url_for('auth.login'))