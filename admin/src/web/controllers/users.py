from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users, auth
bp = Blueprint('auth',__name__,url_prefix="/auth")

@bp.post("/delete_user")
def delete_user():
    user_email = request.form.get("user_email")
    users.user_delete(user_email)
    flash("User deleted successfully")
    return redirect(url_for("users.list_users"))