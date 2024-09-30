from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users, auth
from src.core.models.users import Role

bp = Blueprint('users',__name__,url_prefix="/users")

@bp.get("/")
def users_list():  # preguntar como tienen que ser los nombres list_users o users_list

    #obtengo nro de pagina o por defecto tomo el 1
    page = request.args.get('page', 1, type=int) 

    all_users = users.find_users(page)

    if not all_users:
        flash("No hay usuarios cargados en el sistema.", "info")
        return render_template("home.html")
        
    return render_template("users/show_users.html", list= all_users)


@bp.post("/update")
def user_update():
    """
    Updates a user
    """
    user_mail = request.args.get('user_email')
    print(user_mail)
    user = users.edit(
        email=user_mail,
        nickname=request.form["nickname"],
        system_admin=request.form.get("system_admin", False),
        role_id=1
    )

    if not user:
        flash("No existe el usuario")
    else:
        flash("Usuario actualizado")
    return redirect(url_for("users.users_list", flash=flash) )

@bp.get("/edit")
def user_edit():
    """
    Edits a user
    """
    user_mail = request.args.get('user_email')
    user = auth.find_user_by_email(user_mail)
    roles = Role.query.all()
    return render_template("users/edit_user.html", user=user,roles=roles)

