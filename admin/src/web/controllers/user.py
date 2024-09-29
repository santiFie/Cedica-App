from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users, auth
from src.core.models.users import Role


bp = Blueprint('users',__name__,url_prefix="/users")

bp.post("/update")
def user_update():
    """
    Updates a user
    """
    user = users.edit(nickname=request.form["nickname"], system_admin=request.form["system_admin"], role_id=request.form["role_id"])
    if not user:
        flash("No existe el usuario")
    else:
        flash("Usuario actualizado")
    return redirect(url_for("users.users_list"), flash=flash)

bp.get("/edit")
def user_edit(user_id):
    """
    Edits a user
    """
    user = auth.find_user_by_id(user_id)
    roles = Role.query.all()
    return render_template("users/edit.html", user=user,roles=roles)