from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users


bp = Blueprint('users',__name__,url_prefix="/users")

bp.get("/")
def users_list():  # preguntar como tienen que ser los nombres list_users o users_list

    #obtengo nro de pagina o por defecto tomo el 1
    page = request.args.get('page', 1, type=int) 

    if request.method == "GET":
        users = users.find_users(page)

        if not users:
            flash("No hay usuarios cargados en el sistema.", "info")
            return render_template("home.html")
        
    return render_template("users/show_users.html", user_list = users)
        
        



