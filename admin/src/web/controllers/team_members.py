from flask import Blueprint, render_template, request, url_for, redirect, session, flash, send_file
from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum
from src.core import team_member as tm
from src.core import health_insurance as hi
from src.core import auth as au
from src.core import users as us
from src.core import minio
import mimetypes
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions


bp = Blueprint('team_members',__name__,url_prefix="/team_members")


@bp.get("/")
@check_permissions("team_member_index")
@login_required
def team_member_index():

    page = request.args.get('page', 1, type=int) 

    # obtengo los filtros del formulario
    name = request.args.get('name', None)
    last_name = request.args.get('last_name', None)
    dni = request.args.get('dni', None)
    email = request.args.get('email', None)
    jobs = request.args.get('job', None)
    sort_by = request.args.get('sort_by', None)

    # find_users tambien me devuelve la cantidad maxima de paginas para que sea evaluado en el html
    all_team_members, max_pages = tm.find_team_members(page=page, email=email, name=name, last_name=last_name, dni=dni, jobs=jobs, sort_by=sort_by)
    all_jobs = JobEnum.enums

    return render_template("team_members/show_team_members.html", list=all_team_members, max_pages = max_pages, page=page, jobs = all_jobs)

@bp.get("/new")
@check_permissions("team_member_create")
@login_required
def team_member_new():

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums

    health_insurances = hi.get_all()

    return render_template("team_members/new.html", professions=professions, conditions=conditions, job_positions=jobs, health_insurances=health_insurances)

@bp.post("/create")
@check_permissions("team_member_create")
@login_required
def team_member_create():

    team_member = tm.check_team_member_by_email(request.form["email"])

    if team_member:
        flash("El miembro de equipo ya existe", "info")
        return redirect(url_for("team_members.team_member_new"))
    
    

    file_keys = ['title', 'dni_copy', 'cv']
    files = {key: request.files[key] for key in file_keys if key in request.files}

    tm.create(request.form, files)
    
    return redirect(url_for("team_members.team_member_new"))

@bp.get("show_team_member")
@check_permissions("team_member_show")
@login_required
def team_member_show():
    team_member_email = request.args.get('team_member_email')   ##Deberia tomarlo por el id?

    

    team_member = tm.check_team_member_by_email(team_member_email)

    health_insurance = hi.get_by_id(team_member.health_insurance_id)

    
    return render_template("team_members/view_team_member.html", team_member=team_member, health_insurance = health_insurance)

@bp.get("/edit")
@check_permissions("team_member_edit")
@login_required
def team_member_edit():

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums

    team_member_email = request.args.get('team_member_email')

    team_member = tm.check_team_member_by_email(team_member_email)

    health_insurances = hi.get_all()

    return render_template("team_members/edit_team_member.html", team_member = team_member, health_insurances = health_insurances, professions = professions, conditions = conditions, jobs = jobs)


@bp.post("/update")
@check_permissions("team_member_update")
@login_required
def team_member_update():

    team_member_email = request.args.get('team_member_email')

    file_keys = ['title', 'dni_copy', 'cv']
    files = {key: request.files[key] for key in file_keys if key in request.files}

    tm.edit(team_member_email, request.form, files)
        

    flash("Miembro del equipo actualizado")
    return redirect(url_for('team_members.team_member_index'))



@bp.post("/switch")
@check_permissions("team_member_switch_state")
@login_required
def team_member_switch_state():


    team_member_email = request.args.get('team_member_email')
    team_member = tm.check_team_member_by_email(team_member_email)

    if team_member:
        tm.switch_state(team_member)
        user_associated=au.find_user_by_email(team_member_email)
        if user_associated:
            us.switch_state(team_member_email)
        flash("Se cambio el estado del miembro del equipo")
    

    return redirect(url_for('team_members.team_member_index'))

@bp.get("/view_file/<int:id>/<string:filename>")
def view_file(id, filename):

    file_data, content_type = minio.get_file("team_members", id, filename) 

    if not file_data:
        return "Archivo no encontrado", 404
    
    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)
    
        # For PDF files
    if content_type == 'application/pdf':
        return send_file(
            file_data,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )
    
    # For images
    elif content_type.startswith('image/'):
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=False,
            download_name=filename
        )
    
    # For other files, force download
    else:
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=True,
            download_name=filename
        )
