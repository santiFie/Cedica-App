from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users 


bp = Blueprint('users',__name__,url_prefix="/users")

@bp.get("/")
def users_list():  # preguntar como tienen que ser los nombres list_users o users_list

    #obtengo nro de pagina o por defecto tomo el 1
    page = request.args.get('page', 1, type=int) 

    # obtengo los filtros del formulario
    email = request.args.get('email', None)
    active = request.args.get('active', None)
    role = request.args.get('role', None)
    sort_by = request.args.get('sort_by', None)

     # Convertir el filtro 'active' a un valor booleano
    if active == 'SI':
        active = True
    elif active == 'NO':
        active = False
    else:
        active = None  # No aplicar filtro

    # find_users tambien me devuelve la cantidad maxima de paginas para que sea evaluado en el html
    all_users, max_pages = users.find_users(page=page, email=email, active=active, role_name=role, sort_by=sort_by)

    if not all_users:
        flash("No hay usuarios cargados en el sistema.", "info")
        return render_template("home.html")
        
    return render_template("users/show_users.html", list = all_users, page=page, max_pages=max_pages)



        
        



