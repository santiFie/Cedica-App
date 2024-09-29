from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users


bp = Blueprint('users',__name__,url_prefix="/users")

bp.post("/update")
def user_update():
    """
    Updates a user
    """
    # Tener en cuenta la forma de mostrar el rol en el formulario porque aca se recibe un id y hay que mostrar un string
    users.edit(email=request.form["email"], nickname=request.form["nickname"], system_admin=request.form["system_admin"], role_id=request.form["role_id"])
    return redirect(url_for("users.users_list"))

bp.get("/edit")
def user_edit():
    """
    Edits a user
    """
    return render_template("users/edit.html")