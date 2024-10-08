from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users, auth
from src.core.models.users import Role

bp = Blueprint('users',__name__,url_prefix="/users")

@bp.get("/")
def users_list():  # preguntar como tienen que ser los nombres list_users o users_list

    #obtengo nro de pagina o por defecto tomo el 1
    page = request.args.get('page', 1, type=int) 

    # obtengo el usuario iniciado en sesion
    current_user = session.get("user")

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

    print(email)
    # find_users tambien me devuelve la cantidad maxima de paginas para que sea evaluado en el html
    all_users, max_pages = users.find_users(page=page, email=email, active=active, role_name=role, sort_by=sort_by, exclude_user=current_user)
        
    return render_template("users/show_users.html", list = all_users, page=page, max_pages=max_pages)



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


@bp.get("/delete_user")
def delete_user():
    user_email = request.args.get("user_email")
    print(user_email)
    users.user_delete(user_email)
    flash("User deleted successfully")
    return redirect(url_for("users.users_list", flash=flash) )


@bp.get("/user_register_form")
def user_register_form():
    roles = Role.query.all()
    return render_template("users/register.html", roles=roles)



@bp.route("/register", methods=["GET", "POST"])
def user_create():

    if request.method == "POST":
        user = auth.check_user(request.form["email"], request.form["password"])

        if not user:
            auth.create_user(email=request.form["email"], nickname=request.form["nickname"], password=request.form["password"], role_id=request.form["role_id"])
            flash("Usuario creado exitosamente")
        else:
            flash("El usuario ingresado ya existe", "info")
        
    roles = Role.query.all()

    return render_template("users/register.html", roles=roles)  

