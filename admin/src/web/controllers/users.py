from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core import users, auth
from src.core import team_member as tm
from src.core.models.users import Role
from src.web.forms.UserForm import RegisterForm, UserEditForm
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions
bp = Blueprint('users', __name__, url_prefix="/users")


@bp.get("/")
@check_permissions("user_index")
@login_required
def user_index():
    # Get page number or default to 1
    page = request.args.get('page', 1, type=int)

    # Get the user logged in session
    current_user = session.get("user")

    # Get filters from the form
    email = request.args.get('email', None)
    active = request.args.get('active', None)
    role = request.args.get('role', None)
    sort_by = request.args.get('sort_by', None)

    # Convert the 'active' filter to a boolean value
    if active == 'YES':
        active = True
    elif active == 'NO':
        active = False
    else:
        active = None  # Do not apply filter

    # find_users also returns the maximum number of pages to be evaluated in the HTML
    all_users, max_pages = users.find_users(
        page=page, email=email, active=active, role_name=role, sort_by=sort_by, exclude_user=current_user)

    return render_template("users/show_users.html", list=all_users, page=page, max_pages=max_pages)


@bp.post("/update")
@check_permissions("user_update")
@login_required
def user_update():
    """
    Updates a user
    """
    user_mail = request.args.get('user_email')
    user = users.edit(
        email=user_mail,
        nickname=request.form["nickname"],
        system_admin=request.form.get("system_admin", False),
        role_id=request.form["role_id"]
    )

    form = UserEditForm(request.form)
    if form.validate():

        user = users.edit(
            email=user_mail,
            nickname=request.form["nickname"],
            system_admin=request.form.get("system_admin", False),
            role_id=request.form["role_id"]
        )
        if not user:
            flash("No existe el usuario")
        else:
            flash("Usuario actualizado")
    else:
        flash("Usuario actualizado")
    return redirect(url_for("users.user_index", flash=flash))


@bp.get("/edit")
@check_permissions("user_edit")
@login_required
def user_edit():
    """
    Edits a user
    """
    user_mail = request.args.get('user_email')
    user = auth.find_user_by_email(user_mail)
    roles = Role.query.all()
    return render_template("users/edit_user.html", user=user, roles=roles)


@bp.post("/delete_user")
@check_permissions("user_delete")
@login_required
def user_delete():
    user_email = request.args.get("user_email")
    users.user_delete(user_email)
    flash("Usuario eliminado de manera correcta.")
    return redirect(url_for("users.user_index", flash=flash))


@bp.route("/register", methods=["GET", "POST"])
def user_new():

    if request.method == "POST":

        form = RegisterForm(request.form)
        if form.validate():
            user = auth.check_user(
                request.form["email"], request.form["password"])

            if not user:
                auth.create_user(email=request.form["email"], nickname=request.form["nickname"],
                                 password=request.form["password"], role_id=request.form["role_id"])
                flash("Usuario creado exitosamente")
            else:
                flash("El usuario ingresado ya existe", "info")
        else:
            flash("Faltan campos por completar", "info")

    roles = Role.query.all()

    return render_template("users/register.html", roles=roles, form=request.form)


@bp.get("/user_switch_state")
def user_switch_state():

    check_return = request.args.get('check_return')
    user_email = request.args.get('user_email')
    team_member = tm.find_team_member_by_email(user_email)

    if not users.switch_state(user_email):
        flash("No se puede cambiar el estado a un administrador", "info")
    else:
        if team_member:
            tm.switch_state(team_member)
        flash("Se cambio el estado satisfactoriamente")

    if check_return == 1:
        return redirect(url_for('users.user_profile'))
    return redirect(url_for("users.user_index"))


@bp.get("/user_profile")
@login_required
def user_profile():
    user_email = request.args.get('user_email')

    if user_email is None:
        user_email = session.get('user')

    user = auth.find_user_by_email(user_email)
    team_member = tm.find_team_member_by_email(user_email)

    return render_template("users/view_user.html", user=user, team_member=team_member)
