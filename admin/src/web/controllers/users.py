from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users
bp = Blueprint('auth',__name__,url_prefix="/auth")

@bp.post("/delete_user", user_id):
    users.user_delete(user_id=user_id)
    flash("User deleted successfully")
    return redirect(url_for("users.list_users"))